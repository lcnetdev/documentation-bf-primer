# Relationship to MARC

BIBFRAME is designed to be a MARC replacement. As such, it is suitably rich in its ability to describe bibliographic resources. MARC was originally designed for printed catalog cards and early computer retrieval capabilities, and still very much contains the remnants of these purposes with its use of ISBD punctuation, subfielding, and coded 00X data. BIBFRAME is designed for more contemporary computing infrastructures. BIBFRAME preferences the use of identifiers – URIs – over string matching and especially any need to perform subfield-by-subfield string matching.

And, while MARC encoding and practice have evolved in such a way as to spread information out across ordered subfields (in MARC terminology) that are then most often concatenated back together with a space in between. BIBFRAME offers simplification of information recordation in favor of creating richer relationships between resources, whether those be bibliographic-to-bibliographic relationships, or agent-to-bibliographic relationships, or subject-to-resource relationships.

The Library of Congress maintains a BIBFRAME-to-MARC conversion specification and related programs. By converting existing MARC data to BIBFRAME and then back to MARC, the fidelity to the original MARC description is readily observable, underscoring that the data simplifications are almost invisible while the use of identifiers and relationships more readily apparent. The inclusion of URIs in the MARC data have made it possible at the Library of Congress to, thus far, roundtrip bibliographic descriptions (meaning from MARC to BIBFRAME back to MARC or vice versa). But the MARC is still very much a flat output whose maintenance is potentially to be performed manually on strings, while the URIs ensure the BIBFRAME data not only retains its connections to the broader graph of data but take precedence in that the BIBFRAME descriptions can grow infinitely richer and more detailed while, in MARC, the data are limited simply to what a field’s subfields allow.

---

[Back to Table of Contents](index.md)

[Previous Page: BIBFRAME and Content Models (such as RDA)](bibframe-and-content-models-such-as-rda.md) | [Next Page: Data Model: Resource Description Classes](data-model-resource-description-classes/index.md)
