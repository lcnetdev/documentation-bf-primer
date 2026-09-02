#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "pypandoc_binary==1.17",
#   "lxml>=5.0",
# ]
# ///
"""Break the BIBFRAME Primer .docx apart into separate Markdown pages.

Usage:
    uv run meta-conversion/convert.py [FILE.docx] [--out DIR] [--debug-dir DIR]

Everything here runs on fixed rules, so a given .docx always comes out
byte-for-byte identical. Before writing anything new, each run first deletes
whatever the previous run produced, as listed in
meta-conversion/generated-files.txt.

Pipeline
--------
1. Patch word/document.xml first (with lxml):
   - Read the Word table of contents (the TOC 1/2/3 paragraphs) into an
     ordered list of (level, title, bookmark anchor).
   - Drop the TOC itself from the body.
   - Trim line breaks from both ends of every paragraph.
   - Squash fenced code (~~~xml ... ~~~ or ```xml ... ```) that was typed out
     as ordinary paragraphs down to a single placeholder paragraph, stashing
     the code text (indentation included) on the side. Fences don't need a
     paragraph to themselves; one can open or close a paragraph that also
     carries other text. A fence that doesn't name a language is read as
     xml, and so is any run of two or more paragraphs that are bare XML tag
     lines.
   - Promote every paragraph the TOC points at to a real HeadingN at the
     TOC's level. Anything after the first line break in such a heading is
     split off into its own subtitle paragraph, and a marker paragraph goes
     in front of each heading.
   - Throw away empty headings; note leading tabs and first-line indents so
     Markdown can render them as &nbsp; indentation.
2. Hand the patched .docx to pypandoc and get back a pandoc JSON AST.
3. Swap the placeholders for CodeBlocks, cut the AST at the section markers,
   and assemble the chapter/page tree from the TOC levels: level 1 makes a
   chapter (a directory with index.md, or a lone root file when the chapter
   has no level-2 children), level 2 makes a page file, and level 3+ become
   headings within a page.
4. Render every page to GitHub-flavored Markdown via pandoc, then write out
   the files, images, index pages and manifest. Every page ends with a
   back-to-TOC link and previous/next links; each index.md additionally ends
   with a <!-- NAV_ORDER ... --> comment listing its entries in TOC order.
   Every list is written tight (no blank lines between items) so items don't
   render as paragraphs inside <li>.
   Runs of indented single-token lines (property lists) become tight bullet
   lists preceded by <!-- LIST_STYLE: compact two-column --> for the renderer,
   and the italic property paths that open a page become a tight bullet list
   preceded by <!-- LIST_STYLE: compact single-column no-bullet -->, where the
   lines after a path ending in a class are indented under it; bf:/bflc:
   terms in either kind are linked to the ontology page anchors.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys
import tempfile
import unicodedata
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

import pypandoc
from lxml import etree

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_NS = "http://www.w3.org/XML/1998/namespace"
NS = {"w": W_NS}


def w(tag: str) -> str:
    return f"{{{W_NS}}}{tag}"


FENCE_RE = re.compile(r"^\s*([~`]{2,})[ \t]*([A-Za-z0-9_+.#-]*)[ \t]*$")
FENCE_START_RE = re.compile(r"^\s*[~`]{2,}")
DEFAULT_CODE_LANG = "xml"  # the language we assume when a fence doesn't declare one
XML_LINE_RE = re.compile(r"^\s*<[A-Za-z/!?][^\n]*>\s*$")  # a paragraph that is nothing but a single XML tag
SECTION_MARK = "@@SECTION:{}@@"
CODE_MARK = "@@CODE:{}@@"
INDENT_MARK = "@@INDENT:{}@@"
SECTION_RE = re.compile(r"^@@SECTION:(.+)@@$")
CODE_RE = re.compile(r"^@@CODE:(\d+)@@$")
INDENT_RE = re.compile(r"^@@INDENT:(\d+)@@(.*)$", re.S)
TWIPS_PER_SPACE = 180  # 720 twips is Word's usual indent step, which comes out to 4 spaces
TAB_SPACES = 4
NBSP = " "
WORD_AUTO_ALT_RE = re.compile(r"AI-generated content may be incorrect", re.I)
# Indented list lines that consist of a single vocabulary term become links to the ontology site.
TERM_RE = re.compile(r"^(bf|bflc):([A-Za-z][A-Za-z0-9]*)$")
TOKEN_RE = re.compile(r"^(?!https?://)\S+$")  # an indented single token (a property name, not a URL)
# Property lists become tight bullet lists preceded by a marker that tells the renderer how
# to lay them out: runs of 2+ indented single-token lines get TERM_LIST_STYLE, and the italic
# property paths that open a page (bf:language/bf:Language ...) get PATH_LIST_STYLE.
LIST_STYLE_MARK = "<!-- LIST_STYLE: {} -->"
TERM_LIST_STYLE = "compact two-column"
PATH_LIST_STYLE = "compact single-column no-bullet"
PAGE_HEADING_LEVELS = (1, 2)  # TOC levels whose headings open a page of their own
# A property path whose last step is a class (bf:provisionActivity/bf:ProvisionActivity); the
# lines that follow it in a page-top list are its properties and get indented one step.
CLASS_PATH_RE = re.compile(r"(?:^|/)[A-Za-z]+:[A-Z][A-Za-z0-9]*$")
BRACKET_RE = re.compile(r"\[[^\]]*\]")  # [type=Language] qualifiers, ignored when reading a path
ONTOLOGY_URL = {
    "bf": "https://id.loc.gov/ontologies/bibframe.html",
    "bflc": "https://id.loc.gov/ontologies/bflc.html",
}
BACK_LINK_TEXT = "Back to Table of Contents"
PREV_LINK_TEXT = "Previous Page"
NEXT_LINK_TEXT = "Next Page"
NAV_ORDER_TAG = "NAV_ORDER"  # appended to every index.md as an HTML comment spelling out the nav order
MANIFEST_NAME = "generated-files.txt"

REPO_ROOT = Path(__file__).resolve().parent.parent
META_DIR = Path(__file__).resolve().parent


def warn(msg: str) -> None:
    print(f"WARNING: {msg}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Word styles (styles.xml)
# ---------------------------------------------------------------------------


class Styles:
    """Lookup table linking style ids to their (lowercased) names from styles.xml."""

    def __init__(self, styles_xml: bytes | None):
        self.id_to_name: dict[str, str] = {}
        self.name_to_id: dict[str, str] = {}
        if styles_xml:
            root = etree.fromstring(styles_xml)
            for st in root.iter(w("style")):
                sid = st.get(w("styleId"))
                name_el = st.find("w:name", NS)
                if sid is None or name_el is None:
                    continue
                name = (name_el.get(w("val")) or "").strip().lower()
                self.id_to_name[sid] = name
                self.name_to_id.setdefault(name, sid)

    def name(self, style_id: str | None) -> str:
        if style_id is None:
            return ""
        return self.id_to_name.get(style_id, style_id.lower())

    def toc_level(self, style_id: str | None) -> int | None:
        m = re.fullmatch(r"toc\s*(\d)", self.name(style_id))
        return int(m.group(1)) if m else None

    def is_toc_heading(self, style_id: str | None) -> bool:
        return self.name(style_id) in ("toc heading", "tocheading")

    def heading_level(self, style_id: str | None) -> int | None:
        m = re.fullmatch(r"heading\s*(\d)", self.name(style_id))
        return int(m.group(1)) if m else None

    def heading_id(self, level: int) -> str:
        return self.name_to_id.get(f"heading {level}", f"Heading{level}")


# ---------------------------------------------------------------------------
# paragraph-level utilities
# ---------------------------------------------------------------------------

RUN_CONTENT_TAGS = {w("t"), w("tab"), w("br"), w("cr"), w("drawing"), w("pict"), w("sym"), w("object")}
BREAK_TAGS = {w("br"), w("cr")}


def iter_runs(p):
    """Yield a paragraph's runs in document order, ignoring tracked-change deletions."""
    for r in p.iter(w("r")):
        anc = r.getparent()
        skip = False
        while anc is not None and anc is not p:
            if anc.tag in (w("del"), w("moveFrom"), w("pPr")):
                skip = True
                break
            anc = anc.getparent()
        if not skip:
            yield r


