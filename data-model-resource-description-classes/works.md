# Works

Works represent the conceptual essence of a resource and include characteristics that are common to the assorted manifestations of the Work, like contributors, subjects, summaries and genre/form terms. “Conceptual essence” means all aspects of the resource’s expression. A BIBFRAME Work with a specific translator is different from a BIBFRAME Work with a different translator; translators have defined objectives and strategies, making their product different from others who have performed the same basic function. A BIBFRAME Work with an introduction or a reader’s guide is different from a BIBFRAME Work without those elements; the inclusion of a reader’s guide subtly, but meaningfully, creates an educational element that is otherwise absent from the published original. These differences – some big, some small – generate slightly different identities for each resource or bf:Work. So while the bf:Work is defined as the “conceptual essence of a resource” it is the totality of a resource’s characteristics in the aggregate that give a bf:Work its distinct identity from other, perhaps very similar resources.

## Key properties: Work

bf:Work properties seek to describe the who, what, and when of a resource. This includes a resource’s genre or form, its aboutness, relationships it may have to other Works in the ecosystem. The bf:Work information typically applies to any bf:Instances related to the bf:Work. The contributors, subjects, and language – all bf:Work properties - of a textual resource, a book for example, will remain the same whether published electronically as an ebook or physically as a hardback or a paperback – all bf:Instance properties.

&nbsp;&nbsp;&nbsp;&nbsp;[bf:classification](https://id.loc.gov/ontologies/bibframe.html#p_classification)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:content](https://id.loc.gov/ontologies/bibframe.html#p_content)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:contribution](https://id.loc.gov/ontologies/bibframe.html#p_contribution)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:ensemble](https://id.loc.gov/ontologies/bibframe.html#p_mediumComponent)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:genreForm](https://id.loc.gov/ontologies/bibframe.html#p_genreForm)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:hasInstance](https://id.loc.gov/ontologies/bibframe.html#p_hasInstance)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:language](https://id.loc.gov/ontologies/bibframe.html#p_language)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:note](https://id.loc.gov/ontologies/bibframe.html#p_note)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:relation](https://id.loc.gov/ontologies/bibframe.html#p_relation)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:subject](https://id.loc.gov/ontologies/bibframe.html#p_subject)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:title](https://id.loc.gov/ontologies/bibframe.html#p_title)

## Implementation consideration: BF Work and RDA Work

A Bibframe Work is closer to an RDA Expression than it is to an RDA Work (this is not, however, to say they are the same!). The core of the Bibframe model – BF Works and BF Instances – is about describing real-life resources, not abstractions. The objective is to describe a resource that a user may want to review or acquire. Considerable detail, therefore, may go into a BF Work description such that the included information might be seen as traditional RDA Work elements – titles, authors – but also RDA Expression elements – such as language, content type, other contributors.

---

[Back to Table of Contents](../index.md)

[Previous Page: Data Model: Resource Description Classes](index.md) | [Next Page: Instances](instances.md)
