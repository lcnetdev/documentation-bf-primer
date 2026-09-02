# Titles

*bf:title/bf:Title*

BIBFRAME defines a single title property, bf:title, with a corresponding bf:Title class.

For variant titles, bf:VariantTitle is a subclass of bf:Title, and it has the following subclasses:

- bf:AbbreviatedTitle

- bf:CollectiveTitle

- bf:KeyTitle

- bf:ParallelTitle

In addition to those types defined in the BIBFRAME vocabulary, the Variant Title Type dataset, published by the Library of Congress’s Linked Data Service (id.loc.gov), is a list of resources all of which are defined as bf:VariantTitle resources and readily usable with the BIBFRAME model and vocabulary: <https://id.loc.gov/vocabulary/vartitletype.html>. These variant types can be expressed by use of the rdf:type property of the bf:VariantTitle resource.

```xml
<rdf:RDF>
   <bf:Work>
        <bf:title>
            <bf:VariantTitle>
                <rdf:type rdf:resource="http://id.loc.gov/vocabulary/vartitletype/tra" />
                <bf:mainTitle xml:lang="fr">Le Prince et le Pauvre</bf:mainTitle>
            </bf:VariantTitle>
        </bf:title>
  </bf:Work>
</rdf:RDF>
```

In addition, the following properties may occur within a title resource:

- bf:mainTitle

- bf:subtitle

- bf:qualifier

- bf:date

- bf:originDate

- bf:partName

- bf:partNumber

- bf:version

- bf:assigner

- bflc:nonSortNum

BIBFRAME implementers are encouraged to create the simplest Title resources possible and use the many available properties sparingly. Despite their creation and existence, there is little benefit to segmenting title information when implementing BIBFRAME. Not only does it make the data much more difficult to query and manipulate, but most effort will go to merely recombining the parts into a sensible string.

Compare:

```xml
<rdf:RDF>
   <bf:Work>
        <bf:title>
            <bf:KeyTitle>
                <bf:mainTitle>JAMA</bf:mainTitle>
                <bf:qualifier>(Chicago, Ill.)</bf:qualifier>
            </bf:KeyTitle>
        </bf:title>
  </bf:Work>
</rdf:RDF>
```

to the simpler:

```xml
<rdf:RDF>
   <bf:Work>
        <bf:title>
            <bf:KeyTitle>
                <bf:mainTitle>JAMA (Chicago, Ill.)</bf:mainTitle>
            </bf:KeyTitle>
        </bf:title>
  </bf:Work>
</rdf:RDF>
```

Or

Compare:

```xml
<rdf:RDF>
   <bf:Work>
        <bf:title>
            <bf:Title>
                <bf:mainTitle>Superman</bf:mainTitle>
                <bf:partName>The dark path</bf:partName>
                <bf:partNumber>Vol. 3</bf:partNumber>
            </bf:Title>
        </bf:title>
  </bf:Work>
</rdf:RDF>
```

to the simpler:

```xml
<rdf:RDF>
   <bf:Work>
        <bf:title>
            <bf:Title>
                <bf:mainTitle>Superman. Vol. 3, The dark path</bf:mainTitle>
            </bf:Title>
        </bf:title>
  </bf:Work>
</rdf:RDF>
```

## Implementation consideration: MARC

Most of those properties – subtitle, date, qualifier, partName, partNumber – are defined in BIBFRAME to ease conversion to and from MARC, which expects titles to be parsed into smaller pieces by way of subfields. If compatibility with MARC is not of concern or required, handling titles as simple string literals of bf:mainTitle is advisable.

Note order is difficult to impossible to maintain when the parts of titles are parsed into small sections.

## Implementation consideration: Domain

Whether a bf:Title should be associated with the bf:Work or bf:Instance (or bf:Item or bf:Hub) is an implementation decision. What should be borne in mind is that a Title of the Work generally applies to all Instances and any Instance titles are specific to the Instance. A “spine” title (a shortened title, e.g., printed on the spine of the physical book) is obviously specific to an Instance. If the Title from the Title page is common to both the hardback, paperback, and electronic versions, it may be more appropriate to associate it with the Work. NB: the BIBFRAME Model and Vocabulary is silent about where it is best to enter “transcribed”’ information.

Example (main title with no subtitle): <https://id.loc.gov/resources/instances/22753990.html>