def content_items(p):
    """The elements of a paragraph that actually carry content (text, tabs, breaks, drawings), in order."""
    items = []
    for r in iter_runs(p):
        for el in r:
            if el.tag in RUN_CONTENT_TAGS:
                if el.tag == w("t") and not (el.text or ""):
                    continue
                items.append(el)
    return items


def para_text(p, tab: str = "\t", br: str = "\n") -> str:
    parts = []
    for el in content_items(p):
        if el.tag == w("t"):
            parts.append(el.text or "")
        elif el.tag == w("tab"):
            parts.append(tab)
        elif el.tag in BREAK_TAGS:
            parts.append(br)
    return "".join(parts)


def clean_title(text: str) -> str:
    return " ".join(text.replace(NBSP, " ").split())


def get_style(p) -> str | None:
    el = p.find("w:pPr/w:pStyle", NS)
    return el.get(w("val")) if el is not None else None


def set_style(p, style_id: str) -> None:
    ppr = p.find("w:pPr", NS)
    if ppr is None:
        ppr = etree.Element(w("pPr"))
        p.insert(0, ppr)
    ps = ppr.find("w:pStyle", NS)
    if ps is None:
        ps = etree.Element(w("pStyle"))
        ppr.insert(0, ps)
    ps.set(w("val"), style_id)


def has_numbering(p) -> bool:
    return p.find("w:pPr/w:numPr", NS) is not None


def has_drawing(p) -> bool:
    return any(True for _ in p.iter(w("drawing"))) or any(True for _ in p.iter(w("pict")))


def remove_empty_runs(p) -> None:
    for r in list(p.iter(w("r"))):
        if all(ch.tag == w("rPr") for ch in r):
            r.getparent().remove(r)


def make_text_paragraph(text: str):
    p = etree.Element(w("p"))
    r = etree.SubElement(p, w("r"))
    t = etree.SubElement(r, w("t"))
    t.text = text
    t.set(f"{{{XML_NS}}}space", "preserve")
    return p


def indent_twips(p) -> int:
    ind = p.find("w:pPr/w:ind", NS)
    if ind is None:
        return 0

    def num(attr: str) -> int:
        try:
            return int(ind.get(w(attr)) or 0)
        except ValueError:
            return 0

    left = num("left") or num("start")
    return max(0, left + num("firstLine") - num("hanging"))


def strip_edge_breaks(p) -> None:
    """Drop line/page breaks sitting at the very beginning or very end of a paragraph."""
    items = content_items(p)
    leading = []
    for el in items:
        if el.tag in BREAK_TAGS:
            leading.append(el)
        else:
            break
    trailing = []
    for el in reversed(items[len(leading):]):
        if el.tag in BREAK_TAGS:
            trailing.append(el)
        else:
            break
    for el in leading + trailing:
        el.getparent().remove(el)
    if leading or trailing:
        remove_empty_runs(p)


def split_at_first_break(p):
    """Cut a paragraph in two at its first line break; returns the freshly created tail, or None if there is no break."""
    breaks = [el for el in content_items(p) if el.tag in BREAK_TAGS]
    if not breaks:
        return None
    br = breaks[0]
    run = br.getparent()
    tail = etree.Element(w("p"))
    run_children = list(run)
    after = run_children[run_children.index(br) + 1:]
    if after:
        new_run = etree.SubElement(tail, w("r"))
        rpr = run.find("w:rPr", NS)
        if rpr is not None:
            new_run.append(copy.deepcopy(rpr))
        for ch in after:
            new_run.append(ch)
    run.remove(br)
    top = run
    while top.getparent() is not p:
        top = top.getparent()
    for sib in list(top.itersiblings()):
        tail.append(sib)
    remove_empty_runs(p)
    p.addnext(tail)
    return tail


# ---------------------------------------------------------------------------
# digging out the document TOC
# ---------------------------------------------------------------------------


@dataclass
class TocEntry:
    level: int
    title: str
    anchor: str


