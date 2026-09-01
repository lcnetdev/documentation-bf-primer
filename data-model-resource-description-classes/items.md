# Items

A bf:Item describes a specific copy of a bf:Instance and will therefore almost always have a relationship to a specific organization. For example, the Library of Congress may hold a specific copy of a book with marginalia of some significance. The bf:Item provides a way to capture these *descriptive* details about the Library’s physical copy of a specific bf:Instance. A bf:Item is not intended to be used for inventory control though bf:Item could theoretically be used or understood to function in such a way.

bf:Item

&nbsp;&nbsp;&nbsp;&nbsp;bf:itemOf lc:Instance:1234

&nbsp;&nbsp;&nbsp;&nbsp;bf:heldby \<org:lc\>

&nbsp;&nbsp;&nbsp;&nbsp;bf:note/bf:Note/rdfs:label “Marginalia by Albert Einstein”

&nbsp;&nbsp;&nbsp;&nbsp;bf:barcode “098654321”

## Key properties: Item

&nbsp;&nbsp;&nbsp;&nbsp;[bf:contribution](https://id.loc.gov/ontologies/bibframe.html#p_contribution)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:classification](https://id.loc.gov/ontologies/bibframe.html#p_classification)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:heldBy](https://id.loc.gov/ontologies/bibframe.html#p_heldBy)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:identifiedBy](https://id.loc.gov/ontologies/bibframe.html#p_identifiedBy)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:itemOf](https://id.loc.gov/ontologies/bibframe.html#p_itemOf)

&nbsp;&nbsp;&nbsp;&nbsp;[bf:note](https://id.loc.gov/ontologies/bibframe.html#p_note)

## Implementation Consideration: Instances and Items

Sometimes the line between Instance and Item can be blurry and sometimes it can also be unnecessarily complicated. Implementers will ultimately decide how best to adopt the BIBFRAME model and vocabulary for their uses, but the Library of Congress has identified two implementation considerations to bear in mind about Instances and Items.

1)  bf:electronicLocator is used to capture a (web) accessible address/location for content. For example, the bf:Instance for an ebook might include a bf:electronicLocator property pointing to the ebook itself, i.e. the content, or the Item itself. Some may note that an Instance, in this scenario, should link to an Item, which would then host the bf:electronicLocator property, and would thus be arguably more consistent with the overall model since the content at the end of the URL \*is\* the Item in question. But from an implementation perspective, modelling this information in such a way – Work hasInstance Instance; Instance hasItem Item; Item electronicLocator \<URL\> – introduced an unneeded and unnecessarily complicating abstraction in the data and so it was deemed desirable to simply associate the content directly with the Instance. This resulted in fewer hops in the data (to the benefit of simpler queries and easier navigation) and the elimination of many tiny bf:Item resources of little merit beyond containing a bf:electronicLocator property.

2)  Rare materials, especially books, can be so unique that the Instance itself is unlike anything else in the owning organization’s collection not to mention any other collection. Missing pages, special inserts, notes, custodial history, and more can all combine in such a way that a given Instance, while theoretically a copy of something that may have at one point in history been mass produced, is so unique, or so unlike any other Instance of that Work, that the Item \*is\* its own standalone Instance. Indeed, the specialness of the rare resource can alter the identity of the resource as a whole that it requires its own bf:Work. Therefore, whereas the BIBFRAME model would suggest that the descriptive elements of a rare item should logically be recorded as a bf:Item that relates to a mass-produced Instance, which in turn relates to a common Work, rare materials often have sufficient identify from their generic counterparts to justify their own bf:Work/bf:Instance combination, thereby rendering the bf:Item an unnecessary abstraction.

---

[Back to Table of Contents](../index.md)

[Previous Page: Instances](instances.md) | [Next Page: Hubs](hubs.md)
