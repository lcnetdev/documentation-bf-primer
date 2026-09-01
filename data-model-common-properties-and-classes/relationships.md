# Relationships

*bf:relation/bf:Relation\
bf:relationship\
bf:associatedResource*

Relationships as discussed in this section generally apply to relationships between principal Bibframe resources: Work, Instance, Hub, and Item. Bibframe supports two methods for expressing relationships: the indirect method and the direct method.

The direct method employs an object property to relate two resources to one another:

&nbsp;&nbsp;&nbsp;&nbsp;work1 bf:isTranslationOf work2

The indirect method for relationships implements a model very similar to the bf:Contribution model. The indirect method, like the one for bf:Contribution, introduces an abstraction resource that bundles one or more relationship designators alongside a reference to one or more associated resources.

work1 bf:relation \_r

&nbsp;&nbsp;&nbsp;&nbsp;\_r rdf:type \<bf:Relation\> .

&nbsp;&nbsp;&nbsp;&nbsp;\_r bf:relationship \<relationships:translationOf\> .

&nbsp;&nbsp;&nbsp;&nbsp;\_r bf:associatedResource \<work2\>

Leveraging an abstraction layer makes it possible not only to identify multiple relationships the source resource has with an Associated Resource, but also include additional information pertaining to the related resources as well as expressing more complex relationship patterns.

For example, sometimes it is beneficial to include a note (for a human) that aims to explain some relationships.

```xml
<rdf:RDF>
   <bf:Work rdf:about="http://id.loc.gov/resources/works/11133555">
    <bflc:aap>Social register, Washington</bflc:aap>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Text"/>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Serial"/>
    <bf:relation>
      <bf:Relation>
        <bf:note>
            <bf:Note>
                <rdf:type rdf:resource="http://id.loc.gov/vocabulary/mnotetype/relnote"/>
                <rdfs:label>Supplemented in the summer by: Social register, summer (covers all city editions of the Social register).</rdfs:label>
            </bf:Note>
        </bf:note>
        <bf:relationship rdf:resource="http://id.loc.gov/vocabulary/relationship/supplement"/>
        <bf:associatedResource rdf:resource="http://id.loc.gov/resources/works/13123320"/>
      </bf:Relation>
    </bf:relation>
  </bf:Work>
</rdf:RDF>
```

In another example, the Work is part of a Series, which is to say the Work relates to a Series, but the series enumeration, i.e. which specific issue in a series, is extra information in that it is not part of the Series title or resource proper. It is recorded as additional information to the relationship.

```xml
<rdf:RDF>
   <bf:Work rdf:about="http://id.loc.gov/resources/works/21883950">
    <bflc:aap>Élite burial practices and processes of urbanization at Gabii : the non-adult tombs from area D of the Gabii project excavations</bflc:aap>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Text"/>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Monograph"/>
    <bf:relation>
      <bf:Relation>
        <bf:relationship rdf:resource="http://id.loc.gov/vocabulary/relationship/series"/>
        <bf:seriesEnumeration>no. 108.</bf:seriesEnumeration>
        <bf:associatedResource rdf:resource="http://id.loc.gov/resources/hubs/935b464a-3c49-61b8-35ae-5ca0c4dd9b5e"/>
      </bf:Relation>
    </bf:relation>
  </bf:Work>
</rdf:RDF>
```

The following example not only contains a Note but represents a complex relationship, one showing how the source resource (the Work being described) was split into two different resources at some point in its history:

```xml
<rdf:RDF>
   <bf:Work rdf:about="http://id.loc.gov/resources/works/11257335">
    <bflc:aap>The daily dramatic chronicle</bflc:aap>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Text"/>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Serial"/>
    <bf:relation>
      <bf:Relation>
        <bf:note>
            <bf:Note>
                <rdf:type rdf:resource="http://id.loc.gov/vocabulary/mnotetype/relnote"/>
                <rdfs:label>Split into: Daily morning chronicle (San Francisco, Calif.), and: Dramatic review (San Francisco, Calif.).</rdfs:label>
            </bf:Note>
        </bf:note>
        <bf:relationship rdf:resource="http://id.loc.gov/vocabulary/relationship/splitinto"/>
        <bf:associatedResource rdf:resource="http://id.loc.gov/resources/works/11257334"/>
        <bf:associatedResource rdf:resource="http://id.loc.gov/resources/works/19976425"/>
      </bf:Relation>
    </bf:relation>
  </bf:Work>
</rdf:RDF>
```

The indirect method – the more abstraction method – creates flexibility.

## Implementation consideration: Careful deployment of both methods

The Library of Congress uses both the direct and indirect relationship methods but tries to employ them in consistent and clear ways. How the Library deploys which method has been heavily influenced by its need to convert from and to MARC Bibliographic data. Initially, the Library attempted to model all relationships using the direct method, but the richness and complexity of library bibliographic data revealed a number of shortcomings, top of which was loss of clarity in the data (or no improvement over the MARC data).

Relationships in the MARC 7XX and 8XX range have been modelled using the indirect method. This has facilitated returning this information back to MARC but it has also deployed the most flexible option for the richest relationships found in MARC Bibliographic records. The preceding example, for instance, merged a 580 relationship note and two 785 relationships together into a single Bibframe Relation resource.

