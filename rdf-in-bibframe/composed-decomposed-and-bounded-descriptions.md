# Composed, Decomposed, and Bounded Descriptions

## Composed and Decomposed Descriptions

A “composed” description is the most succinct representation of a resource. This mostly affects the objects of triples. If the object of a triple is a URI, the resource identified by that URI is not expanded. (Anonymous resources – those identified by blank nodes – are expanded.) Note in the below example, only the URI of the bf:genreForm.

```xml
<rdf:RDF>
  <bf:Work rdf:about="http://id.loc.gov/resources/works/23626846">
    <bf:genreForm rdf:resource="http://id.loc.gov/authorities/genreForms/gf2014026339"/>
  </bf:Work>
</rdf:RDF>
```

A more dramatic example:

```xml
<rdf:RDF>
  <bf:Work rdf:about="http://id.loc.gov/resources/works/22481758">
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/MovingImage"/>
    <bf:language rdf:resource="http://id.loc.gov/vocabulary/languages/eng"/>
    <bf:duration rdf:datatype="http://www.w3.org/2001/XMLSchema#duration">PT131M</bf:duration>
    <bf:language rdf:resource="http://id.loc.gov/vocabulary/languages/spa"/>
    <bf:language rdf:resource="http://id.loc.gov/vocabulary/languages/fre"/>
    <bf:geographicCoverage rdf:resource="http://id.loc.gov/vocabulary/geographicAreas/n-usp"/>
    <bf:originDate rdf:datatype="http://id.loc.gov/datatypes/edtf">1992</bf:originDate>
    <bf:expressionOf rdf:resource="http://id.loc.gov/resources/hubs/56b3c7b1-bcaf-52cb-daaa-f12d12062b83"/>
    <bf:title>
      <bf:Title>
        <bf:mainTitle>Unforgiven</bf:mainTitle>
      </bf:Title>
    </bf:title>
    <bf:content rdf:resource="http://id.loc.gov/vocabulary/contentTypes/tdi"/>
    <bf:contribution>
      <bf:Contribution>
        <bf:agent rdf:resource="http://id.loc.gov/rwo/agents/n50024426"/>
        <bf:role rdf:resource="http://id.loc.gov/vocabulary/relators/fmd"/>
        <bf:role rdf:resource="http://id.loc.gov/vocabulary/relators/fmp"/>
        <bf:role rdf:resource="http://id.loc.gov/vocabulary/relators/act"/>
      </bf:Contribution>
    </bf:contribution>
    <bf:contribution>
      <bf:Contribution>
        <bf:agent rdf:resource="http://id.loc.gov/rwo/agents/n93002890"/>
        <bf:role rdf:resource="http://id.loc.gov/vocabulary/relators/aus"/>
      </bf:Contribution>
    </bf:contribution>
    <bf:contribution>
      <bf:Contribution>
        <bf:agent rdf:resource="http://id.loc.gov/rwo/agents/n88678708"/>
        <bf:role rdf:resource="http://id.loc.gov/vocabulary/relators/act"/>
      </bf:Contribution>
    </bf:contribution>
  </bf:Work>
</rdf:RDF>
```

A “decomposed” description, conversely, is more verbose, and, again, this mostly affects object resources. The principal idea behind a decomposed description is to provide enough information about related entities such that the whole description is understandable. Thus, object resources – when the object of a triple is a resource – will be expanded to include, minimally, a label, but might also include other details, such as codes or types. In most cases the inclusion of some kind of “label” is sufficient, but in other cases – for example when the object resource is another Work or Instance – more information may be needed and/or desirable. The two examples above, now in their decomposed forms:

```xml
<rdf:RDF>
  <bf:Work rdf:about="http://id.loc.gov/resources/works/23626846">
    <bf:genreForm>
         <bf:GenreForm rdf:about="http://id.loc.gov/authorities/genreForms/gf2014026339">
        <rdfs:label xml:lang="en">Fiction</rdfs:label>
      </bf:GenreForm>
    </bf:genreForm>
  </bf:Work>
</rdf:RDF>
```

And the more dramatic example:

