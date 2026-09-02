# Introduction

This document describes the BIBFRAME Model and Vocabulary, for use primarily within the library and information science community to describe collection resources. A great number of these resources will be truly bibliographic in nature (i.e monographs and serials), but the model and vocabulary can accommodate all types of common materials, such as audio recordings, notated music, moving images, etc. This document will consider all of these types as “bibliographic resources,” meaning they are collection resources managed by a cultural organization (mainly libraries). The BIBFRAME vocabulary is presented as an OWL ontology, though constraints and/or domain/range declarations are few.

This document is a user guide for those who would like to represent this type of material using BIBFRAME.

BIBFRAME is expressed in RDF, which stands for Resource Description Framework and which, as part of the name would suggest (“Framework”), is but the basis for something larger. RDF resources are atomic, typically focused on the description of a discrete resource, and knitted together via relationships. In BIBFRAME, a single ‘traditional’ library resource, which was perhaps described in a single MARC record, will be composed of a number of smaller resources that, combined, constitute a small graph of information, with a BIBFRAME Work and BIBFRAME Instance at its heart. That small graph will be part of a larger graph, with resources linking to each other, and so on, resulting in an infinite graph of information.

## Contents

- [Status of this document](status-of-this-document.md)
- [Namespaces and Examples](namespaces-and-examples.md)
  - [BFLC](namespaces-and-examples.md#bflc)
  - [Examples](namespaces-and-examples.md#examples)
- [Organization and Abbreviations](organization-and-abbreviations.md)
- [Special Terminology](special-terminology.md)

---

[Back to Table of Contents](../index.md)

[Previous Page: BIBFRAME primer](../index.md) | [Next Page: Status of this document](status-of-this-document.md)

<!--
NAV_ORDER
index.md
status-of-this-document.md
namespaces-and-examples.md
organization-and-abbreviations.md
special-terminology.md
-->
