# Namespaces and Examples

Most of the examples in this guide are presented using the RDF/XML serialization. XML element names use defined prefixes that map to namespaces.

Most namespace declarations are omitted from the examples for brevity and clarity. Generally, these namespaces would be declared as in the following RDF/XML document node:

```xml
<rdf:RDF
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" xmlns:bf="http://id.loc.gov/ontologies/bibframe/" xmlns:bflc="http://id.loc.gov/ontologies/bflc/" xmlns:madsrdf="http://www.loc.gov/mads/rdf/v1#"
    />
```

Nearly all of the BIBFRAME Classes and Properties are expressed in the main BIBFRAME namespace: http://id.loc.gov/ontologies/bibframe/

But a number of auxiliary Class lists are used. These are published at ID.LOC.GOV, often with a declared association with a “parent” BIBFRAME Class. For example, the Relators entity for “author” (<http://id.loc.gov/vocabulary/relators/aut>) is declared a type of bf:Role. This makes it clear that any resource in the Relators dataset is usable as a Role in BIBFRAME.

```xml
<rdf:RDF>
  <madsrdf:Authority rdf:about="http://id.loc.gov/vocabulary/relators/aut">
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Role"/>
    <madsrdf:authoritativeLabel>author</madsrdf:authoritativeLabel>
  </madsrdf:Authority>
</rdf:RDF>
```

## BFLC

The Library of Congress has an extension ontology (BFLC) that is used for testing and review of potential additions to the main BIBFRAME ontology. For example, the agent subclass bf:PrimaryContribution was originally a BFLC class and was moved to the BIBFRAME ontology based on user feedback. The BFLC ontology is also used for LC-specific local data elements. The below example features bflc:aap, which is merely a convenient label generated programmatically. This property has been included in a number of examples below merely to provide a succinct description of what the example Work is.

```xml
<rdf:RDF>
  <bf:Work rdf:about="http://id.loc.gov/resources/hubs/ca6d97b4-923a-b178-6723-d55a4eb236a7">
    <bflc:aap>Dvořák, Antonín, 1841-1904. Symphonies, no. 9, op. 95, E minor</bflc:aap>
  </bf:Work>
</rdf:RDF>
```

## Examples

Typically, BIBFRAME resources tend to be small graphs of information containing ample information to describe a Work or Instance. Examples in this document are focused on a specific detail about the model and/or vocabulary and will therefore often be severely truncated for brevity and clarity.

Full BIBFRAME examples are available from the Library of Congress’s Linked Data Service (<http://id.loc.gov/>).

---

[Back to Table of Contents](../index.md)

[Previous Page: Status of this document](status-of-this-document.md) | [Next Page: Organization and Abbreviations](organization-and-abbreviations.md)