```xml
<rdf:RDF>
  <bf:Work rdf:about="http://id.loc.gov/resources/works/22481758">
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/MovingImage"/>
    <bf:language>
      <bf:Language rdf:about="http://id.loc.gov/vocabulary/languages/eng">
        <rdfs:label xml:lang="en">English</rdfs:label>
        <bf:code rdf:datatype="http://www.w3.org/2001/XMLSchema#string">eng</bf:code>
      </bf:Language>
    </bf:language>
    <bf:duration rdf:datatype="http://www.w3.org/2001/XMLSchema#duration">PT131M</bf:duration>
    <bf:language>
      <bf:Language rdf:about="http://id.loc.gov/vocabulary/languages/spa">
        <rdfs:label xml:lang="en">Spanish</rdfs:label>
        <bf:code rdf:datatype="http://www.w3.org/2001/XMLSchema#string">spa</bf:code>
      </bf:Language>
    </bf:language>
    <bf:language>
      <bf:Language rdf:about="http://id.loc.gov/vocabulary/languages/fre">
        <rdfs:label xml:lang="en">French</rdfs:label>
        <bf:code rdf:datatype="http://www.w3.org/2001/XMLSchema#string">fre</bf:code>
      </bf:Language>
    </bf:language>
    <bf:geographicCoverage>
      <bf:GeographicCoverage rdf:about="http://id.loc.gov/vocabulary/geographicAreas/n-usp">
        <rdfs:label xml:lang="en">West (U.S.)</rdfs:label>
        <bf:code rdf:datatype="http://id.loc.gov/datatypes/codes/gac">n-usp--</bf:code>
      </bf:GeographicCoverage>
    </bf:geographicCoverage>
    <bf:originDate rdf:datatype="http://id.loc.gov/datatypes/edtf">1992</bf:originDate>
    <bf:expressionOf>
      <bf:Hub rdf:about="http://id.loc.gov/resources/hubs/56b3c7b1-bcaf-52cb-daaa-f12d12062b83">
        <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/MovingImage"/>
        <rdfs:label>Unforgiven (Motion picture)</rdfs:label>
        <bflc:marcKey>1300 $aUnforgiven (Motion picture)</bflc:marcKey>
        <bf:title>
          <bf:Title>
            <bf:mainTitle>Unforgiven (Motion picture)</bf:mainTitle>
          </bf:Title>
        </bf:title>
        <bf:title>
          <bf:VariantTitle>
            <bf:mainTitle>Cut whore killings (Motion picture)</bf:mainTitle>
          </bf:VariantTitle>
        </bf:title>
        <bf:title>
          <bf:VariantTitle>
            <bf:mainTitle>William Munny killings (Motion picture)</bf:mainTitle>
          </bf:VariantTitle>
        </bf:title>
      </bf:Hub>
    </bf:expressionOf>
    <bf:title>
      <bf:Title>
        <bf:mainTitle>Unforgiven</bf:mainTitle>
      </bf:Title>
    </bf:title>
    <bf:content>
      <bf:Content rdf:about="http://id.loc.gov/vocabulary/contentTypes/tdi">
        <rdfs:label>two-dimensional moving image</rdfs:label>
        <bf:code>tdi</bf:code>
      </bf:Content>
    </bf:content>
    <bf:contribution>
      <bf:Contribution>
        <bf:agent>
          <bf:Agent rdf:about="http://id.loc.gov/rwo/agents/n50024426">
            <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Person"/>
            <rdfs:label>Eastwood, Clint, 1930-</rdfs:label>
            <bflc:marcKey>1001 $aEastwood, Clint,$d1930-</bflc:marcKey>
          </bf:Agent>
        </bf:agent>
        <bf:role>
          <bf:Role rdf:about="http://id.loc.gov/vocabulary/relators/fmd">
            <rdfs:label>film director</rdfs:label>
            <bf:code>fmd</bf:code>
          </bf:Role>
        </bf:role>
        <bf:role>
          <bf:Role rdf:about="http://id.loc.gov/vocabulary/relators/fmp">
            <rdfs:label>film producer</rdfs:label>
            <bf:code>fmp</bf:code>
          </bf:Role>
        </bf:role>
        <bf:role>
          <bf:Role rdf:about="http://id.loc.gov/vocabulary/relators/act">
            <rdfs:label>actor</rdfs:label>
            <bf:code>act</bf:code>
          </bf:Role>
        </bf:role>
      </bf:Contribution>
    </bf:contribution>
    <bf:contribution>
      <bf:Contribution>
        <bf:agent>
          <bf:Agent rdf:about="http://id.loc.gov/rwo/agents/n93002890">
            <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Person"/>
            <rdfs:label>Peoples, David Webb</rdfs:label>
            <bflc:marcKey>1001 $aPeoples, David Webb</bflc:marcKey>
          </bf:Agent>
        </bf:agent>
        <bf:role>
          <bf:Role rdf:about="http://id.loc.gov/vocabulary/relators/aus">
            <rdfs:label>screenwriter</rdfs:label>
            <bf:code>aus</bf:code>
          </bf:Role>
        </bf:role>
      </bf:Contribution>
    </bf:contribution>
    <bf:contribution>
      <bf:Contribution>
        <bf:agent>
          <bf:Agent rdf:about="http://id.loc.gov/rwo/agents/n88678708">
            <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Person"/>
            <rdfs:label>Harris, Richard, 1930-2002</rdfs:label>
            <bflc:marcKey>1001 $aHarris, Richard,$d1930-2002</bflc:marcKey>
          </bf:Agent>
        </bf:agent>
        <bf:role>
          <bf:Role rdf:about="http://id.loc.gov/vocabulary/relators/act">
            <rdfs:label>actor</rdfs:label>
            <bf:code>act</bf:code>
          </bf:Role>
        </bf:role>
      </bf:Contribution>
    </bf:contribution>
  </bf:Work>
</rdf:RDF>
```

