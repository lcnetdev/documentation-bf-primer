# Properties and classes overview

## Datatype and object properties

Any BIBFRAME property is either a datatype property or an object property.

A **datatype** property always has a literal as its object.

&nbsp;&nbsp;&nbsp;&nbsp;Example: <https://id.loc.gov/resources/instances/23036180.html>

```xml
<rdf:RDF>
   <bf:Instance rdf:about="http://id.loc.gov/resources/instances/23036180">
    <bf:editionStatement>First edition</bf:editionStatement>
    <bf:dimensions>24 cm</bf:dimensions>
  </bf:Instance>
</rdf:RDF>
```

An **object** property has a resource as its object. The resource is either identified by a URI, or by a nodeID in the case of a blank node.

Example (identified by URI): <https://id.loc.gov/resources/works/23036180.html>

```xml
<rdf:RDF>
   <bf:Work rdf:about="http://id.loc.gov/resources/works/23036180">
    <bf:geographicCoverage>
      <bf:GeographicCoverage rdf:about="http://id.loc.gov/vocabulary/geographicAreas/n-us-va">
        <rdfs:label xml:lang="en">Virginia</rdfs:label>
      </bf:GeographicCoverage>
    </bf:geographicCoverage>
  </bf:Work>
</rdf:RDF>
```

Example (blank node): <https://id.loc.gov/resources/instances/in00024328013.html>

```xml
<rdf:RDF>
   <bf:Instance rdf:about="http://id.loc.gov/resources/instances/in00024328013">
    <bf:note>
      <bf:Note rdf:nodeID="n1">
        <rdfs:label>Includes index.</rdfs:label>
      </bf:Note>
    </bf:note>
  </bf:Instance>
</rdf:RDF>
```

NB: The above example shows the nodeID explicitly, but it can be, and is often, omitted as parsers will supply their own blank node identifier when absent.

For any BIBFRAME property, the object should not be a literal in one triple and a resource in another. The object should always be a literal, or it should always be a resource.

## URIs and labels

When referencing a resource, provide the URI, a label, or both. Object properties in BIBFRAME were created with the intention that either the resource, a label in lieu of the resource, or both can be supplied. BIBFRAME and RDF syntax enable the inclusion of these reference methods.

Example: <https://id.loc.gov/resources/works/23626846.html>

```xml
<rdf:RDF>
  <bf:Work rdf:about="http://id.loc.gov/resources/works/23626846">
    <bf:genreForm rdf:resource="http://id.loc.gov/authorities/genreForms/gf2014026339"/>
  </bf:Work>
</rdf:RDF>
```

Or

```xml
<rdf:RDF>
  <bf:Work rdf:about="http://id.loc.gov/resources/works/23626846">
    <bf:genreForm>
         <bf:GenreForm rdf:about="http://id.loc.gov/authorities/genreForms/gf2014026339">
        <rdfs:label xml:lang="en">Fiction</rdfs:label>
      </bf:GenreForm>
    </bf:genreForm>
  </bf:Work>
</rdf:RDF>
```

## URIs and blank nodes

BIBFRAME takes no position on the issue of a URI vs. a blank node. While it is recognized that URIs are linked-data friendly and blank nodes are not, both are acceptable in BIBFRAME and the usage of one or the other is an implementation decision.

&nbsp;&nbsp;&nbsp;&nbsp;Example: <https://id.loc.gov/resources/works/7973066.html>

```xml
<rdf:RDF>
  <bf:Work rdf:about="http://id.loc.gov/resources/works/7973066">
    <bf:subject>
      <bf:Topic rdf:about="http://id.loc.gov/authorities/subjects/sh85061232">
        <rdfs:label xml:lang="en">History, Ancient</rdfs:label>
      </bf:Topic>
    </bf:subject>
  </bf:Work>
</rdf:RDF>
```

Example: <https://id.loc.gov/resources/works/17002361.html>

```xml
<rdf:RDF>
  <bf:Work rdf:about="http://id.loc.gov/resources/works/17002361">
    <bf:subject>
      <bf:Topic>
        <rdfs:label>Ancient history</rdfs:label>
      </bf:Topic>
    </bf:subject>
  </bf:Work>
</rdf:RDF>
```

## Classes and types

Classes are generally used to indicate type. Identifiers, for example, have types such as ISBN, ISSN, LCCN, and variant titles have types such as abbreviated title, key title and parallel title.

In BIBFRAME, there is a single identifier property, bf:identifiedBy. Separate classes are defined for the different identifier types of bf:Isbn, bf:Issn, and bf:Lccn.

Advantages to representing type as a class rather than a property are:

- Reusability: For every identifier expressed in BIBFRAME, a resource is created. If it is created as a linked data resource, then it may be accessed and reused outside of BIBFRAME. Allowing the class to reflect the identifier source means that the source will be known when it is used as such. If the source is conveyed only by the BIBFRAME property, then that source will only be known when accessed in the BIBFRAME context.
- Query efficiency: Expressing types as classes often makes the data more easily queried. “Find things of type *X*” is simpler when *X* is a class rather than a property.
- Conciseness: Defining a single general property and using subclasses of a general class (when multiple potential properties have the same meaning) creates a more concise ontology. For instance, bf:AbbreviatedTitle and bf:KeyTitle are subclasses of bf:VariantTitle.
- Graceful degradation: Since non-BIBFRAME external namespaces can be used, introducing that namespace as a new class ensures that systems can recognize the data as a type of a BIBFRAME property.

## Formal constraints

Explicit domains and ranges for a property are generally not specified. Some exceptions to this practice include defining a domain of Work and a range of Instance for the property bf:hasInstance. In general, explicitly defined domains and ranges can have unintended, over-constraining effects.

For documentation purposes, properties are noted as “property of” and have an “expected value” to express the usual domain and range, but these are guidelines and are not enforced.

## Naming properties and classes

Class names are nouns and property names suggest verbs. In most cases, the prefix “has” is implied for properties, meaning that “hasTitle” is expressed as “title”.

## Reciprocal properties

For any BIBFRAME property, a reciprocal property should be defined, if appropriate. Whether or not the reciprocal property is used is an implementation decision.

## Using rdf: and rdfs: properties

Use rdf:value and rdfs:label as appropriate rather than defining additional properties.

Example: <https://id.loc.gov/resources/instances/20229412.html>

```xml
<rdf:RDF>
  <bf:Instance rdf:about="http://id.loc.gov/resources/instances/20229412">
    <bf:identifiedBy>
      <bf:Upc>
        <rdf:value>050087352431</rdf:value>
      </bf:Upc>
    </bf:identifiedBy>
    <bf:note>
      <bf:Note>
        <rdfs:label>Title from disc labels.</rdfs:label>
      </bf:Note>
    </bf:note>
  </bf:Instance>
</rdf:RDF>
```

---

[Back to Table of Contents](../index.md)

[Previous Page: RDF in BIBFRAME](index.md) | [Next Page: Language and script codes](language-and-script-codes.md)