```xml
<rdf:RDF>
   <bf:Instance rdf:about="http://id.loc.gov/resources/instances/22753990">
    <bf:title>
      <bf:Title>
        <bf:mainTitle>Do you like getting creative?</bf:mainTitle>
      </bf:Title>
    </bf:title>
  </bf:Instance>
</rdf:RDF>
```

Example (main title and subtitle): <https://id.loc.gov/resources/instances/14279282.html>

```xml
<rdf:RDF>
   <bf:Instance rdf:about="http://id.loc.gov/resources/instances/14279282">
    <bf:title>
      <bf:Title>
        <bf:mainTitle>The great deluge</bf:mainTitle>
        <bf:subtitle>Hurricane Katrina, New Orleans, and the Mississippi Gulf Coast</bf:subtitle>
        <bflc:nonSortNum>4</bflc:nonSortNum>
      </bf:Title>
    </bf:title>
  </bf:Instance>
</rdf:RDF>
```

Example (main title with part number and part name): <https://id.loc.gov/resources/instances/23416899.html>

```xml
<rdf:RDF>
   <bf:Instance rdf:about="http://id.loc.gov/resources/instances/23416899">
    <bf:title>
      <bf:Title>
        <bf:mainTitle>Superman: Action comics</bf:mainTitle>
        <bf:partNumber>Vol. 1</bf:partNumber>
        <bf:partName>Rise of Metallo</bf:partName>
      </bf:Title>
    </bf:title>
  </bf:Instance>
</rdf:RDF>
```

Example (abbreviated title): <https://id.loc.gov/resources/works/18697382.html>

```xml
<rdf:RDF>
   <bf:Work rdf:about="http://id.loc.gov/resources/works/18697382">
    <bflc:aap>JDR clinical and translational research</bflc:aap>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Text"/>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Serial"/>
    <bf:title>
      <bf:AbbreviatedTitle>
        <bf:mainTitle>JDR clin. trans. res.</bf:mainTitle>
        <bf:qualifier>(Online)</bf:qualifier>
        <bf:assigner>
            <bf:Agent>
                <bf:code>issnkey</bf:code>
            </bf:Agent>
        </bf:assigner>
      </bf:AbbreviatedTitle>
    </bf:title>
  </bf:Work>
</rdf:RDF>
```

Example (key title): <https://id.loc.gov/resources/works/11260957.html>

```xml
<rdf:RDF>
   <bf:Work rdf:about="http://id.loc.gov/resources/works/11260957">
    <bflc:aap>JAMA : the journal of the American Medical Association</bflc:aap>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Text"/>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Serial"/>
    <bf:title>
      <bf:AbbreviatedTitle>
        <bf:mainTitle>JAMA</bf:mainTitle>
        <bf:qualifier>(Chic. Ill.)</bf:qualifier>
        <bf:assigner>
            <bf:Agent>
                <bf:code>issnkey</bf:code>
            </bf:Agent>
        </bf:assigner>
      </bf:AbbreviatedTitle>
    </bf:title>
  </bf:Work>
</rdf:RDF>
```

Example (variant title type, spine title): <https://id.loc.gov/resources/instances/23227325.html>

```xml
<rdf:RDF>
   <bf:Instance rdf:about="http://id.loc.gov/resources/instances/23227325">
    <bf:title>
      <bf:Title>
        <bf:mainTitle>UNESCO Namibia National Commission @30</bf:mainTitle>
        <bf:subtitle>1992-2022</bf:subtitle>
      </bf:Title>
    </bf:title>
    <bf:title>
      <bf:VariantTitle>
        <rdf:type rdf:resource="http://id.loc.gov/vocabulary/vartitletype/spi"/>
        <bf:mainTitle>Namibia National Commission for UNESCO @30</bf:mainTitle>
      </bf:VariantTitle>
    </bf:title>
  </bf:Instance>
</rdf:RDF>
```

Example (variant title type, added title page title): <https://id.loc.gov/resources/works/in00024299736.html>

```xml
<rdf:RDF>
   <bf:Work rdf:about="http://id.loc.gov/resources/works/in00024299736">
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Text"/>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Monograph"/>
    <bf:title>
      <bf:VariantTitle>
        <rdf:type rdf:resource="http://id.loc.gov/vocabulary/vartitletype/atp"/>
        <bf:mainTitle>The masses (A roman)</bf:mainTitle>
      </bf:VariantTitle>
    </bf:title>
  </bf:Work>
</rdf:RDF>
```

---

[Back to Table of Contents](../index.md)

[Previous Page: Subjects](subjects.md) | [Next Page: RDF in BIBFRAME](../rdf-in-bibframe/index.md)
