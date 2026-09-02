# Language

*bf:language/bf:Language*

*bf:accompaniedBy/bf:Work/bf:language*

*bf:note/bf:Note\[type=Language\]/bf:language*

Ideally, one has a resource and it is in one or more languages. And that is precisely the pattern/model that BIBFRAME naturally supports.

```xml
<rdf:RDF>
  <bf:Work rdf:about="http://id.loc.gov/resources/works/1190085">
    <bflc:aap>Eco, Umberto. Il nome della rosa</bflc:aap>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Text"/>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Monograph"/>
    <bf:language rdf:resource="http://id.loc.gov/vocabulary/languages/ita"/>
    <bf:contribution>
      <bf:Contribution>
        <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/PrimaryContribution"/>
        <bf:agent rdf:resource="http://id.loc.gov/rwo/agents/n79021285"/>
        <bf:role rdf:resource="http://id.loc.gov/vocabulary/relators/aut"/>
      </bf:Contribution>
    </bf:contribution>
    <bf:title>
      <bf:Title>
        <bf:mainTitle>Il nome della rosa</bf:mainTitle>
        <bflc:nonSortNum>3</bflc:nonSortNum>
      </bf:Title>
    </bf:title>
  </bf:Work>
</rdf:RDF>
```

Another basic example: <https://id.loc.gov/resources/works/22320252.html>

```xml
<rdf:RDF>
  <bf:Work rdf:about="http://id.loc.gov/resources/works/22320252">
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Text"/>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Monograph"/>
    <bf:language rdf:resource="http://id.loc.gov/vocabulary/languages/eng"/>
  </bf:Work>
</rdf:RDF>
```

## Implementation consideration: Handling language information from MARC

In addition to the expected method of recording language for a resource (as seen above), conversion from MARC (and back to MARC, if desired) required two additional methods, one of which basically aligns with the expected method and the second of which is quite distinct from the expected method.

MARC 041, which is used to record language information, supports a wide range of subfields. Some of those subfields relate to the resource in hand, some refer to related resources, and some can be interpreted as notes. For those that relate to the resource in hand, language recordation is handled as seen in the example above, the expected method. If, however, the subfield can be interpreted as a reference to a related resource, then the related resource should be modelled as best possible and the language information associated with the related resource.

Example (of a Work with libretto in Italian, sung or spoken text in German and Italian, and accompanying material in German and English): <https://id.loc.gov/resources/works/20453267.html>

```xml
<rdf:RDF>
  <bf:Work rdf:about="http://id.loc.gov/resources/works/20453267">
    <bflc:aap>Jubilee edition</bflc:aap>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/MusicAudio"/>
    <bf:language rdf:resource="http://id.loc.gov/vocabulary/languages/ita"/>
    <bf:accompaniedBy>
      <bf:Work>
            <rdf:type rdf:resource="http://id.loc.gov/vocabulary/resourceComponents/lib"/>
            <bf:language rdf:resource="http://id.loc.gov/vocabulary/languages/ita"/>
      </bf:Work>
    </bf:accompaniedBy>
    <bf:accompaniedBy>
      <bf:Work>
            <rdf:type rdf:resource="http://id.loc.gov/vocabulary/resourceComponents/stx"/>
            <bf:language rdf:resource="http://id.loc.gov/vocabulary/languages/ita"/>
      </bf:Work>
    </bf:accompaniedBy>
    <bf:accompaniedBy>
      <bf:Work>
            <rdf:type rdf:resource="http://id.loc.gov/vocabulary/resourceComponents/stx"/>
            <bf:language rdf:resource="http://id.loc.gov/vocabulary/languages/ger"/>
      </bf:Work>
    </bf:accompaniedBy>
    <bf:accompaniedBy>
      <bf:Work>
            <rdf:type rdf:resource="http://id.loc.gov/vocabulary/resourceComponents/amt"/>
            <bf:language rdf:resource="http://id.loc.gov/vocabulary/languages/ger"/>
      </bf:Work>
    </bf:accompaniedBy>
    <bf:accompaniedBy>
      <bf:Work>
            <rdf:type rdf:resource="http://id.loc.gov/vocabulary/resourceComponents/amt"/>
            <bf:language rdf:resource="http://id.loc.gov/vocabulary/languages/eng"/>
      </bf:Work>
    </bf:accompaniedBy>
  </bf:Work>
</rdf:RDF>
```

The above represents five related resources of the bf:Work being described. bf:accompaniedBy has been used as the relationship, on the assumption that the related pieces can be reasonably considered “accompanying material.” They have each been modeled as a bf:Work, with a specific resource type (“libretto” for the first; two copies of the “sung or spoken text;” and finally some kind of generic accompanied material, each in a different language). A bf:language property, indicating the appropriate language of the extra piece, identifies the language.

The second method, the one that breaks notably from the expected way to handle language, treats some of the language information from the original MARC record as a note.

Example (of a translated Work whose original language – the ‘otx’ type below - is recorded as a note): <https://id.loc.gov/resources/works/19052646.html>

```xml
<rdf:RDF>
  <bf:Work rdf:about="http://id.loc.gov/resources/works/19052646">
    <bflc:aap>Ferrante, Elena. The story of the lost child</bflc:aap>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Text"/>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Monograph"/>
    <bf:language rdf:resource="http://id.loc.gov/vocabulary/languages/eng"/>
    <bf:note>
      <bf:Note>
        <!-- Original language: Italian -->
        <rdf:type rdf:resource="http://id.loc.gov/vocabulary/resourceComponents/otx"/>
        <bf:language rdf:resource="http://id.loc.gov/vocabulary/languages/ita"/>
      </bf:Note>
    </bf:note>
  </bf:Work>
</rdf:RDF>
```

In this situation, instead of attempting to model the reference as a related resource, the information from MARC – that the original language of the translation being described - is treated as note of the bf:Work. While it is logically possible to model this as a related resource (i.e. Work isTranslationOf Work), there is a reasonable likelihood that a more formal relationship to the original Work/text exists in the record (or could) and there is no need to risk creating a duplicate Work resource for the original. Also, consistency is important: a group of subfields could be identified as “accompanying material” and another as “notes,” simplifying the logic about how to handle this from the perspective of conversion.

---

[Back to Table of Contents](../index.md)

[Previous Page: Identifiers](identifiers.md) | [Next Page: Notes](notes.md)