def parse_toc(body, styles: Styles) -> list[TocEntry]:
    entries: list[TocEntry] = []
    for p in body.iter(w("p")):
        level = styles.toc_level(get_style(p))
        if level is None:
            continue
        anchor = None
        link = p.find(".//w:hyperlink", NS)
        if link is not None:
            anchor = link.get(w("anchor"))
        if not anchor:
            for it in p.iter(w("instrText")):
                m = re.search(r"PAGEREF\s+(\S+)", it.text or "")
                if m:
                    anchor = m.group(1)
                    break
        text = para_text(p, tab="\t", br=" ")
        if "\t" in text:
            title = text.split("\t", 1)[0]
        else:
            title = re.sub(r"\s*\d+\s*$", "", text)
        title = clean_title(title)
        if not anchor or not title:
            warn(f"skipping TOC paragraph without anchor/title: {text!r}")
            continue
        entries.append(TocEntry(level, title, anchor))
    return entries


def remove_toc(body, styles: Styles) -> None:
    for sdt in list(body.iter(w("sdt"))):
        gallery = sdt.find(".//w:docPartGallery", NS)
        if gallery is not None and (gallery.get(w("val")) or "").lower() == "table of contents":
            sdt.getparent().remove(sdt)
    for p in list(body.iter(w("p"))):
        st = get_style(p)
        if styles.toc_level(st) is not None or styles.is_toc_heading(st):
            p.getparent().remove(p)


# ---------------------------------------------------------------------------
# collapsing code blocks
# ---------------------------------------------------------------------------


@dataclass
class CodeBlock:
    lang: str
    text: str


def collapse_code_regions(body) -> list[CodeBlock]:
    """Collapse everything between an opening fence and its closing partner
    into a single placeholder paragraph.

    Matching works line by line (a paragraph's text is split on its line
    breaks first), so a fence may live in a paragraph of its own or share
    one with the code it wraps.
    """
    blocks: list[CodeBlock] = []
    open_para = None
    lang = ""
    lines: list[str] = []

    def add_code(p, plines: list[str]) -> None:
        indent = " " * round(indent_twips(p) / TWIPS_PER_SPACE)
        for line in plines:
            line = line.replace(NBSP, " ").expandtabs(TAB_SPACES).rstrip()
            lines.append(indent + line if line else "")

    def close_block(p, trailing: list[str]) -> None:
        nonlocal open_para
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        blocks.append(CodeBlock(lang, "\n".join(lines)))
        for ch in list(open_para):
            open_para.remove(ch)
        open_para.append(make_text_paragraph(CODE_MARK.format(len(blocks) - 1))[0])
        if p is not open_para:
            p.getparent().remove(p)
        if any(t.strip() for t in trailing):
            warn(f"text after a closing fence moved to its own paragraph: {' '.join(trailing)[:60]!r}")
            anchor = open_para
            for t in trailing:
                new_p = make_text_paragraph(t)
                anchor.addnext(new_p)
                anchor = new_p
        open_para = None

    for p in list(body.iter(w("p"))):
        plines = para_text(p, tab="\t", br="\n").split("\n")
        if open_para is None:
            idx = next((i for i, ln in enumerate(plines) if FENCE_RE.match(ln)), None)
            if idx is None:
                if FENCE_START_RE.match(plines[0]):
                    warn(f"paragraph looks like a code fence but was not recognized: {plines[0][:60]!r}")
                continue
            leading = plines[:idx]
            if any(t.strip() for t in leading):
                warn(f"text before an opening fence moved to its own paragraph: {' '.join(leading)[:60]!r}")
                for t in leading:
                    p.addprevious(make_text_paragraph(t))
            m = FENCE_RE.match(plines[idx])
            open_para, lang, lines = p, m.group(2) or DEFAULT_CODE_LANG, []
            remaining = plines[idx + 1:]
        else:
            remaining = plines
        close = next((i for i, ln in enumerate(remaining) if FENCE_RE.match(ln)), None)
        if close is None:
            add_code(p, remaining)
            if p is not open_para:
                p.getparent().remove(p)
        else:
            add_code(p, remaining[:close])
            close_block(p, remaining[close + 1:])
    if open_para is not None:
        raise SystemExit("ERROR: unterminated code fence in document")
    collapse_unfenced_xml(body, blocks)
    return blocks


def code_lines(p) -> list[str]:
    indent = " " * round(indent_twips(p) / TWIPS_PER_SPACE)
    out = []
    for line in para_text(p, tab="\t", br="\n").replace(NBSP, " ").split("\n"):
        line = line.expandtabs(TAB_SPACES).rstrip()
        out.append(indent + line if line else "")
    return out


def looks_like_xml(p) -> bool:
    lines = [ln for ln in para_text(p, tab=" ", br="\n").split("\n") if ln.strip()]
    return bool(lines) and all(XML_LINE_RE.match(ln) for ln in lines)


def collapse_unfenced_xml(body, blocks: list[CodeBlock]) -> None:
    """Any stretch of two or more back-to-back paragraphs of bare XML tag lines gets folded into an xml code block."""
    run: list = []

    def flush():
        if len(run) >= 2:
            lines = [ln for p in run for ln in code_lines(p)]
            blocks.append(CodeBlock(DEFAULT_CODE_LANG, "\n".join(lines)))
            first = run[0]
            for ch in list(first):
                first.remove(ch)
            first.append(make_text_paragraph(CODE_MARK.format(len(blocks) - 1))[0])
            for p in run[1:]:
                p.getparent().remove(p)
        run.clear()

    for p in list(body.iter(w("p"))):
        if looks_like_xml(p) and not has_numbering(p) and (not run or run[-1].getparent() is p.getparent()):
            run.append(p)
        else:
            flush()
    flush()


# ---------------------------------------------------------------------------
# fixing up headings
# ---------------------------------------------------------------------------


def find_anchor_paragraph(body, anchor: str):
    for bm in body.iter(w("bookmarkStart")):
        if bm.get(w("name")) != anchor:
            continue
        el = bm
        while el is not None and el.tag != w("p"):
            if el.getparent() is body or el.getparent() is None:
                nxt = el.getnext()
                while nxt is not None and nxt.tag != w("p"):
                    nxt = nxt.getnext()
                return nxt
            el = el.getparent()
        return el
    return None


