![](images/image1.png)

# BIBFRAME primer

BIBFRAME (BF) provides a model for representing bibliographic data in a linked data environment. This document is a reference guide for those who would like to implement the Bibframe model and vocabulary.

---

## Table of Contents

- [Introduction](introduction/index.md)
  - [Status of this document](introduction/status-of-this-document.md)
  - [Namespaces and Examples](introduction/namespaces-and-examples.md)
    - [BFLC](introduction/namespaces-and-examples.md#bflc)
    - [Examples](introduction/namespaces-and-examples.md#examples)
  - [Organization and Abbreviations](introduction/organization-and-abbreviations.md)
  - [Special Terminology](introduction/special-terminology.md)
- [Data Model Overview](data-model-overview.md)
- [BIBFRAME and Content Models (such as RDA)](bibframe-and-content-models-such-as-rda.md)
- [Relationship to MARC](relationship-to-marc.md)
- [Data Model: Resource Description Classes](data-model-resource-description-classes/index.md)
  - [Works](data-model-resource-description-classes/works.md)
    - [Key properties: Work](data-model-resource-description-classes/works.md#key-properties-work)
    - [Implementation consideration: BF Work and RDA Work](data-model-resource-description-classes/works.md#implementation-consideration-bf-work-and-rda-work)
  - [Instances](data-model-resource-description-classes/instances.md)
    - [Key properties: Instance](data-model-resource-description-classes/instances.md#key-properties-instance)
    - [Implementation Consideration: Secondary Instances](data-model-resource-description-classes/instances.md#implementation-consideration-secondary-instances)
  - [Items](data-model-resource-description-classes/items.md)
    - [Key properties: Item](data-model-resource-description-classes/items.md#key-properties-item)
    - [Implementation Consideration: Instances and Items](data-model-resource-description-classes/items.md#implementation-consideration-instances-and-items)
  - [Hubs](data-model-resource-description-classes/hubs.md)
    - [Key properties and classes: Hub](data-model-resource-description-classes/hubs.md#key-properties-and-classes-hub)
    - [BIBFRAME Hubs and MARC](data-model-resource-description-classes/hubs.md#bibframe-hubs-and-marc)
    - [Implementation consideration: Hubs and RDA](data-model-resource-description-classes/hubs.md#implementation-consideration-hubs-and-rda)
- [Data Model: Common Properties and Classes](data-model-common-properties-and-classes/index.md)
  - [Contributions and Contributors](data-model-common-properties-and-classes/contributions-and-contributors.md)
  - [Identifiers](data-model-common-properties-and-classes/identifiers.md)
  - [Language](data-model-common-properties-and-classes/language.md)
    - [Implementation consideration: Handling language information from MARC](data-model-common-properties-and-classes/language.md#implementation-consideration-handling-language-information-from-marc)
  - [Notes](data-model-common-properties-and-classes/notes.md)
  - [Provision Activity](data-model-common-properties-and-classes/provision-activity.md)
    - [Implementation consideration: Interoperability with MARC, RDA requirements](data-model-common-properties-and-classes/provision-activity.md#implementation-consideration-interoperability-with-marc-rda-requirements)
  - [Relationships](data-model-common-properties-and-classes/relationships.md)
    - [Implementation consideration: Careful deployment of both methods](data-model-common-properties-and-classes/relationships.md#implementation-consideration-careful-deployment-of-both-methods)
    - [Implementation consideration: Transcribed Series information (aka MARC 490)](data-model-common-properties-and-classes/relationships.md#implementation-consideration-transcribed-series-information-aka-marc-490)
    - [Implementation consideration: Placement](data-model-common-properties-and-classes/relationships.md#implementation-consideration-placement)
  - [Subjects](data-model-common-properties-and-classes/subjects.md)
    - [Implementation consideration: LCSH](data-model-common-properties-and-classes/subjects.md#implementation-consideration-lcsh)
  - [Titles](data-model-common-properties-and-classes/titles.md)
    - [Implementation consideration: MARC](data-model-common-properties-and-classes/titles.md#implementation-consideration-marc)
    - [Implementation consideration: Domain](data-model-common-properties-and-classes/titles.md#implementation-consideration-domain)

---

[Next Page: Introduction](introduction/index.md)
