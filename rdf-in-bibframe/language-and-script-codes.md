# Language and script codes

Language and script encoding for non-Latin data fields will follow [BCP47](https://www.rfc-editor.org/info/rfc5646). BCP47 provides a pattern for defining language tags for use in a number of applications. It is the only means by which to record language in RDF. Using BCP47, it is possible to capture not just the language of string literal but also any geographic considerations, the script used, and even whether something has been transformed via romanization.

As a data consumer and producer, the Library of Congress will treat BCP47 codes in the following manner:

1)  Respect all the components of any incoming BCP47 codes by retaining any incoming BCP47 codes.

2)  Normalize BCP47 codes as follows:

    1.  Follow BCP47’s [IANA Registry](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry) for language codes. This means two-character, lowercase language codes are preferred; three-character, lowercase language codes are used when a two-character code is unavailable. Registry language codes include all of ISO 639-1, ISO 639-2, and ISO 639-3.

    2.  If “Suppress-script” is included in registry for a given language, it is respected.

    3.  If “Suppress-script” is NOT included in registry for a given language, a script code is required in the resulting BCP47 code.

    4.  Entire BCP47 code (i.e. all components) to lowercase.

3)  Regional (i.e. geographic) codes will be respected, but will be avoided when they otherwise do not add information.

Examples:

&nbsp;&nbsp;&nbsp;&nbsp;**en** *not* eng

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;“en” is the preferred two-character code for English

&nbsp;&nbsp;&nbsp;&nbsp;**ko** *not* ko-kore

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The script “kore” is assumed when the language is “ko” (Korean)

&nbsp;&nbsp;&nbsp;&nbsp;**zh-hant**, **zh-hani**, **zh-hans** *not* zh

> The Chinese language “zh” does not include a suppress-script instruction; per the rules outlined above, the script code needs to be included

&nbsp;&nbsp;&nbsp;&nbsp;**sr-cyrl** *not* sr

> The Serbian language “sr” can be expressed in two scripts – Cyrillic and Latin – and the BCP47 registry does not include a suppress-script instruction, meaning that the script must be included

These guidelines err on the side of caution, favoring clarity at the risk of wider interoperability. The fact that Simplified and Traditional Chinese can both use “zh” as a language code necessitates the addition of the script component (“hant” for Traditional Chinese, “hans” for Simplified Chinese, “hani” for both) to provide clarity even if, in more general implementations of BCP47, “zh” would alone be used. Most of the time the BCP47 codes used in BIBFRAME, however, will be those that would be used in a general application that also implements BCP47, thereby preferencing interoperability of our data outside our community.

---

[Back to Table of Contents](../index.md)

[Previous Page: Properties and classes overview](properties-and-classes-overview.md) | [Next Page: References](../references.md)