def normalize_headings(body, entries: list[TocEntry], styles: Styles) -> dict[str, str]:
    """Promote each TOC target to a HeadingN paragraph and hand back a mapping of anchor -> heading text."""
    titles: dict[str, str] = {}
    seen: list[tuple[object, str]] = []  # hold onto the elements so later identity checks still work
    for entry in entries:
        p = find_anchor_paragraph(body, entry.anchor)
        if p is None:
            warn(f"TOC entry {entry.title!r} ({entry.anchor}) has no bookmark in the body; skipped")
            continue
        dup = next((t for el, t in seen if el is p), None)
        if dup is not None:
            warn(f"TOC entries {dup!r} and {entry.title!r} point at the same paragraph; skipped")
            continue
        seen.append((p, entry.title))
        strip_edge_breaks(p)
        split_at_first_break(p)
        set_style(p, styles.heading_id(entry.level))
        title = clean_title(para_text(p, tab=" ", br=" "))
        if not title:
            warn(f"TOC entry {entry.title!r} targets a paragraph with no text; using TOC title")
            p.append(make_text_paragraph(entry.title)[0])
            title = entry.title
        elif title.lower() not in entry.title.lower():
            warn(f"heading text {title!r} differs from TOC entry {entry.title!r}")
        titles[entry.anchor] = title
        p.addprevious(make_text_paragraph(SECTION_MARK.format(entry.anchor)))
    return titles


def remove_empty_headings(body, styles: Styles) -> None:
    for p in list(body.iter(w("p"))):
        if styles.heading_level(get_style(p)) is None:
            continue
        if not clean_title(para_text(p, tab=" ", br=" ")) and not has_drawing(p):
            p.getparent().remove(p)


def mark_indentation(body, styles: Styles) -> None:
    """Capture visual indentation (leading tabs, first-line indent) in a marker run."""
    for p in body.iter(w("p")):
        if has_numbering(p) or styles.heading_level(get_style(p)) is not None:
            continue
        items = content_items(p)
        tabs = []
        for el in items:
            if el.tag == w("tab"):
                tabs.append(el)
            else:
                break
        if not items or len(tabs) == len(items):
            continue
        ind = p.find("w:pPr/w:ind", NS)
        first_line = 0
        if ind is not None:
            try:
                first_line = int(ind.get(w("firstLine")) or 0)
            except ValueError:
                first_line = 0
        total = len(tabs) * TAB_SPACES + max(0, round(first_line / TWIPS_PER_SPACE))
        if total == 0:
            continue
        for el in tabs:
            el.getparent().remove(el)
        remove_empty_runs(p)
        run = make_text_paragraph(INDENT_MARK.format(total))[0]
        ppr = p.find("w:pPr", NS)
        if ppr is not None:
            ppr.addnext(run)
        else:
            p.insert(0, run)


# ---------------------------------------------------------------------------
# running the docx preprocessing
# ---------------------------------------------------------------------------


@dataclass
class Preprocessed:
    docx_path: Path
    entries: list[TocEntry]
    titles: dict[str, str]
    code_blocks: list[CodeBlock]


def preprocess_docx(src: Path, work: Path, debug_dir: Path | None) -> Preprocessed:
    with zipfile.ZipFile(src) as zin:
        doc_xml = zin.read("word/document.xml")
        try:
            styles_xml = zin.read("word/styles.xml")
        except KeyError:
            styles_xml = None
        names = zin.namelist()
        others = {n: zin.read(n) for n in names if n != "word/document.xml"}

    styles = Styles(styles_xml)
    tree = etree.fromstring(doc_xml)
    body = tree.find("w:body", NS)
    if body is None:
        raise SystemExit("ERROR: word/document.xml has no body")

    entries = parse_toc(body, styles)
    if not entries:
        raise SystemExit("ERROR: no table of contents found in the document")
    remove_toc(body, styles)
    for p in list(body.iter(w("p"))):
        strip_edge_breaks(p)
    code_blocks = collapse_code_regions(body)
    titles = normalize_headings(body, entries, styles)
    remove_empty_headings(body, styles)
    mark_indentation(body, styles)

    new_xml = etree.tostring(tree, xml_declaration=True, encoding="UTF-8", standalone=True)
    if debug_dir:
        (debug_dir / "document.preprocessed.xml").write_bytes(new_xml)
    out = work / "preprocessed.docx"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in names:
            zout.writestr(n, new_xml if n == "word/document.xml" else others[n])
    return Preprocessed(out, entries, titles, code_blocks)


# ---------------------------------------------------------------------------
# pandoc AST building blocks
# ---------------------------------------------------------------------------

BLOCK_TYPES = {
    "Plain", "Para", "LineBlock", "CodeBlock", "RawBlock", "BlockQuote", "OrderedList",
    "BulletList", "DefinitionList", "Header", "HorizontalRule", "Table", "Figure", "Div",
}
INLINE_TYPES = {
    "Str", "Emph", "Underline", "Strong", "Strikeout", "Superscript", "Subscript", "SmallCaps",
    "Quoted", "Cite", "Code", "Space", "SoftBreak", "LineBreak", "Math", "RawInline", "Link",
    "Image", "Note", "Span",
}


def walk(node, block_fn=None, inline_fn=None):
    """Rebuild an AST fragment recursively; fn(elem) may return None (keep as-is), a dict, or a list."""
    if isinstance(node, list):
        out = []
        for item in node:
            if isinstance(item, dict) and "t" in item:
                fn = None
                if block_fn and item["t"] in BLOCK_TYPES:
                    fn = block_fn
                elif inline_fn and item["t"] in INLINE_TYPES:
                    fn = inline_fn
                res = fn(item) if fn else None
                if res is None:
                    out.append(walk(item, block_fn, inline_fn))
                elif isinstance(res, list):
                    out.extend(walk_children(r, block_fn, inline_fn) for r in res)
                else:
                    out.append(walk_children(res, block_fn, inline_fn))
            else:
                out.append(walk(item, block_fn, inline_fn))
        return out
    if isinstance(node, dict):
        return {k: walk(v, block_fn, inline_fn) for k, v in node.items()}
    return node


def walk_children(elem, block_fn, inline_fn):
    return {k: walk(v, block_fn, inline_fn) for k, v in elem.items()}


def inlines_text(inlines) -> str:
    out = []
    for il in inlines:
        t, c = il["t"], il.get("c")
        if t == "Str":
            out.append(c)
        elif t in ("Space", "SoftBreak", "LineBreak"):
            out.append(" ")
        elif t in ("Emph", "Strong", "Underline", "Strikeout", "SmallCaps", "Superscript", "Subscript"):
            out.append(inlines_text(c))
        elif t in ("Span", "Link", "Image", "Quoted", "Cite"):
            out.append(inlines_text(c[1]))
        elif t in ("Code", "Math"):
            out.append(c[1])
    return "".join(out)


