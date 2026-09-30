# Appendix B: LC’s BIBFRAME Bounded Descriptions

As noted in the main text earlier, the Library of Congress makes significant use of what it calls BIBFRAME Bounded Descriptions, notably when exchanging data with Marva (its BIBFRAME editor) and generating MARC records from BIBFRAME descriptions. The idea behind a BIBFRAME Bounded Description is that it is a small graph of information that provides enough information such that the resource is self-explaining.

Although you can serialize it in several ways, including the jsonld version - <https://id.loc.gov/resources/instances/24091701.bd.jsonld> - LC almost always uses the RDF/XML serialization. This Appendix will therefore focus on RDF/XML, but know that the general concepts, such as base resources types, apply regardless of serialization format.

These are the specs for LC’s BIBFRME Bounded Description in the RDF/XML serialization.

## High Level Overview

All principal bf:Works, bf:Instances, and bf:Items are placed directly under the rdf:RDF parent node. bf:Hub may also be a principal element when a Hub is being edited. Subsidiary bf:Works and bf:Hubs, such as those found in relationships, are handled in their nested locations in the XML.

```xml
<rdf:RDF>
  <bf:Instance/>
  <bf:Work/>
  <bf:Item/>
</rdf:RDF>
```

When editing a Hub:

```xml
<rdf:RDF>
  <bf:Hub />
</rdf:RDF>
```

All Objects of Object Properties are “decomposed,” where possible, but with a handful of exceptions: rdf:type, bf:instanceOf, dcterms:isPartOf, bf:hasInstance, bf:itemOf, bf:hasItem, bf:electronicLocator, bf:generationProcess, bf:descriptionLevel. These remain simple URIs identified using an rdf:resource attribute on the Object Property element.

```xml
<rdf:RDF>
  <bf:Instance>
    <dcterms:isPartOf rdf:resource="http://id.loc.gov/resources/instances" />
    <bf:instanceOf rdf:resource="http://id.loc.gov/resources/works/24091701"/>
  </bf:Instance>
</rdf:RDF>
```

Object elements may include extra types. For example, if bf:Agent is an Object’s element name, there may be an rdf:type property within the Object describing it also as a bf:Organization (though, sometimes, bf:Organization may have been used as the Object’s element name). This is typical with bf:Agents, but can happen elsewhere such as with bf:Note resources.

```xml
<rdf:RDF>
  <bf:Work>
    <bf:contribution>
      <bf:Contribution>
        <bf:agent>
          <bf:Agent rdf:about="http://id.loc.gov/vocabulary/organizations/dlc">
            <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Organization"/>
            <rdfs:label>United States, Library of Congress</rdfs:label>
          </bf:Agent>
        </bf:agent>
      </bf:Contribution>
    </bf:contribution>
  </bf:Work>
</rdf:RDF>
```

There is no significance to the order of multiple rdf:types.

Object elements, which include the principal Objects of Work, Instance, Item, and Hub, may have any number of subelements. All Datatype Properties are retained as simple literals. Some Datatype Property elements may have rdf:datatype attributes; some may have xml:lang attributes. If the subelement is an Object Property, it is recursively “decomposed” according to the above guidelines.

Many Object elements will have an rdf:about attribute. These will almost always have one or more labels (usually at least one rdfs:label but madsrdf:authoritativeLabel cannot be ruled out) and many will have one or more bf:code properties/subelements (many of which will have a specific rdf:datatype attribute). Generally, anything with an rdf:about URI that links to ID.LOC.GOV and contains “/vocabulary/” in its URI will have an rdfs:label and the majority will have one or more bf:code properties/subelements. Those with an rdf:about that links to ID.LOC.GOV and containing “/authorities/” or “/rwo/” in their URIs will (likely) have one or more rdfs:label properties/subelements and likely one or more bflc:marcKey properties/subelements. If there are multiples of the same property/subelement, there is likely a distinction to be made between them either from the presence or absence of an XML attribute – xml:lang or rdf:datatype typically – or the attributes values.

```xml
<rdf:RDF>
  <bf:Instance>
    <bf:carrier>
      <bf:Carrier rdf:about="http://id.loc.gov/vocabulary/carriers/nc">
        <rdfs:label>volume</rdfs:label>
        <bf:code>nc</bf:code>
      </bf:Carrier>
    </bf:carrier>
  </bf:Instance>
</rdf:RDF>
```

```xml
<rdf:RDF>
  <bf:Work>
    <bf:subject>
      <bf:Organization rdf:about="http://id.loc.gov/rwo/agents/n81066718">
        <rdfs:label>Korea (North). Chosŏn Inmin'gun</rdfs:label>
        <bflc:marcKey>1101 $aKorea (North).$bChosŏn Inmin'gun</bflc:marcKey>
        <rdfs:label xml:lang="ko ">Korea (North). 조선 인민군</rdfs:label>
        <bflc:marcKey xml:lang="ko">4101 $aKorea (North).$b조선 인민군</bflc:marcKey>
      </bf:Organization>
    </bf:subject>
  </bf:Work>
</rdf:RDF>
```

