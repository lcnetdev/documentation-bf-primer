# Administrative Metadata

*bf:adminMetadata/bf:AdminMetadata*

For any BIBFRAME description, there are metadata elements which pertain to the description, rather than to the resource which is the subject of the description. These elements are stored in Admin Metadata resources using the BIBFRAME property bf:adminMetadata. This structure ensures that the administrative metadata is clearly distinguished from statements describing the resource.

A single BIBFRAME description will contain multiple Admin Metadata resources. Most are very brief and only contain the status, the date that the status changed, and the agent which changed the resource. These capture events in the history of the description. But there will typically be one bf:AdminMetadata resource that captures more specific cataloging information like encoding level, description conventions, description authentication, and language of cataloging.

Example (basic administrative event; shows time of conversion from MARC): <https://id.loc.gov/resources/works/20898769.html>

```xml
<rdf:RDF>
  <bf:Work rdf:about="http://id.loc.gov/resources/works/20898769">
    <bflc:aap>Obama, Michelle, 1964-. Becoming</bflc:aap>
    <bf:adminMetadata>
      <bf:AdminMetadata>
        <bf:status rdf:resource="http://id.loc.gov/vocabulary/mstatus/c"/>
        <bf:agent rdf:resource="http://id.loc.gov/vocabulary/organizations/dlcmrc"/>
        <bf:generationProcess rdf:resource="https://github.com/lcnetdev/marc2bibframe2/releases/tag/v3.1.0"/>
        <bf:date rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">2026-04-15T18:40:56.393103-04:00</bf:date>
      </bf:AdminMetadata>
    </bf:adminMetadata>
  </bf:Work>
</rdf:RDF>
```

Example (showing specific cataloging details): <https://id.loc.gov/resources/works/20898769.html>

```xml
<rdf:RDF>
  <bf:Instance rdf:about="http://id.loc.gov/resources/instances/20898769">
    <bf:adminMetadata>
      <bf:AdminMetadata>
        <bf:descriptionLevel rdf:resource="http://id.loc.gov/ontologies/bibframe-3-0-1/"/>
        <bflc:encodingLevel rdf:resource="http://id.loc.gov/vocabulary/menclvl/f"/>
        <bf:descriptionConventions rdf:resource="http://id.loc.gov/vocabulary/descriptionConventions/isbd"/>
        <bf:identifiedBy>
            <bf:Local>
                <rdf:value>20898769</rdf:value>
                <bf:assigner rdf:resource="http://id.loc.gov/vocabulary/organizations/dlc"/>
            </bf:Local>
        </bf:identifiedBy>
        <bf:descriptionLanguage rdf:resource="http://id.loc.gov/vocabulary/languages/eng"/>
        <bf:descriptionConventions rdf:resource="http://id.loc.gov/vocabulary/descriptionConventions/rda"/>
        <bf:descriptionAuthentication rdf:resource="http://id.loc.gov/vocabulary/marcauthen/lccopycat"/>
      </bf:AdminMetadata>
    </bf:adminMetadata>
  </bf:Instance>
</rdf:RDF>
```

---

[Back to Table of Contents](../index.md)

[Previous Page: Data Model: Common Properties and Classes](index.md) | [Next Page: Contributions and Contributors](contributions-and-contributors.md)