def block_text(block) -> str:
    t = block["t"]
    if t in ("Para", "Plain"):
        return inlines_text(block["c"])
    if t == "Header":
        return inlines_text(block["c"][2])
    return ""


def header(level: int, inlines) -> dict:
    return {"t": "Header", "c": [level, ["", [], []], inlines]}


def para(inlines) -> dict:
    return {"t": "Para", "c": inlines}


def str_inlines(text: str) -> list:
    out = []
    for i, word_ in enumerate(text.split(" ")):
        if i:
            out.append({"t": "Space"})
        if word_:
            out.append({"t": "Str", "c": word_})
    return out


def link(text: str, url: str) -> dict:
    return {"t": "Link", "c": [["", [], []], str_inlines(text), [url, ""]]}


def bullet_list(items: list[list]) -> dict:
    return {"t": "BulletList", "c": items}


def github_slug(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r"[^\w\- ]", "", s)
    return s.replace(" ", "-")


def file_slug(text: str) -> str:
    s = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "section"


# ---------------------------------------------------------------------------
# chapters, pages and sections
# ---------------------------------------------------------------------------


@dataclass
class Section:
    anchor: str
    level: int
    title: str
    blocks: list  # the Header always sits at index 0


@dataclass
class Page:
    section: Section
    subs: list[Section] = field(default_factory=list)
    path: Path | None = None


@dataclass
class Chapter:
    section: Section
    pages: list[Page] = field(default_factory=list)
    subs: list[Section] = field(default_factory=list)  # deeper sections that don't belong to any page
    path: Path | None = None  # index.md when the chapter has pages, otherwise its own file
    dir: Path | None = None


def split_sections(blocks: list, entries: list[TocEntry], titles: dict[str, str]):
    by_anchor = {e.anchor: e for e in entries}
    marker_idx = []
    for i, b in enumerate(blocks):
        m = SECTION_RE.match(block_text(b).strip()) if b["t"] in ("Para", "Plain") else None
        if m:
            marker_idx.append((i, m.group(1)))
    front = blocks[: marker_idx[0][0]] if marker_idx else blocks
    sections: list[Section] = []
    for n, (i, anchor) in enumerate(marker_idx):
        end = marker_idx[n + 1][0] if n + 1 < len(marker_idx) else len(blocks)
        body = blocks[i + 1:end]
        entry = by_anchor[anchor]
        title = titles.get(anchor, entry.title)
        if body and body[0]["t"] == "Header":
            body[0] = header(entry.level, body[0]["c"][2])
        else:
            warn(f"section {title!r} did not start with a heading; one was synthesized")
            body.insert(0, header(entry.level, str_inlines(title)))
        sections.append(Section(anchor, entry.level, title, body))
    return front, sections


def build_tree(sections: list[Section]) -> list[Chapter]:
    chapters: list[Chapter] = []
    for s in sections:
        if s.level <= 1 or not chapters:
            if s.level > 1:
                warn(f"section {s.title!r} (level {s.level}) appears before any chapter; treated as a chapter")
            chapters.append(Chapter(s))
        elif s.level == 2:
            chapters[-1].pages.append(Page(s))
        else:
            ch = chapters[-1]
            if ch.pages:
                ch.pages[-1].subs.append(s)
            else:
                ch.subs.append(s)
    return chapters


def assign_paths(chapters: list[Chapter]) -> None:
    used_root: set[str] = {"index", "readme", "license"}
    for ch in chapters:
        slug = unique(file_slug(ch.section.title), used_root)
        if ch.pages:
            ch.dir = Path(slug)
            ch.path = ch.dir / "index.md"
            used: set[str] = {"index"}
            for pg in ch.pages:
                pg.path = ch.dir / f"{unique(file_slug(pg.section.title), used)}.md"
        else:
            ch.path = Path(f"{slug}.md")


def unique(slug: str, used: set[str]) -> str:
    candidate, n = slug, 2
    while candidate in used:
        candidate = f"{slug}-{n}"
        n += 1
    used.add(candidate)
    return candidate


# ---------------------------------------------------------------------------
# markdown generation
# ---------------------------------------------------------------------------


class Renderer:
    def __init__(self, api_version, code_blocks: list[CodeBlock], images: dict[str, str]):
        self.api_version = api_version
        self.code_blocks = code_blocks
        self.images = images  # url from the docx -> file name under images/
        self.anchor_targets: dict[str, tuple[Path, str | None]] = {}

    # -- one cleanup pass over the entire AST ---------------------

    def clean(self, blocks: list) -> list:
        def block_fn(b):
            if b["t"] in ("BulletList", "OrderedList"):
                return tight_list(b)
            if b["t"] in ("Para", "Plain"):
                m = CODE_RE.match(block_text(b).strip())
                if m:
                    cb = self.code_blocks[int(m.group(1))]
                    classes = [cb.lang] if cb.lang else []
                    return {"t": "CodeBlock", "c": [["", classes, []], cb.text]}
                linked = link_vocabulary_term(b)
                if linked is not None:
                    return linked
            return None

        def inline_fn(il):
            if il["t"] == "Span" and not il["c"][1]:
                return []
            if il["t"] == "Str":
                m = INDENT_RE.match(il["c"])
                if m:
                    out = [{"t": "RawInline", "c": ["html", "&nbsp;" * int(m.group(1))]}]
                    if m.group(2):
                        out.append({"t": "Str", "c": m.group(2).replace(NBSP, " ")})
                    return out
                if NBSP in il["c"]:  # leftover non-breaking spaces in running text become regular spaces
                    return {"t": "Str", "c": il["c"].replace(NBSP, " ")}
            if il["t"] == "Image":
                attr, alt, (url, title) = il["c"]
                if WORD_AUTO_ALT_RE.search(inlines_text(alt)):
                    alt = []
                return {"t": "Image", "c": [["", [], []], alt, [url, title]]}
            return None

        return walk(group_term_lists(group_path_lists(blocks)), block_fn, inline_fn)

    # -- rendering a single page --------------------------------------------------

    def to_markdown(self, blocks: list, page_path: Path) -> str:
        depth = len(page_path.parent.parts)
        prefix = "../" * depth

        def inline_fn(il):
            if il["t"] == "Image":
                attr, alt, (url, title) = il["c"]
                name = self.images.get(url)
                if name:
                    return {"t": "Image", "c": [attr, alt, [f"{prefix}images/{name}", title]]}
            if il["t"] == "Link":
                attr, inl, (url, title) = il["c"]
                if url.startswith("#") and url[1:] in self.anchor_targets:
                    target, frag = self.anchor_targets[url[1:]]
                    rel = relative_link(page_path, target)
                    return {"t": "Link", "c": [attr, inl, [rel + (f"#{frag}" if frag else ""), title]]}
            return None

        blocks = walk(blocks, None, inline_fn)
        doc = {"pandoc-api-version": self.api_version, "meta": {}, "blocks": blocks}
        md = pypandoc.convert_text(json.dumps(doc), "gfm", format="json", extra_args=["--wrap=none"])
        return tidy_markdown(md)

    def page_blocks(self, title: str, body: list, subs: list[Section]) -> list:
        """The title becomes the H1; remaining headings are shifted so the highest sub-level lands at H2."""
        rest = list(body)
        for s in subs:
            rest.extend(s.blocks)
        levels = [b["c"][0] for b in rest if b["t"] == "Header"]
        base = min(levels) if levels else 2

        def block_fn(b):
            if b["t"] == "Header":
                lvl, attr, inl = b["c"]
                return {"t": "Header", "c": [min(6, lvl - base + 2), attr, inl]}
            return None

        return [header(1, str_inlines(title))] + walk(rest, block_fn, None)


