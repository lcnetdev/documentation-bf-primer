# Hubs

Hubs are abstract bibliographic resources meant to organize resources via collocation and aggregation. Hubs are usually lightweight in the amount of information they contain. They will not contain all the descriptive or subject metadata that is generally expected in a bibliographic description. They are not the main descriptive focus.

A Hub need be no more than this:

```xml
<rdf:RDF>
  <bf:Hub rdf:about="http://id.loc.gov/resources/hubs/4978c720-ca4f-ca86-2d7e-a15f8245ade9">
    <bflc:aap>Homer. Odyssey. English</bflc:aap>
    <bf:title>
      <bf:Title>
        <bf:mainTitle>Odyssey. English</bf:mainTitle>
      </bf:Title>
    </bf:title>
    <bf:title>
    <bf:contribution>
      <bf:Contribution>
        <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/PrimaryContribution"/>
        <bf:agent rdf:resource="http://id.loc.gov/rwo/agents/n78095639" />
        <bf:role rdf:resource="http://id.loc.gov/vocabulary/relators/ctb" />
      </bf:Contribution>
    </bf:contribution>
    <bf:language rdf:resource="http://id.loc.gov/vocabulary/languages/eng" />
  </bf:Hub>
</rdf:RDF>
```

But that is enough to collocate or aggregate all of the resources that are expressions of or subjects of or otherwise related to Homer’s *Odyssey*. (Hubs generally contain a little more information than seen in this example. Variant titles and some times GenreForm information might appear.)

In addition to the following two sections, more information about Hubs may be found in Appendix A.

## Key properties and classes: Hub

&nbsp;&nbsp;&nbsp;&nbsp;[bf:title](https://id.loc.gov/ontologies/bibframe.html#p_title)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:contribution](https://id.loc.gov/ontologies/bibframe.html#p_contribution)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:relation](https://id.loc.gov/ontologies/bibframe.html#p_relation)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:relationship](https://id.loc.gov/ontologies/bibframe.html#p_relationship)

## BIBFRAME Hubs and MARC

Hubs are the functional BIBFRAME equivalent of MARC Title and NameTitle Authorities (1XX+\$t or 130), Main Entry and/or Uniform Title combinations (1xx+240, 130) in the MARC Bibliographic format, or Access Points (6XX+\$t, 630, 7XX+\$t, 730, 8XX+\$t, 830) in the MARC Bibliographic format.

The act of taking what is commonly conceived of as a string in MARC and making it into a ‘resource,’ or ‘entity,’ with a new identity and name seems to be a common stumbling point. In MARC cataloging culture, a name/title access point found in a 700 is a string created using specific rules and designed to collocate resources in a browse display or via searching. But looking more deeply, that carefully crafted string represents an abstract bibliographic resource/entity, regardless of whether the string relates to an authority record in the LC/NACO file or whether it was merely added in a bibliographic description based on cataloger judgment. “Homer’s *Odyssey* in English” is a concept, a bibliographic one, and it is abstracted from any known, specific expression or manifestation. It does not matter if, in MARC, the cataloger enters “Homer. Odyssey. English” in a 700 or if, in BIBFRAME, a cataloger creates a relationship to the Hub presenting Homer’s *Odyssey* in English, in both situations the cataloger is making a reference to an abstracted bibliographic concept with the intent that this Thing being cataloged should in some way collocate, with other similar resources, under the abstract idea thought of as “Homer’s *Odyssey* in English.”

## Implementation consideration: Hubs and RDA

Hubs sometimes are close equivalents to the concept of an RDA Work (consider the above example without the language component) and sometimes are close equivalents to the concept of an RDA Expression, such as the Homer example above, which includes a language designation.

But the importance of Hubs as collocation and aggregation resources cannot be overstated. *Resource Description & Access* (RDA) favors an entirely different approach to work and expression access points. In RDA, disambiguation of work and expression access points is tied to identification. In RDA, work and expression access points are meant to disambiguate, not collocate or aggregate. (It has gone little remarked on how this concept has inverted the traditional role of authority records and access points, which being more general have functioned as collocation and aggregation points, in bibliographic description.) So, while BIBFRAME Hubs can sometimes be surrogates of RDA Works and RDA Expressions, a Hub is not really designed to describe a resource so specifically that it will basically link to no other resource in a collection. Those implementing RDA who wish to use RDA Works and RDA Expressions as disambiguating entities can leverage the generic bf:Work for this purpose and not use Hubs.

---

[Back to Table of Contents](../index.md)

[Previous Page: Items](items.md) | [Next Page: Data Model: Common Properties and Classes](../data-model-common-properties-and-classes/index.md)
