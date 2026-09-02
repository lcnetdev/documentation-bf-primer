# Appendix A: More about Hubs

One can approach BIBFRAME Hubs from a theoretical perspective, i.e. one that references principles of library and information science theory, or from a practical perspective, perhaps by describing how they relate to current MARC practice.

The latter is often marginally more successful and discussed above: Hubs are the functional BIBFRAME equivalent of MARC Title and NameTitle Authorities (1XX+\$t or 130), Main Entry and/or Uniform Title combinations (1xx+240, 130) in the MARC Bibliographic format, or Access Points (6XX+\$t, 630, 7XX+\$t, 730, 8XX+\$t, 830) in the MARC Bibliographic format.

The carefully constructed strings in MARC Title and NameTitle authorities – indeed, the reason behind developing an authority file more generally - and Main Entries plus Uniform Titles and Access Points in MARC bibliographic records have traditionally been used for collocation (McCallum. In physical card catalogs and later online systems, these strings made it possible to cluster information items. Current Library of Congress cataloging policies and use of these headings facilitate collocation.

The focus, thus far, has been on how these carefully constructed strings, composed, minimally, of a normalized form of a name (if appropriate) and a normalized form of the title, function in MARC, where much of the functionality these headings enable is based on string matching or viewing browse lists of these strings. The strings are the identifiers. But BIBFRAME is a data format that uses pure identifiers, not strings, to identify resources. The string is secondary. In the simplest of explanations, the strings used in MARC were wrapped in a resource called a Hub and then the Hub given an identifier, an HTTP URI.

An example (the same as earlier):

```xml
<rdf:RDF>
<bf:Hub rdf:about="http://id.loc.gov/resources/hubs/4978c720-ca4f-ca86-2d7e-a15f8245ade9">
    <bflc:aap>Homer. Odyssey. English</bflc:aap>    <bf:title>
      <bf:Title>
    <bf:mainTitle>Odyssey. English</bf:mainTitle>
      </bf:Title>
    </bf:title>
    <bf:contribution>
      <bf:Contribution>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/PrimaryContribution"/>
    <bf:agent rdf:resource="http://id.loc.gov/rwo/agents/n78095639"/>
    <bf:role rdf:resource="http://id.loc.gov/vocabulary/relators/ctb"/>
      </bf:Contribution>
    </bf:contribution>
    <bf:language rdf:resource="http://id.loc.gov/vocabulary/languages/eng"/>
</bf:Hub>
</rdf:RDF>
```

Although the creator (Homer), title (Odyssey), and language (English) have been broken into distinct elements, the AAP (short for Authorized Access Point) near the top retains the carefully constructed string used in MARC cataloging. Although this example has been pruned of a few variant titles and a few notes for the sake of succinctness, Hubs are designed, much like Title and NameTitle authorities, to be fairly lightweight. They are an essential component of the ecosystem, but not the main focus of the cataloger’s attention, nor of the user.

In BIBFRAME, since this Hub has an identifier, it is possible to link to the Hub (and it is also possible to link the Hub to other resources). With all of the potential incoming and outgoing links, the Hub functions very much as its name implies – it is a Hub with many spokes connected to other resources. And it is therefore also possible to aggregate all the versions of Homer’s Odyssey in English in precisely the way the controlled string functions in MARC. This is why Hubs have always been described as aggregators and why they functionally serve the same purpose of the Title and NameTitle Authorities, Main Entries plus Uniform Titles, and Access Points in MARC.

The act of taking what is commonly conceived of as a string in MARC and making it into a ‘resource,’ or ‘entity,’ with a new identity and name seems to be a common stumbling point. In MARC cataloging culture, a name/title access point found in a 700 is a string created using specific rules and designed to collocate resources in a browse display or via searching. But looking more deeply, that carefully crafted string represents an abstract bibliographic resource/entity, regardless of whether the string relates to an authority record in the LC/NACO file or whether it was merely added in a bibliographic description based on cataloger judgment. “Homer’s Odyssey in English” is a concept, a bibliographic one, and it is abstracted from any known, specific expression or manifestation. It does not matter if, in MARC, the cataloger enters “Homer. Odyssey. English” in a 700 or if, in BIBFRAME, a cataloger creates a relationship to the Hub presenting Homer’s Odyssey in English, in both situations the cataloger is making a reference to an abstracted bibliographic concept with the intent that this Thing being cataloged should in some way collocate, with other similar resources, under the abstract idea thought of as “Homer’s Odyssey in English.”

Having introduced the notion that Hubs, like access points, represent an abstract bibliographic concept/resource/entity, it is not clear how much deeper into information theory one must delve to sufficiently describe Hubs and their relationship to traditional cataloging, but it is worth viewing the above in light of Elaine Svenonius’s 2000 publication The Intellectual Foundation of Information Organization. Quoting Svenonius at length about what she describes as “Work Identifiers (Work IDs)” is illuminating:

> From the point of view of collocation the most important metadata used in bibliographic description are work identifiers. How to construct work IDs is a problem that has claimed the attention of some of the best minds in cataloging and one that has been misunderstood by many. Normally, the AACR author-title language identifies authored works using expressions consisting of the normalized name of the author followed by the normalized title of the work. Where a work has no obvious author, its ID is its normalized title. Work identifiers were introduced in the nineteenth century in the form of main entries… (95)

She is, of course, describing the name/title pair found in Title and Name/Title authority records, main entries plus uniform titles, and access points. Notably, lest we apply today’s concept of ‘identifier,’ it is worth underscoring how it is the resulting string from the normalized name/title combination that is the identifier. And she opens with the notion of collocation and notes the importance of these work identifiers. All of this perfectly aligns with how these strings have been used in bibliographic description in a MARC environment.

Earlier in Intellectual Foundation, Svenonius introduces the notion of ‘sets,’ with sections about ‘work sets’ and ‘author sets’ and ‘subject sets,’ etc. She also introduces the idea of a ‘superworks set’ (“A superwork may contain any number of works as subsets, the members of which while not sharing essentially the same information content are nevertheless similar by virtue of emanating from the same ur-work” (38)) and ended with a section for “other entities.” In short, she introduced the concept of “set theory,” which has its roots in mathematics, to bibliographic description. From Stanford’s Encyclopedia of Philosophy: “Set theory is the mathematical theory of well-determined collections, called sets, of objects that are called members, or elements, of the set.” Svenonius explored how taking attributes of documents, for example, such as author and title to determine work sets or whether something is a revision or abridgement of a work to determine edition sets. Although Hubs do not relate in any specific way to any of the sets Svenonius identified, they certainly have commonalities with ‘work sets’ and ‘superwork sets’ and the ‘entity sets.’ But her description of a work set, in light of Hubs, is worth quoting in full:

> The forming of work sets constitutes the prototypical act of information organization. It is the act that collects in one place all documents that contain the same information, that systematically integrates each new document into a database, and that transforms the database from a simple finding tool to a sophisticated bibliographic tool. In structuring a database, work sets are used to perform two essential functions: to organize displays and to provide nodes for linking related bibliographic entities. (36)

To suggest this is about Hubs is anachronistic and wrong, and it is immaterial whether Hubs better align with Svenonius’s notion of work or superwork or simply entity, but it is nigh impossible to take her description of a ‘work set’ and not view Hubs as being a set of collected, related bibliographic resources (“nodes for linking related bibliographic entities”) that can be used to organize displays/information.

Ultimately, Svenonius is not talking about RDF and RDF Resources and triples – her notions are largely grounded in the practice of using strings for identity – but it is hard not to see how the use of Hubs in BIBFRAME do not conform to her ideas for information organization.

Hubs as aggregators have become essential, mostly as nodes between related bibliographic entities. They perform the historical function of collocation that are the rationale behind the traditional Title and NameTitle Authorities, Main Entries plus Uniform Titles, and Access Points in MARC.

But performing the functions of effective aggregation and collocation have been increasingly challenged in the last five to ten years because of the introduction of, and growth in number of, ever more expression-specific headings. These expression-specific headings are permitted by RDA cataloging rules and some in the community exercise this option vigorously. A few examples of these expression specific headings:

> 100 1 \$aBrontë, Charlotte,\$d1816-1855.\$tJane Eyre.\$lSpanish\$s(Gómez Aquino)
>
> 100 0 \$aEuripides.\$tMedea.\$lEnglish\$s(Way).\$f1894
>
> 100 0 \$aEuripides.\$tMedea.\$lEnglish\$s(Way).\$f1912
>
> 100 0 \$aEuripides.\$tMedea.\$lGreek\$s(Paley).\$f1872
>
> 100 0 \$aHomer.\$tOdyssey.\$lEnglish\$s(Rieu, Rieu, and Jones). Spoken word (Blagden)
>
> 100 0 \$aHomer.\$tOdyssey (Findaway World, LLC).\$lEnglish.\$hSpoken word\$s(Findaway World, LLC)

The names seen in these headings are somewhat ambiguous; they may reflect the editor, translator, narrator or producer. Regardless, they are added, as are the dates, to disambiguate the heading - i.e. Authority – from anything else in the file and to ensure the resulting string, mainly to be used in MARC bibliographic descriptions, is unique in the LC/NACO file. This is the very opposite of facilitating collocation. Indeed, some headings are so unique that it is hard to see how, for example, “Euripides. Medea. English (Way). 1912” will collocate anything other than the 1912 Way-translated version of Euripides’s Medea.

From a practical perspective, these exceedingly expression-specific headings create noise in the system, and their specificity is an impediment to aggregation. As such, despite being Title and NameTitle authorities and headings, they are not candidates for Hubs and are not found (generally) in the Hub dataset. (It is possible one or two slipped through because it had been used in a bibliographic record and maintaining the link/relationship took precedence, with bibliographic maintenance to follow.)

**References**

Bagaria, Joan, "Set Theory", The Stanford Encyclopedia of Philosophy (Spring 2023 Edition), Edward N. Zalta & Uri Nodelman (eds.), <https://plato.stanford.edu/archives/spr2023/entries/set-theory>

McCallum, Sally. “Collocation and Hubs. Fundamental and New Version”. *JLIS.It* , vol. 13, no. 1, Jan. 2022, pp. 45-52, doi:10.4403/jlis.it-12760. <https://www.jlis.it/index.php/jlis/article/view/418/411>

Svenonius, Elaine. *The Intellectual Foundation of Information Organization*. Cambridge, Massachusetts: The MIT Press, 2000.

---

[Back to Table of Contents](index.md)

[Previous Page: References and Links](references-and-links.md)
