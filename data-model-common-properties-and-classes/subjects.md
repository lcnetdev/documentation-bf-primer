# Subjects

*bf:subject/bf:Topic*

*bf:subject/bf:Agent*

*bf:subject/bf:Place*

*bf:subject/bf:Hub*

BIBFRAME’s single bf:subject object property may identify four different types of subjects: (generic/conceptual) Topics, Agents (People, Organizations, e.g.), Places, and Hubs (other bibliographic resources). But there are no restrictions on its use and so could be used with bf:Work or bf:Event. Any entity or concept from any subject scheme can be used in BIBFRAME. The source of the term or entity is usually identifiable via URI but can also be identified via the bf:source property.

## Implementation consideration: LCSH

The Library of Congress remains committed to the Library of Congress Subject Heading scheme which supports a precoordinated system of heading creation. Precoordination means that catalogers determine which terms are chosen and establish their order, which carries meaning. (Postcoordination places the burden of combination on users to generate Boolean searches and even then the concept of order is lost or challenging at best.)

To support LCSH precoordination, BIBFRAME uses properties and modelling from the MADS/RDF namespace. Specifically, madsrdf:componentList is used to record individual concepts that compose a precoordinated string and ensure their order is maintained. MADS/RDF resource types, especially as used in the madsrdf:componentList, are used liberally.

The Library of Congress has also implemented a modelling decision that concludes any subject that combines one or more entities or concepts be identified as a bf:Topic, which is defined in similar terms as skos:Concept.

```xml
<rdf:RDF>
   <bf:Work rdf:about="http://id.loc.gov/resources/works/20644710">
    <bflc:aap>Cassiano, Domenico, 1935-. Inchiostro e lupare : intellettuali e potere tra briganti e galantuomini</bflc:aap>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Text"/>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Monograph"/>
    <bf:subject>
      <bf:Topic>
        <rdf:type rdf:resource="http://www.loc.gov/mads/rdf/v1#ComplexSubject"/>
        <rdfs:label>Italy, Southern--Social life and customs--19th century</rdfs:label>
        <madsrdf:authoritativeLabel>Italy, Southern--Social life and customs--19th century</madsrdf:authoritativeLabel>
        <madsrdf:isMemberOfMADSScheme rdf:resource="http://id.loc.gov/authorities/subjects"/>
        <madsrdf:componentList rdf:parseType="Collection">
            <madsrdf:Geographic rdf:about="http://id.loc.gov/authorities/subjects/sh85069035">
                <madsrdf:authoritativeLabel xml:lang="en">Italy, Southern</madsrdf:authoritativeLabel>
            </madsrdf:Geographic>
            <madsrdf:Topic rdf:about="http://id.loc.gov/authorities/subjects/sh2001008851">
                <madsrdf:authoritativeLabel xml:lang="en">Social life and customs</madsrdf:authoritativeLabel>
            </madsrdf:Topic>
            <madsrdf:Temporal rdf:about="http://id.loc.gov/authorities/subjects/sh2002012475">
                <madsrdf:authoritativeLabel xml:lang="en">19th century</madsrdf:authoritativeLabel>
            </madsrdf:Temporal>
        </madsrdf:componentList>
      </bf:Topic>
    </bf:subject>
  </bf:Work>
</rdf:RDF>
```

The above example shows one of these complex subjects with considerable support from MADS/RDF. This resource is clearly about 19<sup>th</sup> century Social life and customs in Southern Italy.

**More examples**

Example (topical subject): <https://id.loc.gov/resources/works/12134925.html>

```xml
<rdf:RDF>
   <bf:Work rdf:about="http://id.loc.gov/resources/works/12134925">
    <bflc:aap>Abbey, Duane C. Compliance for coding, billing &amp; reimbursement : a systematic approach to developing a comprehensive program</bflc:aap>
   <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Text"/>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Monograph"/>
    <bf:subject>
      <bf:Topic rdf:about="http://id.loc.gov/authorities/subjects/sh85066933">
        <rdfs:label xml:lang="en">Health insurance claims</rdfs:label>
        <bf:source rdf:resource="http://id.loc.gov/authorities/subjects" />
      </bf:Topic>
    </bf:subject>
  </bf:Work>
</rdf:RDF>
```