def tidy_markdown(md: str) -> str:
    """Light touch-ups on pandoc's GFM: ```lang fences and short --- rules."""
    lines = []
    in_fence = False
    for line in md.split("\n"):
        m = re.match(r"^(\s*)(`{3,}|~{3,})\s*(\S*)\s*$", line)
        if m:
            in_fence = not in_fence
            line = f"{m.group(1)}{m.group(2)}{m.group(3)}"
        elif not in_fence and re.fullmatch(r"-{3,}", line.strip()):
            line = "---"
        lines.append(line)
    return "\n".join(lines).strip("\n") + "\n"


def indent_parts(inlines):
    """Split a leading @@INDENT@@ marker off a paragraph -> (marker inline or None, remaining inlines)."""
    if inlines and inlines[0]["t"] == "Str":
        m = INDENT_RE.match(inlines[0]["c"])
        if m:
            rest = ([{"t": "Str", "c": m.group(2)}] if m.group(2) else []) + inlines[1:]
            return {"t": "Str", "c": INDENT_MARK.format(int(m.group(1)))}, rest
    return None, inlines


def plain_text(inlines) -> str:
    return inlines_text(inlines).replace(NBSP, " ").strip()


def link_term(inlines):
    """`bf:term` / `bflc:Term` -> link to the ontology anchor, unless already linked.

    Properties (lower-case initial) use the page's #p_ anchors, classes
    (upper-case initial) use #c_.
    """
    m = TERM_RE.match(plain_text(inlines))
    if not m or '"t": "Link"' in json.dumps(inlines):
        return inlines
    prefix, name = m.group(1), m.group(2)
    url = f"{ONTOLOGY_URL[prefix]}#{'c' if name[0].isupper() else 'p'}_{name}"
    return [{"t": "Link", "c": [["", [], []], inlines, [url, ""]]}]


def link_vocabulary_term(b: dict):
    """Indented paragraph that is just a vocabulary term -> linked (see link_term)."""
    marker, rest = indent_parts(b["c"])
    if marker is None:
        return None
    linked = link_term(rest)
    if linked is rest:
        return None
    return {"t": b["t"], "c": [marker] + linked}


def is_term_line(b: dict) -> bool:
    if b["t"] not in ("Para", "Plain"):
        return False
    marker, rest = indent_parts(b["c"])
    return marker is not None and bool(TOKEN_RE.match(plain_text(rest)))


def tight_list(b: dict) -> dict:
    """Word lists reach us loose (a Para per item, which renders as <li><p>); make them tight.

    Only the first block of an item decides tightness for pandoc, so that one
    becomes Plain and anything else in the item (nested lists, extra
    paragraphs) is left alone.
    """
    items = b["c"] if b["t"] == "BulletList" else b["c"][1]
    items = [
        [{"t": "Plain", "c": item[0]["c"]}] + item[1:] if item and item[0]["t"] == "Para" else item
        for item in items
    ]
    if b["t"] == "BulletList":
        return {"t": "BulletList", "c": items}
    return {"t": "OrderedList", "c": [b["c"][0], items]}


def list_style_block(style: str) -> dict:
    return {"t": "RawBlock", "c": ["html", LIST_STYLE_MARK.format(style)]}


def indent_width(inlines) -> int:
    """Width of a leading @@INDENT@@ marker, or 0."""
    if inlines and inlines[0]["t"] == "Str":
        m = INDENT_RE.match(inlines[0]["c"])
        if m:
            return int(m.group(1))
    return 0


def is_italic_line(b: dict) -> bool:
    """A paragraph whose entire text is italic (an indent marker may lead it)."""
    if b["t"] not in ("Para", "Plain"):
        return False
    _, rest = indent_parts(b["c"])
    return bool(plain_text(rest)) and all(il["t"] in ("Emph", "Space", "SoftBreak", "LineBreak") for il in rest)


def trim_spaces(inlines: list) -> list:
    while inlines and inlines[0]["t"] in ("Space", "SoftBreak"):
        inlines = inlines[1:]
    while inlines and inlines[-1]["t"] in ("Space", "SoftBreak"):
        inlines = inlines[:-1]
    return inlines


def split_lines(inlines) -> list[list]:
    """Cut inlines into lines at LineBreaks; a break inside an Emph splits it so every line stays italic."""
    lines: list[list] = [[]]
    for il in inlines:
        if il["t"] == "LineBreak":
            lines.append([])
        elif il["t"] == "Emph":
            for n, piece in enumerate(split_lines(il["c"])):
                if n:
                    lines.append([])
                lines[-1].append({"t": "Emph", "c": piece})
        else:
            lines[-1].append(il)
    return [trim_spaces(line) for line in lines if plain_text(line)]


