#!/usr/bin/env python3
"""Check that the XML embedded in the primer's Markdown is well-formed.

Usage:
    python3 meta-conversion/check-xml.py [PATH ...] [--strict] [--verbose]

With no PATH, every *.md in the repository is scanned. A PATH may be a file or
a directory. Exit status is 0 when every block is well-formed, 1 otherwise
(with --strict, warnings fail the run too).

Why this isn't just "parse the fence"
-------------------------------------
The snippets in the primer are fragments: they open with <rdf:RDF> but declare
no namespaces, because the prose declares them once in
introduction/namespaces-and-examples.md and every later example leaves them out
for brevity. Handing one to an XML parser as-is fails with "unbound prefix" on
the first line, which says nothing about whether the snippet is actually sound.

So each block is first patched the same way bibframe.org patches it before
rendering (see prepareRdfXml in documentation-tool,
client/src/utils/rdf/rdfxml.js): declarations are added for prefixes that are
used but undeclared, and a bare fragment with no rdf:RDF root gets wrapped in
one. The patching only ever edits within a line or adds whole lines ahead of
the content, so parser positions map back onto real line numbers in the .md
file and every message is reported as path:line:column.

What gets reported
------------------
error   the block is not well-formed XML (mismatched tag, stray '&' or an
        undefined entity such as &nbsp;, duplicate attribute, bad character)
warning the block uses a namespace prefix that is neither declared nor
        well known, so the website falls back to a placeholder namespace
        and the block will not mean what it appears to mean
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

RDF_NS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"

# Namespaces assumed for prefixes a snippet uses without declaring. Keep this in
# step with WELL_KNOWN_PREFIXES in documentation-tool's
# client/src/utils/rdf/terms.js -- that table is what the website substitutes,
# so a prefix missing from here but present there would be flagged as a warning
# the website never shows (and the reverse would hide a real problem).
WELL_KNOWN_PREFIXES = {
    "rdf": RDF_NS,
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "skosxl": "http://www.w3.org/2008/05/skos-xl#",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "dct": "http://purl.org/dc/terms/",
    "dctype": "http://purl.org/dc/dcmitype/",
    "schema": "http://schema.org/",
    "sdo": "https://schema.org/",
    "bf": "http://id.loc.gov/ontologies/bibframe/",
    "bflc": "http://id.loc.gov/ontologies/bflc/",
    "madsrdf": "http://www.loc.gov/mads/rdf/v1#",
    "lcc": "http://id.loc.gov/ontologies/lcc#",
    "premis": "http://www.loc.gov/premis/rdf/v3/",
}

# Fence languages read as RDF/XML no matter what the body looks like, matching
# RDF_XML_LANGS in client/src/utils/rdf/detect.js.
RDF_XML_LANGS = {"rdf", "rdfxml", "rdf-xml", "rdf/xml", "application/rdf+xml"}
# Fence languages checked as plain XML even when the body isn't RDF at all.
XML_LANGS = {"xml", "application/xml", "text/xml"}

NAME = r"[A-Za-z_][\w.\-]*"
FENCE_OPEN_RE = re.compile(r"^( {0,3})(`{3,}|~{3,})[ \t]*(.*)$")
FENCE_CLOSE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})[ \t]*$")
XMLNS_DECL_RE = re.compile(rf"""xmlns:({NAME})\s*=\s*(?:"([^"]*)"|'([^']*)')""")
TAG_RE = re.compile(rf"<\/?({NAME}):{NAME}(?:\s[^>]*)?>")
ATTR_RE = re.compile(rf"\s({NAME}):{NAME}\s*=")
# Leading byte-order mark, whitespace and XML declaration -- legal only at the
# very top of a document, and dropped by the website before parsing.
LEAD_RE = re.compile(r"^﻿?[ \t\r\n]*(?:<\?xml[^>]*\?>)?")
RDF_ROOT_RE = re.compile(rf"^(?:[ \t\r\n]|<!--.*?-->)*<({NAME}):RDF(?=[\s/>])", re.S)
# xml.etree appends its own ": line N, column N" to the message; we print our own.
ET_POSITION_RE = re.compile(r":?\s*line \d+, column \d+\s*$")

WRAP_PREFIX = "wfcheck"
WRAP_NS = "http://invalid.example/wellformed-check#"


@dataclass
class Block:
    """A fenced code block, with the source lines it came from."""

    path: Path
    lang: str
    code: str
    fence_line: int  # 1-based line of the opening fence
    start_line: int  # 1-based line of the first content line