## Top Level Nodes

All top level nodes are in “decomposed” format, which means that all URIs are expressed and labels and more are fetched from their resources, so that the fuller package is enough to describe the main resource at least as fully as a MARC record would have. The labels are fetched just as the Bounded Description package is assembled, so any changes are incorporated on export. This is the package sent to the BIBFRAME to MARC conversion program and Marva for editing.

For example in a Contribution node:

```xml
<rdf:RDF>
  <bf:Work>
    <bf:contribution>
      <bf:Contribution>
        <bf:agent>
          <bf:Agent rdf:about="http://id.loc.gov/rwo/agents/n80053135">
            <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Person"/>
            <rdfs:label>Geminiani, Francesco, 1687-1762</rdfs:label>
          </bf:Agent>
        </bf:agent>
      </bf:Contribution>
    </bf:contribution>
  </bf:Work>
</rdf:RDF>
```

Information within the Agent resource here is not editable, but Marva will allow you to replace it with a different Agent by swapping out the URI. The same is true for any linked resource from other vocabularies.

The root element of the BIBFRAME Bounded Description is rdf:RDF. There is only one.

Embedded in rdf:RDF is an Instance, it’s Work, and (possibly) any Items, all at the root. Sequence of the nodes should not matter, since the XPATH is the same for each top level element:

```xml
<rdf:RDF>
  <bf:Instance/>
  <bf:Work/>
  <bf:Item/>
</rdf:RDF>
```

## Secondary Instances

Secondary instances are not expected to generate their own separate MARC export, so they are packaged with the main Instance. It is expected that native BIBFRAME systems may begin treating each resource in its own right, but that has implications for building legacy MARC records from the dataset. 

The BIBFRAME Bounded Description will include any Secondary Instance resources. These are identifiable by a suffix added to the URI:

```xml
<rdf:RDF>
  <bf:Instance rdf:about="http://id.loc.gov/resources/instances/7735577"/>
  <bf:Work rdf:about="http://id.loc.gov/resources/works/7735577"/>
  <bf:Instance rdf:about="http://id.loc.gov/resources/instances/7735577-85X-1"/>
</rdf:RDF>
```

Items would be included in the Bounded Description also:

```xml
<rdf:RDF>
  <bf:Instance rdf:about="http://id.loc.gov/resources/instances/19873666"/>
  <bf:Work rdf:about="http://id.loc.gov/resources/works/19873666"/>
  <bf:Instance rdf:about="http://id.loc.gov/resources/instances/19873666-85X-1"/>
  <bf:Item rdf:about="http://id.loc.gov/resources/items/19873666"/>
</rdf:RDF>
```

Each of the top level nodes are a full element set for that resource URI, intended to replace that resource in a consuming system or intended to be the editable resources, as in Marva.

Embedded within each Instance and Item are links to their “parent” resource.

```xml
<rdf:RDF>
  <bf:Work rdf:about="http://id.loc.gov/resources/works/7735577" />
  <bf:Instance rdf:about="http://id.loc.gov/resources/instances/19873666">
    <bf:instanceOf rdf:resource="http://id.loc.gov/resources/works/7735577"/>
  </bf:Instance>
  <bf:Item>
    <bf:itemOf rdf:resource="http://id.loc.gov/resources/instances/19873666"/>
  </bf:Item>
</rdf:RDF>
```

## Hubs

Hubs are sometimes referenced in a BD package. Usually only a label, marcKey, and a few other details are included.

```xml
<rdf:RDF>
  <bf:Work>
    <bf:expressionOf>
      <bf:Hub rdf:about="http://id.loc.gov/resources/hubs/9c0ca213-7755-45ab-6031-a7dbca86053c">
        <bflc:aap>Sonata, keyboard instrument, F major</bflc:aap>
        <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Hub"/>
        <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Audio"/>
        <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/NotatedMusic"/>
      </bf:Hub>
    </bf:expressionOf>
  </bf:Work>
</rdf:RDF>
```

LC’s Marva cannot edit a Hub within a Bounded Description. To edit a Hub, Marva expects the “decomposed” structure from ID.loc.gov, which will contain all the information pertaining to a given Hub. An example: https://id.loc.gov/resources/hubs/71dba5d7-6533-7b22-cd96-6bee74b80efa.decomposed.rdf . Each decomposed resource is a single bf:Hub node wrapped in rdf:RDF. Other hubs related to this Hub can be referenced but will not be editable directly when editing this Hub.

---

[Back to Table of Contents](index.md)

[Previous Page: Appendix A: More about Hubs](appendix-a-more-about-hubs.md)