## Bounded Descriptions

The Library of Congress has made extensive use of a BIBFRAME data output it calls a Bounded Description, or CBD for short. The notion of a “bounded description” – or, more specifically, a “concise bounded description” – was a proposed means by which to publish and/or exchange RDF data as a small graph of information. It was an idea introduced in 2005 at the W3C but not pursued. The proposal nonetheless became the foundation for BIBFRAME bounded descriptions. Quoting the introduction from [2005 W3C proposal](https://www.w3.org/submissions/CBD/) demonstrates its relevance:

> As the semantic web emerges and the behavior of automated software agents become increasingly directed by formally defined knowledge about resources gathered from disparate sources, the need for optimal and consistent interchange of knowledge about specific resources between agents becomes critical to achieving an efficient, globally scalable, and ubiquitous semantic web.
>
> This document defines a concise bounded description of a resource in terms of an RDF graph, as a general and broadly optimal unit of specific knowledge about that resource to be utilized by, and/or interchanged between, semantic web agents.
>
> Given a particular node in a particular RDF graph, a concise bounded description is a subgraph consisting of those statements which together constitute a focused body of knowledge about the resource denoted by that particular node.
>
> Optimality is, of course, application dependent and it is not presumed that a concise bounded description is an optimal form of description for every application.

A BIBFRAME bounded description brings together all the information to make a single (bibliographic) resource independently understandable. A BIBFRAME bounded description is a small graph of information that will, minimally, include one Work and one Instance, but will additionally include expanded information about contributions, agents, subjects, related resources, and much more. In so far as a traditional MARC bibliographic record contains all the information about a resource – mostly expressed as labels in the record – a BIBFRAME bounded description likewise contains all the information about a specific resource.

The Library of Congress’s BIBFRAME bounded descriptions are used extensively in its BIBFRAME ecosystem. They are what is loaded into the Library’s BIBFRAME editor (Marva). Catalogers need to be able to view both an Instance and its Work, as well as related RDF resources; editing an Instance or a Work in isolation is impractical, to say the least. Marva posts the entire bounded description package back to the BIBFRAME database when complete. The BIBFRAME bounded description – the small graph of information – for a given resource is literally the input for the BIBFRAME-to-MARC conversion program. It is possible to access any BIBFRAME bounded description from an Instance URI at ID.LOC.GOV. Example:

<https://id.loc.gov/resources/instances/22481758.bd.rdf>

Note: BIBFRAME bounded descriptions do not match the algorithm detailed in the 2005 W3C proposal. Please see Appendix B for details about how the Library of Congress creates its bounded descriptions.

---

[Back to Table of Contents](../index.md)

[Previous Page: RDF in BIBFRAME](index.md) | [Next Page: Properties and classes overview](properties-and-classes-overview.md)