@dataclass
class Problem:
    path: Path
    line: int
    column: int | None
    severity: str
    message: str
    fence_line: int

    def render(self, root: Path) -> str:
        try:
            where = self.path.relative_to(root)
        except ValueError:
            where = self.path
        column = f":{self.column}" if self.column is not None else ""
        return (
            f"{where}:{self.line}{column}: {self.severity}: {self.message} "
            f"(block opened at line {self.fence_line})"
        )


def blank_keep_lines(text: str) -> str:
    """Replace text with spaces, keeping newlines so line numbers don't shift."""
    return "".join("\n" if ch == "\n" else " " for ch in text)


def iter_fenced_blocks(path: Path, text: str):
    """Yield every fenced code block in a Markdown document."""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        opening = FENCE_OPEN_RE.match(lines[i])
        # A backtick fence's info string may not itself contain a backtick.
        if not opening or (opening.group(2)[0] == "`" and "`" in opening.group(3)):
            i += 1
            continue
        indent, fence, info = opening.groups()
        lang = info.split()[0] if info.split() else ""
        body: list[str] = []
        j = i + 1
        while j < len(lines):
            closing = FENCE_CLOSE_RE.match(lines[j])
            if closing and closing.group(1)[0] == fence[0] and len(closing.group(1)) >= len(fence):
                break
            # Content is indented to match its fence; strip no more than that.
            body.append(re.sub(rf"^ {{0,{len(indent)}}}", "", lines[j]) if indent else lines[j])
            j += 1
        yield Block(
            path=path,
            lang=lang,
            code="\n".join(body),
            fence_line=i + 1,
            start_line=i + 2,
        )
        i = j + 1


def declared_prefixes(code: str) -> dict[str, str]:
    """Every prefix the snippet binds with an xmlns: declaration."""
    found = {}
    for match in XMLNS_DECL_RE.finditer(code):
        quoted = match.group(2)
        found[match.group(1)] = quoted if quoted is not None else match.group(3)
    return found


def rdf_prefix_in(code: str) -> str:
    """Whichever prefix the snippet binds to the RDF namespace; "rdf" if none."""
    for prefix, namespace in declared_prefixes(code).items():
        if namespace == RDF_NS:
            return prefix
    return "rdf"


def used_prefixes(code: str) -> set[str]:
    """Prefixes that element and attribute names rely on (searching tags only)."""
    used = set()
    for tag in TAG_RE.finditer(code):
        used.add(tag.group(1))
        for attr in ATTR_RE.finditer(tag.group(0)):
            used.add(attr.group(1))
    used.discard("xml")  # bound by the spec itself
    used.discard("xmlns")
    return used


def looks_like_rdf_xml(lang: str, code: str) -> bool:
    """Port of looksLikeRdfXml in client/src/utils/rdf/detect.js."""
    tag = (lang or "").strip().lower()
    if tag in RDF_XML_LANGS:
        return True
    if tag not in ("", "xml"):
        return False
    if "<" not in code:
        return False
    prefix = re.escape(rdf_prefix_in(code))
    return (
        re.search(
            rf"<{prefix}:(?:RDF|Description)(?=[\s/>])"
            rf"|\s{prefix}:(?:about|resource|nodeID|ID|parseType|datatype)\s*=",
            code,
        )
        is not None
    )


def should_check(block: Block) -> bool:
    """Blocks the website will try to parse, plus anything tagged as XML."""
    tag = block.lang.strip().lower()
    if tag in XML_LANGS or tag in RDF_XML_LANGS:
        return True
    return looks_like_rdf_xml(block.lang, block.code)


@dataclass
class Prepared:
    xml: str
    lead_lines: int  # whole lines added ahead of the content
    undeclared: list[str]  # used, undeclared and not well known
    injected: dict[str, str]
    wrapped: bool