Example (subject with geographic and topical subdivisions): <https://id.loc.gov/resources/works/24229583.html>

```xml
<rdf:RDF>
   <bf:Work rdf:about="http://id.loc.gov/resources/works/24229583">
    <bflc:aap>Gorman, Megan. All the presidents' money : how the men who governed America governed their money</bflc:aap>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Text"/>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Monograph"/>
    <bf:subject>
      <bf:Topic>
        <rdf:type rdf:resource="http://www.loc.gov/mads/rdf/v1#ComplexSubject"/>
        <rdfs:label>Presidents--United States--Finance, Personal</rdfs:label>
        <madsrdf:authoritativeLabel>Presidents--United States--Finance, Personal</madsrdf:authoritativeLabel>
        <madsrdf:isMemberOfMADSScheme rdf:resource="http://id.loc.gov/authorities/subjects" />
        <madsrdf:componentList rdf:parseType="Collection">
            <madsrdf:Topic rdf:about="http://id.loc.gov/authorities/subjects/sh85106459">
                <rdfs:label xml:lang="en">Presidents</rdfs:label>
            </madsrdf:Topic>
            <madsrdf:Geographic rdf:about="http://id.loc.gov/rwo/agents/n78095330-781">
                <rdfs:label>United States</rdfs:label>
            </madsrdf:Geographic>
            <madsrdf:Topic rdf:about="http://id.loc.gov/authorities/subjects/sh2002007886">
                <rdfs:label xml:lang="en">Finance, Personal</rdfs:label>
            </madsrdf:Topic>
        </madsrdf:componentList>
      </bf:Topic>
    </bf:subject>
  </bf:Work>
</rdf:RDF>
```

Example (geographic subject): <https://id.loc.gov/resources/works/20743537.html>

```xml
<rdf:RDF>
   <bf:Work rdf:about="http://id.loc.gov/resources/works/20743537">
    <bflc:aap>A stitch in time : African-American quiltmakers of Oakland</bflc:aap>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/MovingImage"/>
    <bf:subject>
      <bf:Place rdf:about="http://id.loc.gov/rwo/agents/n79118971">
        <rdfs:label>Oakland (Calif.)</rdfs:label>
      </bf:Place>
    </bf:subject>
  </bf:Work>
</rdf:RDF>
```

Example (geographic subject with topical and chronological subdivisions): <https://id.loc.gov/resources/works/23883951.html>

```xml
<rdf:RDF>
   <bf:Work rdf:about="http://id.loc.gov/resources/works/23883951">
    <bflc:aap>Madrigal, Alexis, 1982-. The Pacific Circuit : A Globalized Account of the Battle for the Soul of an American City</bflc:aap>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Text"/>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Monograph"/>
    <bf:subject>
      <bf:Topic>
        <rdf:type rdf:resource="http://www.loc.gov/mads/rdf/v1#ComplexSubject"/>
        <rdfs:label>Oakland (Calif.)--Economic conditions--21st century.</rdfs:label>
        <madsrdf:authoritativeLabel>Oakland (Calif.)--Economic conditions--21st century.</madsrdf:authoritativeLabel>
        <madsrdf:isMemberOfMADSScheme rdf:resource="http://id.loc.gov/authorities/subjects" />
        <madsrdf:componentList rdf:parseType="Collection">
            <madsrdf:Geographic rdf:about="http://id.loc.gov/rwo/agents/n79118971">
                <rdfs:label>Oakland (Calif.)</rdfs:label>
            </madsrdf:Geographic>
            <madsrdf:Topic rdf:about="http://id.loc.gov/authorities/subjects/sh99005736">
                <rdfs:label xml:lang="en">Economic conditions</rdfs:label>
            </madsrdf:Topic>
            <madsrdf:Temporal rdf:about="http://id.loc.gov/authorities/subjects/sh2002012478">
                <rdfs:label xml:lang="en">21st century</rdfs:label>
            </madsrdf:Temporal>
        </madsrdf:componentList>
      </bf:Topic>
    </bf:subject>
  </bf:Work>
</rdf:RDF>
```

---

[Back to Table of Contents](../index.md)

[Previous Page: Relationships](relationships.md) | [Next Page: Titles](titles.md)
