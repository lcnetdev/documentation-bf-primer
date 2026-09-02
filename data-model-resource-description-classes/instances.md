# Instances

A bf:Instance represents an individual embodiment – whether physical or electronic - of a bf:Work. An Instance for a physical resource will include information about the resource’s physical details (page numbers, dimensions, e.g.), provision activity (publication or distribution info), and Instance-specific identifiers, such as ISBNs. An electronic Instance will capture details such as file size, file type, access modes, etc. With the information recorded for a bf:Instance, in conjunction with its related bf:Work, combine to neatly identify a single attainable resource in a library’s collection. The bf:Instance *is similar to* the RDA manifestation.

Multiple Instances can relate to a single Work, and this is where much of the potential of the BIBFRAME model comes into play. A publisher produces a Hardback, Paperback, Large Print, and an Ebook of a title. Each of those represents a different Instance of the same Work. Music publishers or movie distributors might do the same – an album is made available as a CD or LP or digital download; a movie is made available as a DVD, BluRay, 4K, or digital download. Notably, Instances, at the model level, essentially are of two types: Physical or Electronic. While it is possible to refine Instance typing, between the bf:media and bf:carrier properties, there is already much in each Instance description to help any consumer to more granularly identify the physical or electronic nature of the Instance.

## Key properties: Instance

bf:Instance properties seek to describe the who, what, where, when, and how of an acquirable resource. This may include where a resource was published or distributed, who published or distributed it, and when. Details about its existence, such as page numbers or dimensions for physical material or bytes and file types for electronic. Identifiers associated with those specific physical or electronic resources, such as system numbers, ISBNs, control numbers, etc.

&nbsp;&nbsp;&nbsp;&nbsp;[bf:carrier](https://id.loc.gov/ontologies/bibframe.html#p_carrier)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:copyrightDate](https://id.loc.gov/ontologies/bibframe.html#p_copyrightDate)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:dimensions](https://id.loc.gov/ontologies/bibframe.html#p_dimensions)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:distributionStatement](https://id.loc.gov/ontologies/bibframe.html#p_distributionStatement)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:duration](https://id.loc.gov/ontologies/bibframe.html#p_duration)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:electronicLocator](https://id.loc.gov/ontologies/bibframe.html#p_electronicLocator)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:extent](https://id.loc.gov/ontologies/bibframe.html#p_extent)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:identifiedBy](https://id.loc.gov/ontologies/bibframe.html#p_identifiedBy)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:instanceOf](https://id.loc.gov/ontologies/bibframe.html#p_instanceOf)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:media](https://id.loc.gov/ontologies/bibframe.html#p_media)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:note](https://id.loc.gov/ontologies/bibframe.html#p_note)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:provisionActivity](https://id.loc.gov/ontologies/bibframe.html#p_classification)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:publicationStatement](https://id.loc.gov/ontologies/bibframe.html#p_publicationStatement)

## Implementation Consideration: Secondary Instances

The BIBFRAME concept of Secondary Instances grew out of the understanding that a single MARC record can include multiple manifestations of a resource or other bits of accompanying material, even though there is just one MARC record with one valid LCCN. Some Instances the Library of Congress produces carry an additional type from the BFLC namespace: bflc:SecondaryInstance.

Sometimes a resource to be cataloged is a single object, like a book. And sometimes, a resource being cataloged consists of multiple parts in different forms, like a book with a CD or a film issued as a DVD but with bonus content on a computer CD.

In each case, the resource can be cataloged in BIBFRAME as a single work. The number of instances will vary.

- One print monograph = one Work and one Instance

- One book with a CD = one Work, one Instance for the book, one Instance for the CD

- One print map and its digitized version = one Work, one Instance for the print map, one Instance for the digitized map

- One DVD and an accompanying CD = one Work, one Instance for the DVD, one Instance for the CD

To avoid unnecessary redundancy, the majority of the data (such as provision activity, identifiers, notes, statement of responsibility) is placed on one Instance and the technical information unique to each accompanying object (carrier, media, electronic locator, extent, dimensions) is placed on a Secondary Instance. Often, however, Secondary Instances are slimmer than the main Instance simply because most MARC records from which they are derived contain far fewer details about them. They are designed to work in conjunction with the Work and Instance(s) to describe all of the components of the resource being cataloged.

The Library of Congress views the use of Secondary Instances as a mechanism to bridge past MARC cataloging practice with current and future cataloging in BIBFRAME. In a pure BIBFRAME implementation, without need to create MARC records that describe various components of a single resource, Secondary Instance resources are not needed or advisable.

Examples of Secondary Instances:

&nbsp;&nbsp;&nbsp;&nbsp;<https://id.loc.gov/resources/works/18790086.html>

&nbsp;&nbsp;&nbsp;&nbsp;<https://id.loc.gov/resources/works/13797793.html>

&nbsp;&nbsp;&nbsp;&nbsp;<https://id.loc.gov/resources/works/21775889.html>

&nbsp;&nbsp;&nbsp;&nbsp;<https://id.loc.gov/resources/works/21965143.html>

&nbsp;&nbsp;&nbsp;&nbsp;<https://id.loc.gov/resources/works/11966429.html>

---

[Back to Table of Contents](../index.md)

[Previous Page: Works](works.md) | [Next Page: Items](items.md)
