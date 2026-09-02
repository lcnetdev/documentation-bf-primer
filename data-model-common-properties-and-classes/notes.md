# Notes

<!-- LIST_STYLE: compact single-column no-bullet -->

- *bf:note/b:Note\[rdf:type=”http://id.loc.gov/vocabulary/mnotetype...”\]*

Any BIBFRAME resource may express a note via the object property bf:note (expected value bf:Note). The content of the note is typically expressed in an rdfs:label. It is possible to more specifically identify notes by employing the use of rdf:type and a value from the [Note Type](http://id.loc.gov/vocabulary/mnotetype) list at ID.LOC.GOV. When notes are not specifically identified, they can be interpreted to be general notes of the resource with which the note is associated.

Example (no note type): <https://id.loc.gov/resources/instances/20709686.html>

This is a general note about the Instance.

```xml
<rdf:RDF>
  <bf:Instance rdf:about="http://id.loc.gov/resources/instances/20709686">
    <bf:note>
      <bf:Note>
        <rdfs:label>Regional road map with tourist features.</rdfs:label>
      </bf:Note>
    </bf:note>
  </bf:Instance>
</rdf:RDF>
```

Example (note type expressed by property rdf:type with a value from the Note Type list): <https://id.loc.gov/resources/works/17800318.html>

And a note about an award the Work earned.

```xml
<rdf:RDF>
  <bf:Work rdf:about="http://id.loc.gov/resources/works/17800318">
    <bflc:aap>The office. The complete series one &amp; two and the special</bflc:aap>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/MovingImage"/>
    <bf:note>
      <bf:Note>
        <rdf:type rdf:resource="http://id.loc.gov/vocabulary/mnotetype/award"/>
        <rdfs:label>Peabody Award, 2004.</rdfs:label>
      </bf:Note>
    </bf:note>
  <bf:Work>
</rdf:RDF>
```

---

[Back to Table of Contents](../index.md)

[Previous Page: Language](language.md) | [Next Page: Provision Activity](provision-activity.md)