def ends_in_class(inlines) -> bool:
    return bool(CLASS_PATH_RE.search(BRACKET_RE.sub("", plain_text(inlines)).strip()))


def path_indents(lines: list[tuple[int, list]]) -> list[int]:
    """Indent for each (docx indent, inlines) line of a page-top path list.

    A line ending in a class opens a group: the lines after it, up to the next
    class line, are indented one step below it. Indentation typed into the
    docx is kept where it is deeper than that.
    """
    indents = []
    parent = None
    for own, inlines in lines:
        if ends_in_class(inlines):
            parent = own
            indents.append(own)
        else:
            indents.append(max(own, parent + TAB_SPACES if parent is not None else 0))
    return indents


def group_path_lists(blocks: list) -> list:
    """Italic lines directly under a page heading -> LIST_STYLE marker + tight bullet list.

    These are the property paths that open the common-properties pages
    (bf:language/bf:Language, ...). One item per line, indented per
    path_indents and carried as an indent marker.
    """
    out: list = []
    i = 0
    while i < len(blocks):
        b = blocks[i]
        out.append(b)
        i += 1
        if b["t"] != "Header" or b["c"][0] not in PAGE_HEADING_LEVELS:
            continue
        run = []
        while i < len(blocks) and is_italic_line(blocks[i]):
            run.append(blocks[i])
            i += 1
        if not run:
            continue
        base = min(indent_width(p["c"]) for p in run)
        lines = [(indent_width(p["c"]) - base, line) for p in run for line in split_lines(indent_parts(p["c"])[1])]
        items = []
        for indent, (_, line) in zip(path_indents(lines), lines):
            prefix = [{"t": "Str", "c": INDENT_MARK.format(indent)}] if indent else []
            items.append([{"t": "Plain", "c": prefix + link_term(line)}])
        out.append(list_style_block(PATH_LIST_STYLE))
        out.append(bullet_list(items))
    return out


def group_term_lists(blocks: list) -> list:
    """Runs of 2+ consecutive indented single-token lines -> LIST_STYLE marker + tight bullet list."""
    out: list = []
    run: list = []

    def flush():
        if len(run) >= 2:
            items = [[{"t": "Plain", "c": link_term(indent_parts(b["c"])[1])}] for b in run]
            out.append(list_style_block(TERM_LIST_STYLE))
            out.append(bullet_list(items))
        else:
            out.extend(run)
        run.clear()

    for b in blocks:
        if is_term_line(b):
            run.append(b)
            continue
        flush()
        t = b["t"]
        if t == "BlockQuote":
            b = {"t": t, "c": group_term_lists(b["c"])}
        elif t == "Div":
            b = {"t": t, "c": [b["c"][0], group_term_lists(b["c"][1])]}
        elif t == "BulletList":
            b = {"t": t, "c": [group_term_lists(item) for item in b["c"]]}
        elif t == "OrderedList":
            b = {"t": t, "c": [b["c"][0], [group_term_lists(item) for item in b["c"][1]]]}
        elif t == "Figure":
            b = {"t": t, "c": [b["c"][0], b["c"][1], group_term_lists(b["c"][2])]}
        out.append(b)
    flush()
    return out


def relative_link(from_path: Path, to_path: Path) -> str:
    start = from_path.parent.as_posix() or "."
    return Path(os.path.relpath(to_path.as_posix(), start)).as_posix()


def nav_order_block(entries: list[str]) -> dict:
    """Builds the <!-- NAV_ORDER ... --> comment: entries are file names for pages, directory names for chapters."""
    body = "\n".join([NAV_ORDER_TAG, *entries])
    return {"t": "RawBlock", "c": ["html", f"<!--\n{body}\n-->"]}


def nav_blocks(page_path: Path, prev, nxt, back: bool) -> list:
    """The page footer: a rule, a back-to-TOC link, and then previous/next links following reading order."""
    blocks = [{"t": "HorizontalRule"}]
    if back:
        blocks.append(para([link(BACK_LINK_TEXT, relative_link(page_path, Path("index.md")))]))
    nav = []
    if prev:
        nav.append(link(f"{PREV_LINK_TEXT}: {prev[0]}", relative_link(page_path, prev[1])))
    if nxt:
        if nav:
            nav.extend([{"t": "Space"}, {"t": "RawInline", "c": ["html", "|"]}, {"t": "Space"}])
        nav.append(link(f"{NEXT_LINK_TEXT}: {nxt[0]}", relative_link(page_path, nxt[1])))
    if nav:
        blocks.append(para(nav))
    return blocks


def toc_list(chapters: list[Chapter], from_path: Path, only: Chapter | None = None) -> dict:
    """A nested bullet list that mirrors the docx TOC (chapters > pages > headings within a page)."""

    def sub_items(page: Page):
        items = []
        used: dict[str, int] = {}
        for s in page.subs:
            slug = github_slug(s.title)
            n = used.get(slug, 0)
            used[slug] = n + 1
            frag = f"{slug}-{n}" if n else slug
            items.append([{"t": "Plain", "c": [link(s.title, relative_link(from_path, page.path) + "#" + frag)]}])
        return items

    def page_items(ch: Chapter):
        items = []
        for pg in ch.pages:
            item = [{"t": "Plain", "c": [link(pg.section.title, relative_link(from_path, pg.path))]}]
            subs = sub_items(pg)
            if subs:
                item.append(bullet_list(subs))
            items.append(item)
        return items

    if only is not None:
        return bullet_list(page_items(only))
    items = []
    for ch in chapters:
        item = [{"t": "Plain", "c": [link(ch.section.title, relative_link(from_path, ch.path))]}]
        pages = page_items(ch)
        if pages:
            item.append(bullet_list(pages))
        items.append(item)
    return bullet_list(items)


