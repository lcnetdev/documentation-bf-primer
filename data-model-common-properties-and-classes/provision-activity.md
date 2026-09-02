# Provision Activity

*bf:provisionActivity/bf:ProvisionActivity*

*bf:publicationStatement*

*bf:productionStatement*

*bf:distributionStatement*

*bf:manufactureStatement*

Provision Activity in BIBFRAME is a class of resource that captures event information around the publication, production, distribution, or manufacture of an Instance. Indeed, bf:ProvisionActivity has four subclasses: bf:Publication, bf:Production, bf:Distribution, and bf:Manufacture.

Example 1:

```xml
<rdf:RDF>
  <bf:Instance rdf:about="http://id.loc.gov/resources/instances/17104916">
    <bf:issuance rdf:resource="http://id.loc.gov/vocabulary/issuance/mono"/>
    <bf:provisionActivity>
      <bf:ProvisionActivity>
        <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Publication"/>
        <bf:date rdf:datatype="http://id.loc.gov/datatypes/edtf">2011</bf:date>
        <bf:place rdf:resource="http://id.loc.gov/vocabulary/countries/ie"/>
      </bf:ProvisionActivity>
    </bf:provisionActivity>
    <bf:publicationStatement>Cork: Collins Press, 2011</bf:publicationStatement>
  </bf:Instance>
</rdf:RDF>
```

The example above represents the ideal. The bf:ProvisionActivity is identified as a “Publication,” has a coded date, and has a coded place. The basic ingredients of any event – what, when, and where. One could, if desired, add a bf:agent to the bf:ProvisionActivity resource to identify the publisher (Collins Press). (Likewise, the city of Cork could also have been identified versus the country as place of publication.) Underneath is the human readable provision activity in statement form using bf:publicationStatement formatted with ISBD punctuation, the form long used for displaying this information to library end users.

Provision Activity resources are repeatable within an Instance. There might be one for Distribution and another for Publication. Serial resources tend to have multiple Provision Activity resources, each recording a different publication event in the life of a long-running serial publication.

## Implementation consideration: Interoperability with MARC, RDA requirements

The following example is what is actually observed in the Library of Congress BIBFRAME Instance from Example 1.

```xml
<rdf:RDF>
  <bf:Instance rdf:about="http://id.loc.gov/resources/instances/17104916">
    <bf:issuance rdf:resource="http://id.loc.gov/vocabulary/issuance/mono"/>
    <bf:provisionActivity>
      <bf:ProvisionActivity>
        <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Publication"/>
        <bf:date rdf:datatype="http://id.loc.gov/datatypes/edtf">2011</bf:date>
        <bf:place rdf:resource="http://id.loc.gov/vocabulary/countries/ie"/>
        <bflc:simplePlace>Cork</bflc:simplePlace>
        <bflc:simpleAgent>Collins Press</bflc:simpleAgent>
        <bflc:simpleDate>2011</bflc:simpleDate>
      </bf:ProvisionActivity>
    </bf:provisionActivity>
    <bf:publicationStatement>Cork: Collins Press, 2011</bf:publicationStatement>
  </bf:Instance>
</rdf:RDF>
```

Take note of the three “bflc” properties: bflc:simplePlace, bflc:simpleAgent, bflc:simpleDate. These three properties, which are not in the formal BIBFRAME namespace, exist for the sole purpose of MARC interoperability. MARC parses these discrete bits of information into subfields of the 264 field. In MARC, they are additionally segmented using ISBD punctuation, effectively resulting in double encoding – once in order to place the information into the proper subfield and again with ISBD punctation to distinguish the pieces for the user. Further, this lexical information is ‘transcribed’ from the piece in hand, which invariably results in wide variation (see e.g. <https://id.loc.gov/entities/providers/360bb1111f974b10613761b87bc70320.html> which shows the various, and still incomplete, ways one publisher’s name has been recorded in MARC).

In BIBFRAME, the bf:publicationStatement represents the ISBD-punctuated string, meant for the end user. There is no discernable need to segment this information into individual elements and thus support for this practice is reserved for a non-BIBFRAME namespace and for the express purpose of MARC interoperability. In a pure BIBFRAME environment, bf:publicationStatement (and the other similar properties) should be used exclusively.

Finally, RDA requires only that catalogers record a publication, production, distribution, and manufacture “statement.” Although many RDA catalogers are working in MARC, the BIBFRAME statement properties are likewise sufficient to adhere to this RDA instruction.

Example (publication): <https://id.loc.gov/resources/instances/23586254.html>

```xml
<rdf:RDF>
   <bf:Instance rdf:about="http://id.loc.gov/resources/instances/23586254">
    <bf:issuance rdf:resource="http://id.loc.gov/vocabulary/issuance/mono"/>
    <bf:provisionActivity>
      <bf:ProvisionActivity>
        <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Publication"/>
        <bf:date rdf:datatype="http://id.loc.gov/datatypes/edtf">2025</bf:date>
        <bf:place rdf:resource="http://id.loc.gov/vocabulary/countries/nyu"/>
        <bflc:simplePlace>New York</bflc:simplePlace>
        <bflc:simpleAgent>G. P. Putnam's Sons</bflc:simpleAgent>
        <bflc:simpleDate>2025</bflc:simpleDate>
       </bf:ProvisionActivity>
    </bf:provisionActivity>
    <bf:publicationStatement>New York: G. P. Putnam's Sons, 2025</bf:publicationStatement>
  </bf:Instance>
</rdf:RDF>
```

Example (distribution): <https://id.loc.gov/resources/instances/21648911.html>

```xml
<rdf:RDF>
   <bf:Instance rdf:about="http://id.loc.gov/resources/instances/21648911">
    <bf:provisionActivity>
      <bf:ProvisionActivity>
        <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Distribution"/>
        <bflc:simplePlace>New Haven</bflc:simplePlace>
        <bflc:simpleAgent>distributed outside Benelux by Yale University Press</bflc:simpleAgent>
        <bflc:simpleDate>[2020]</bflc:simpleDate>
      </bf:ProvisionActivity>
    </bf:provisionActivity>
    <bf:distributionStatement>New Haven: distributed outside Benelux by Yale University Press, [2020]</bf:distributionStatement>
  </bf:Instance>
</rdf:RDF>
```

Example (provision activity with status resource): <https://id.loc.gov/resources/instances/15387794.html>

```xml
<rdf:RDF>
   <bf:Instance rdf:about="http://id.loc.gov/resources/instances/15387794">
    <bf:issuance rdf:resource="http://id.loc.gov/vocabulary/issuance/serl"/>
    <bf:provisionActivity>
      <bf:ProvisionActivity>
        <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Publication"/>
        <bf:date rdf:datatype="http://id.loc.gov/datatypes/edtf">2008/..</bf:date>
        <bf:status rdf:resource="http://id.loc.gov/vocabulary/mstatus/current"/>
        <bf:place rdf:resource="http://id.loc.gov/vocabulary/countries/ncu"/>
        <bflc:simplePlace>Charlotte, NC</bflc:simplePlace>
        <bflc:simpleAgent>Hearst Communications, Inc</bflc:simpleAgent>
      </bf:ProvisionActivity>
    </bf:provisionActivity>
    <bf:publicationStatement>Charlotte, NC: Hearst Communications, Inc</bf:publicationStatement>
  </bf:Instance>
</rdf:RDF>
```

---

[Back to Table of Contents](../index.md)

[Previous Page: Notes](notes.md) | [Next Page: Relationships](relationships.md)