def prepare(code: str) -> Prepared:
    """Make a parseable document out of a snippet, without moving any line."""
    code = LEAD_RE.sub(lambda m: blank_keep_lines(m.group(0)), code, count=1)
    declared = declared_prefixes(code)

    root = RDF_ROOT_RE.search(code)
    if root:
        prefix = root.group(1)
        has_root = declared[prefix] == RDF_NS if prefix in declared else prefix == "rdf"
    else:
        has_root = False

    injected: dict[str, str] = {}
    undeclared: list[str] = []
    decls: list[str] = []
    for prefix in sorted(used_prefixes(code)):
        if prefix in declared:
            continue
        namespace = WELL_KNOWN_PREFIXES.get(prefix)
        if namespace is None:
            namespace = f"http://invalid.example/undeclared/{prefix}#"
            undeclared.append(prefix)
        injected[prefix] = namespace
        decls.append(f'xmlns:{prefix}="{namespace}"')

    if has_root:
        # Widen the existing root tag in place, so every line keeps its number.
        addition = (" " + " ".join(decls)) if decls else ""
        xml = RDF_ROOT_RE.sub(lambda m: m.group(0) + addition, code, count=1)
        return Prepared(xml, 0, undeclared, injected, wrapped=False)

    if "rdf" not in injected and "rdf" not in declared:
        decls.insert(0, f'xmlns:rdf="{RDF_NS}"')
    wrapper = f'<{WRAP_PREFIX}:document xmlns:{WRAP_PREFIX}="{WRAP_NS}" ' + " ".join(decls) + ">"
    xml = f"{wrapper}\n{code}\n</{WRAP_PREFIX}:document>"
    return Prepared(xml, 1, undeclared, injected, wrapped=True)


def check_block(block: Block, show_prepared: bool = False) -> list[Problem]:
    """Parse one block and turn any complaint into source-line problems."""
    prepared = prepare(block.code)
    problems = []

    for prefix in prepared.undeclared:
        problems.append(
            Problem(
                path=block.path,
                line=block.start_line,
                column=None,
                severity="warning",
                message=(
                    f'namespace prefix "{prefix}" is used but never declared, and is not '
                    f"well known; the website will substitute a placeholder namespace"
                ),
                fence_line=block.fence_line,
            )
        )

    try:
        ET.fromstring(prepared.xml)
    except ET.ParseError as exc:
        line, column = exc.position  # 1-based line, 0-based column
        source_line = block.start_line + line - 1 - prepared.lead_lines
        message = ET_POSITION_RE.sub("", str(exc)).strip() or "malformed XML"
        problems.append(
            Problem(
                path=block.path,
                # An error landing on the synthetic wrapper is reported against
                # the fence, since there is no real line for it.
                line=max(source_line, block.fence_line),
                column=column + 1 if source_line >= block.start_line else None,
                severity="error",
                message=message,
                fence_line=block.fence_line,
            )
        )
        if show_prepared:
            print(f"--- prepared XML for block at line {block.fence_line} ---", file=sys.stderr)
            print(prepared.xml, file=sys.stderr)
            print("--- end ---", file=sys.stderr)

    return problems


def markdown_files(paths: list[Path]) -> list[Path]:
    found: list[Path] = []
    for path in paths:
        if path.is_dir():
            found.extend(
                p for p in path.rglob("*.md") if ".git" not in p.parts
            )
        elif path.is_file():
            found.append(path)
        else:
            print(f"check-xml.py: no such file or directory: {path}", file=sys.stderr)
    return sorted(set(found))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check that the XML embedded in Markdown code fences is well-formed."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Markdown files or directories to scan (default: the whole repository)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat warnings as failures",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="name every block checked, not just the ones with problems",
    )
    parser.add_argument(
        "--show-prepared",
        action="store_true",
        help="dump the patched XML for any block that fails to parse",
    )
    args = parser.parse_args()

    files = markdown_files(args.paths or [REPO_ROOT])
    if not files:
        print("check-xml.py: nothing to check", file=sys.stderr)
        return 1

    problems: list[Problem] = []
    blocks_checked = 0
    files_with_blocks = 0

    for path in files:
        text = path.read_text(encoding="utf-8")
        blocks = [b for b in iter_fenced_blocks(path, text) if should_check(b)]
        if blocks:
            files_with_blocks += 1
        for block in blocks:
            blocks_checked += 1
            found = check_block(block, show_prepared=args.show_prepared)
            problems.extend(found)
            if args.verbose and not found:
                where = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
                print(f"{where}:{block.fence_line}: ok ({block.lang or 'no language'})")

    for problem in sorted(problems, key=lambda p: (str(p.path), p.line)):
        print(problem.render(REPO_ROOT))

    errors = sum(1 for p in problems if p.severity == "error")
    warnings = len(problems) - errors
    print(
        f"\nChecked {blocks_checked} XML block(s) in {files_with_blocks} file(s) "
        f"of {len(files)} scanned: {blocks_checked - errors} well-formed, "
        f"{errors} malformed, {warnings} warning(s)"
    )

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