The following relationships are still deployed using the direct method to knit together principal resources:

&nbsp;&nbsp;&nbsp;&nbsp;bf:hasInstance/bf:instanceOf \[These link bf:Work to a bf:Instance and vice versa.\]

&nbsp;&nbsp;&nbsp;&nbsp;bf:hasItem/bf:itemOf \[These link bf:Instance to a bf:Item and vice versa.\]

&nbsp;&nbsp;&nbsp;&nbsp;bf:hasExpression/bf:expressionOf \[These link bf:Work to a bf:Hub and vice versa.\]

The last in that list represents a single concession in how the Library has modelled its Bibframe data where arguably the indirect method could have been used. To put that statement in context, name/title (MARC 700,711,710 with \$t) and title (MARC 730) access points are relationships in MARC between the resource described in the 245 and some other abstract bibliographic resource. When they are converted to Bibframe, they use the indirect method and link to Hubs. This is why the “expression” relationships above, which also link a bf:Work to a bf:Hub (and vice versa), could have been logically treated via the indirect method. Nonetheless, the direct method was chosen to emphasize the tighter relationship between a BF Work and the Hub of which it is an expression, elevating a relationship with strong association to RDA.

In at least two other places, the Library uses the direct method for relationships. One is handling the rather complex “X, Y, Z was ‘merged to form’ A” relationship:

```xml
<rdf:RDF>
   <bf:Work rdf:about="http://id.loc.gov/resources/works/19533794">
    <bflc:aap>Social register, Pittsburgh</bflc:aap>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Text"/>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Serial"/>
    <bf:relation>
      <bf:Relation>
        <bf:note>
            <bf:Note>
                <rdf:type rdf:resource="http://id.loc.gov/vocabulary/mnotetype/relnote"/>
                <rdfs:label>Merged with social registers of various cities, including: Social register, Baltimore; Social register, Boston; Social register, Buffalo; Social register, Chicago; Social register, Cincinnati &amp; Dayton; Social register, Cleveland; Social register, New York; Social register, Philadelphia, including Wilmington; Social register Providence; Social register, St. Louis; Social register, San Francisco; and: Social register, Washington; to form: Social register.</rdfs:label>
            </bf:Note>
        </bf:note>
        <bf:relationship rdf:resource="http://id.loc.gov/vocabulary/relationship/mergedtoform"/>
        <bf:mergedWith rdf:resource="http://id.loc.gov/resources/works/19545917"/>
        <bf:mergedWith rdf:resource="http://id.loc.gov/resources/works/11133427"/>
        <bf:mergedWith rdf:resource="http://id.loc.gov/resources/works/11133609"/>
        <bf:mergedWith rdf:resource="http://id.loc.gov/resources/works/11133555"/>
        <bf:associatedResource rdf:resource="http://id.loc.gov/resources/works/11734633"/>
      </bf:Relation>
    </bf:relation>
  </bf:Work>
</rdf:RDF>
```

Inside the abstract bf:Relation resource there are a number of bf:mergedWith relationship properties that directly link to the related resource; the bf:mergedWith relationship properties in this scenario are used directly. The above (also) includes a human-readable note that explains the relationships. In this example, the bf:Work being described was merged with four other resources to form the resource the bf:associatedResource points to; “Social register, Pittsburgh” and four other titles were merged into a single resource, the one identified via the bf:associatedResource property.

The other place the Library uses a direct Work to Work relationship is for the handling of language information from MARC 041. See the Language section of this document for more information.

## Implementation consideration: Transcribed Series information (aka MARC 490)

The Library has modelled all related Series, whether from an 800, 810, 811, or 830 or from a 490, as a related Work/Series relationship employing the indirect method. Past and present cataloging practices (i.e. RDA) relegate certain information to specific parts of the model based on the method of recordation. In RDA, for example, *transcribed* information is associated with an RDA Manifestation. Ergo, since the BF Instance is closest to the concept of an RDA Manifestation (worth remembering: close is not the same as “equal to”), transcribed information, such as Series information recorded in the MARC 490 field, belongs with the Instance, or so the logic goes. But the MARC 490 is merely a loose way of capturing a relationship between two resources – a Work and its related Series. The pairing of 490s and 830s, which represent the very same Series except in controlled form, underscores that, despite the method of recordation, this is a relationship between two resources first and foremost. Thus, in Bibframe a relationship to a Series is treated uniformly at the model level – they are all placed on the bf:Work. (The associated resource for one of these “transcribed” Series is still a bf:Series, just as a resource converted from an 830 is, but it is marked as transcribed and therefore “uncontrolled.” Catalogers are expected to transcribe the information in Bibframe just as they are in MARC.)

## Implementation consideration: Placement

The Library of Congress has placed all relationships at the bf:Work level. Said another way, relationships to other BF resources (other than the direct ones noted above) are not expressed on the bf:Instance or bf:Item. No bf:Instance has a relationship to a bf:Hub; no bf:Hub has a relationship to a bf:Instance.

This is an implementation decision. Nothing in the model dictates that relationships cannot be at the bf:Instance or bf:Item level. The Library has made this decision for consistency and clarity.

---

[Back to Table of Contents](../index.md)

[Previous Page: Provision Activity](provision-activity.md) | [Next Page: Subjects](subjects.md)
