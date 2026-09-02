# Contributions and Contributors

*bf:contribution/bf:Contribution*

&nbsp;&nbsp;&nbsp;&nbsp;*bf:agent/bf:Agent*

&nbsp;&nbsp;&nbsp;&nbsp;*bf:role/bf:Role*

A bf:Contribution is an abstraction resource that mainly allows for the identification of a single Agent and that Agent’s roles with respect to the related resource, such as a bf:Work, bf:Hub, bf:Item, or bf:Instance. Leveraging an abstraction layer makes it possible not only to identify multiple roles the Agent played in the lifecycle of a resource, but also any other information that is specific to the relationship between an Agent and the BIBFRAME resource in question. Consider the following example that captures not only who the actor was but also his role:

```xml
<rdf:RDF>
  <bf:Work rdf:about="http://id.loc.gov/resources/works/22481758">
    <bflc:aap>Unforgiven</bflc:aap>
    <bf:contribution>
      <bf:Contribution>
        <bf:agent rdf:resource="http://id.loc.gov/rwo/agents/n50024426"/>
        <bf:role rdf:resource="http://id.loc.gov/vocabulary/relators/fmd"/>
        <bf:role rdf:resource="http://id.loc.gov/vocabulary/relators/fmp"/>
        <bf:role rdf:resource="http://id.loc.gov/vocabulary/relators/act"/>
        <bf:dramaticRole>William Munny</bf:dramaticRole>
      </bf:Contribution>
    </bf:contribution>
</rdf:RDF>
```

The abstraction leaves additional room for notes or other details that may be desirable to record.

bf:PrimaryContribution is defined as a subclass of bf:Contribution. Identifying a Contribution resource as a bf:PrimaryContribution resource is analogous to Main Entry in MARC, and can be used for contribution resources created from the 100/110/111 MARC fields. Use of this class is important for conversion to and from MARC, and reflects historical cataloging practice, but is not technically required.

Agents also appear in subject resources, but a role is not included.

The Relators dataset, published by the Library of Congress’s Linked Data Service (id.loc.gov), is a list of resources all of which are defined as bf:Role resources and readily usable with the Bibframe model and vocabulary: <https://id.loc.gov/vocabulary/relators.html> In this way, these roles are maintained more as a list that can be added to easily and therefore not embedded in the BIBFRAME vocabulary, which is subject to stricter maintenance rules.

bf:Agent has subclasses:

&nbsp;&nbsp;&nbsp;&nbsp;[bf:Person](https://id.loc.gov/ontologies/bibframe.html#c_Person)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:Family](https://id.loc.gov/ontologies/bibframe.html#c_Family)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:Organization](https://id.loc.gov/ontologies/bibframe.html#c_Organization)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:Jurisdiction](https://id.loc.gov/ontologies/bibframe.html#c_Jurisdiction)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:Meeting](https://id.loc.gov/ontologies/bibframe.html#c_Meeting)

Example (agent and single role): <http://id.loc.gov/resources/works/22481758>

```xml
<rdf:RDF>
  <bf:Work rdf:about="http://id.loc.gov/resources/works/22481758">
    <bflc:aap>Unforgiven</bflc:aap>
    <bf:contribution>
      <bf:Contribution>
        <bf:agent rdf:resource="http://id.loc.gov/rwo/agents/n93002890"/>
        <bf:role rdf:resource="http://id.loc.gov/vocabulary/relators/aus"/>
      </bf:Contribution>
    </bf:contribution>
  </bf:Work>
</rdf:RDF>
```

Example (agent and multiple roles): <https://id.loc.gov/resources/works/19537131.html>

```xml
<rdf:RDF>
  <bf:Work rdf:about="http://id.loc.gov/resources/works/19537131">
    <bflc:aap>Miranda, Lin-Manuel, 1980-. Hamilton : original Broadway cast recording</bflc:aap>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/MusicAudio"/>
    <bf:contribution>
      <bf:Contribution>
        <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/PrimaryContribution"/>
        <bf:agent rdf:resource="http://id.loc.gov/rwo/agents/no2008101876"/>
        <bf:role rdf:resource="http://id.loc.gov/vocabulary/relators/cmp"/>
        <bf:role rdf:resource="http://id.loc.gov/vocabulary/relators/lbt"/>
        <bf:role rdf:resource="http://id.loc.gov/vocabulary/relators/lyr"/>
        <bf:role rdf:resource="http://id.loc.gov/vocabulary/relators/prf"/>
      </bf:Contribution>
    </bf:contribution>
  </bf:Work>
</rdf:RDF>
```

Example (agent as subject and no role): <https://id.loc.gov/resources/works/13291929.html>

```xml
<rdf:RDF>
  <bf:Work rdf:about="http://id.loc.gov/resources/works/13291929">
    <bflc:aap>Spence, Jon. Becoming Jane Austen : a life</bflc:aap>
    <bf:subject>
      <bf:Person rdf:about="http://id.loc.gov/rwo/agents/n79032879">
        <rdfs:label>Austen, Jane, 1775-1817</rdfs:label>
      </bf:Person>
    </bf:subject>
  </bf:Work>
</rdf:RDF>
```

---

[Back to Table of Contents](../index.md)

[Previous Page: Administrative Metadata](administrative-metadata.md) | [Next Page: Identifiers](identifiers.md)
