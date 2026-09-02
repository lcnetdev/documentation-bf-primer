# Identifiers

*bf:identifiedBy/bf:Identifier*

<!-- LIST_STYLE: compact two-column -->

- *rdf:value*
- [*bf:qualifier*](https://id.loc.gov/ontologies/bibframe.html#p_qualifier)
- [*bf:status*](https://id.loc.gov/ontologies/bibframe.html#p_status)

A BIBFRAME resource may have several identifiers. An Instance may have, for example, an ISBN, and a Work might have an ISSN or cluster ISSN, such as an ISSN-H. In bibliographic description, most Identifiers are associated with specific Instances or are part of administrative metadata.

Since it is imperative to know the type of identifier, bf:Identifier is subclassed nearly 50 times in the BIBFRAME vocabulary. Additionally, implementers may choose any of the values from the [Standard Identifiers Scheme](http://id.loc.gov/vocabulary/identifiers) list at ID.LOC.GOV, all of which are of type bf:Identifier and can be used with BIBFRAME.

1)  Type Indicated by BIBFRAME Class

Example (bf:Lccn subclass): <https://id.loc.gov/resources/instances/23423612.html>

```xml
<rdf:RDF>
  <bf:Instance rdf:about="http://id.loc.gov/resources/instances/23423612">
    <bf:identifiedBy>
      <bf:Lccn>
        <rdf:value>  2023281062</rdf:value>
      </bf:Lccn>
    </bf:identifiedBy>
  </bf:Instance>
</rdf:RDF>
```

Example (bf:Isbn subclass with added bf:qualifier property): <https://id.loc.gov/resources/instances/23423612.html>

```xml
<rdf:RDF>
  <bf:Instance rdf:about="http://id.loc.gov/resources/instances/23423612">
    <bf:identifiedBy>
      <bf:Isbn>
        <rdf:value>9781524763145</rdf:value>
        <bf:qualifier>paperback</bf:qualifier>
      </bf:Isbn>
    </bf:identifiedBy>
  </bf:Instance>
</rdf:RDF>
```

Example (bf:Isbn subclass with added bf:status resource indicating the identifier is cancelled or invalid): <https://id.loc.gov/resources/instances/23586254.html>

```xml
<rdf:RDF>
  <bf:Instance rdf:about="http://id.loc.gov/resources/instances/23586254">
    <bf:identifiedBy>
      <bf:Isbn>
        <rdf:value>9780593851678</rdf:value>
        <bf:status rdf:resource="http://id.loc.gov/vocabulary/mstatus/cancinv"/>
        <bf:qualifier>epub</bf:qualifier>
      </bf:Isbn>
    </bf:identifiedBy>
  </bf:Instance>
</rdf:RDF>
```

2)  Type indicated by a Standard Identifier class

For identifier types not defined in the BIBFRAME namespace but defined in the Standard Identifier dataset, bf:Identifier is used and the type is indicated by property rdf:type. The example below shows a reference to a MusicBrainz identifier value.

```xml
<rdf:RDF>
  <bf:Instance rdf:about="http://id.loc.gov/resources/instances/20447340">
    <bf:identifiedBy>
      <bf:Identifier>
        <rdf:type rdf:resource="http://id.loc.gov/vocabulary/identifiers/musicb" />
        <rdf:value>9fc8cc73-2e82-4a61-a7a3-441066ef906a</rdf:value>
      </bf:Identifier>
    </bf:identifiedBy>
  </bf:Instance>
</rdf:RDF>
```

---

[Back to Table of Contents](../index.md)

[Previous Page: Contributions and Contributors](contributions-and-contributors.md) | [Next Page: Language](language.md)