def render_all(front: list, chapters: list[Chapter], r: Renderer) -> dict[Path, str]:
    files: dict[Path, str] = {}

    # where every anchor landed (file + heading) so in-document links can be fixed up
    for ch in chapters:
        r.anchor_targets[ch.section.anchor] = (ch.path, None)
        for s in ch.subs:
            r.anchor_targets[s.anchor] = (ch.path, github_slug(s.title))
        for pg in ch.pages:
            r.anchor_targets[pg.section.anchor] = (pg.path, None)
            for s in pg.subs:
                r.anchor_targets[s.anchor] = (pg.path, github_slug(s.title))

    # the top-level index page: intro material (images, title, description) plus the TOC
    index_path = Path("index.md")
    images = []

    def collect_images(il):
        if il["t"] == "Image":
            images.append(il)
        return None

    walk(front, None, collect_images)
    title = next((block_text(b) for b in front if b["t"] == "Header" and block_text(b).strip()), None)
    title = clean_title(title) if title else "Index"
    description = [b for b in front if b["t"] != "Header" and block_text(b).strip()]

    # pages in reading order for prev/next links: the index first, then each chapter followed by its pages
    order: list[tuple[str, Path]] = [(title, index_path)]
    for ch in chapters:
        order.append((ch.section.title, ch.path))
        for pg in ch.pages:
            order.append((pg.section.title, pg.path))
    position = {path: i for i, (_, path) in enumerate(order)}

    def nav(path: Path) -> list:
        i = position[path]
        prev = order[i - 1] if i > 0 else None
        nxt = order[i + 1] if i + 1 < len(order) else None
        return nav_blocks(path, prev, nxt, back=path != index_path)

    blocks = [para([img]) for img in images]
    blocks.append(header(1, str_inlines(title)))
    blocks.extend(description)
    blocks.append({"t": "HorizontalRule"})
    blocks.append(header(2, str_inlines("Table of Contents")))
    blocks.append(toc_list(chapters, index_path))
    root_order = [index_path.name] + [(ch.dir or ch.path).name for ch in chapters]
    blocks += nav(index_path) + [nav_order_block(root_order)]
    files[index_path] = r.to_markdown(blocks, index_path)

    for ch in chapters:
        sec = ch.section
        blocks = r.page_blocks(sec.title, sec.blocks[1:], ch.subs)
        if ch.pages:
            blocks.append(header(2, str_inlines("Contents")))
            blocks.append(toc_list(chapters, ch.path, only=ch))
        blocks += nav(ch.path)
        if ch.pages:
            blocks.append(nav_order_block([ch.path.name] + [pg.path.name for pg in ch.pages]))
        files[ch.path] = r.to_markdown(blocks, ch.path)
        for pg in ch.pages:
            blocks = r.page_blocks(pg.section.title, pg.section.blocks[1:], pg.subs)
            files[pg.path] = r.to_markdown(blocks + nav(pg.path), pg.path)
    return files


# ---------------------------------------------------------------------------
# writing files to disk
# ---------------------------------------------------------------------------


def remove_previous_output(out_root: Path, manifest: Path) -> None:
    if not manifest.exists():
        return
    dirs = set()
    for line in manifest.read_text(encoding="utf-8").splitlines():
        rel = line.strip()
        if not rel:
            continue
        p = out_root / rel
        if p.is_file():
            p.unlink()
        dirs.add(p.parent)
    for d in sorted(dirs, key=lambda x: len(x.parts), reverse=True):
        while d != out_root and d.exists() and not any(d.iterdir()):
            d.rmdir()
            d = d.parent


def write_output(out_root: Path, files: dict[Path, str], images: dict[Path, bytes], manifest: Path) -> None:
    remove_previous_output(out_root, manifest)
    written = []
    for rel, content in files.items():
        p = out_root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8", newline="\n")
        written.append(rel.as_posix())
    for rel, data in images.items():
        p = out_root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        written.append(rel.as_posix())
    manifest.write_text("\n".join(sorted(written)) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# command-line entry point
# ---------------------------------------------------------------------------


def find_default_docx() -> Path:
    candidates = sorted(META_DIR.glob("*.docx"))
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        raise SystemExit(f"ERROR: no .docx found in {META_DIR}; pass the path explicitly")
    names = "\n  ".join(c.name for c in candidates)
    raise SystemExit(f"ERROR: several .docx files in {META_DIR}; pass one explicitly:\n  {names}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("docx", nargs="?", type=Path, help="source .docx (default: the one in meta-conversion/)")
    ap.add_argument("--out", type=Path, default=REPO_ROOT, help="output root (default: repository root)")
    ap.add_argument("--debug-dir", type=Path, help="write intermediate files (patched XML, AST) here")
    args = ap.parse_args(argv)

    src = (args.docx or find_default_docx()).resolve()
    out_root = args.out.resolve()
    debug_dir = args.debug_dir.resolve() if args.debug_dir else None
    if debug_dir:
        debug_dir.mkdir(parents=True, exist_ok=True)
    print(f"source : {src}")
    print(f"output : {out_root}")
    print(f"pandoc : {pypandoc.get_pandoc_version()} (pypandoc {pypandoc.__version__})")

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        pre = preprocess_docx(src, work, debug_dir)
        media_dir = work / "media"
        ast_json = pypandoc.convert_file(
            str(pre.docx_path), "json", format="docx",
            extra_args=["--extract-media", str(media_dir)],
        )
        if debug_dir:
            (debug_dir / "ast.json").write_text(ast_json, encoding="utf-8")
        ast = json.loads(ast_json)

        # pandoc keeps the docx media file names when extracting (image1.png, ...)
        image_files: dict[Path, bytes] = {}
        url_to_name: dict[str, str] = {}

        def collect(il):
            if il["t"] == "Image":
                url = il["c"][2][0]
                p = Path(url)
                if p.is_file():
                    url_to_name[url] = p.name
                    image_files[Path("images") / p.name] = p.read_bytes()
                else:
                    warn(f"image not found on disk: {url}")
            return None

        walk(ast["blocks"], None, collect)

        renderer = Renderer(ast["pandoc-api-version"], pre.code_blocks, url_to_name)
        blocks = renderer.clean(ast["blocks"])
        front, sections = split_sections(blocks, pre.entries, pre.titles)
        chapters = build_tree(sections)
        assign_paths(chapters)
        files = render_all(front, chapters, renderer)

    manifest = (META_DIR if out_root == REPO_ROOT else out_root) / MANIFEST_NAME
    write_output(out_root, files, image_files, manifest)
    print(f"wrote {len(files)} markdown files and {len(image_files)} images; manifest: {manifest}")
    for ch in chapters:
        print(f"  {ch.path}")
        for pg in ch.pages:
            print(f"    {pg.path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
