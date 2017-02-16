## Approach to Fact Extraction Using Spacy

Following several weeks of experimentation, this document summarizes the current approach to extracting facts and reports from articles using the Spacy library.

### Reporting Terms and Units

As per the competition guildeines, fact extraction is based upon a set of core reporting terms, and reporting units.
There are two broad categories:

__Reporting Terms and Units Relating to People:__

```
person_reporting_terms = [
    'displaced', 'evacuated', 'forced flee', 'homeless', 'relief camp',
    'sheltered', 'relocated', 'stranded','stuck','stranded',"killed","dead","died"
]
person_reporting_units = ["families", "person", "people",
    "individuals", "locals", "villagers", "residents", "occupants", "citizens", "households"]
```

__Reporting Terms and Units Relating to Structures:__

```
structure_reporting_terms = [
    'destroyed', 'damaged', 'swept', 'collapsed', 'flooded', 'washed'
]
structure_reporting_units = ["home", "house", "hut", "dwelling",
    "building", "shop", "business", "apartment", "flat", "residence"]
```

In practice, each of these terms and units is lemmatized for comparison with tokens parsed from the article.

These terms and units can be updated as needed to ensure we are maximizing coverage of events referenced in articles.

---

### High Level Country Extraction

The competition guidelines require that each article be tagged with ISO 3166 country codes.
This is achieved using:
- Spacy library for named entity recognition
- Pycountry for mapping country names and subdivisions (states, provinces etc) to country codes
- JSON of cities -> country code for all cities with a population > 5,000 extracted from [www.geonames.org](www.geonames.org).

The procedure is:

1. Combine article title and contents and parse using Spacy to identify geographical named entities
2. Attempt to match the identified entity to a country code using the following steps in order:
    - Try a direct match for the entity against country names, common names and official names
    - Try to identify the country by comparing the entity to country subdivisions
    - Try to identify the country by seeing if the entity appears in the cities_to_countries JSON

---

### Report Extraction

The possible fields that a Report can have are:
- Referenced locations
- Referenced Date
- Reporting term (see above)
- Reporting unit (see above)
- Quantity

At a minimum, a Reporting Term and relevant Reporting Unit must be present in order to create an Article (the other fields can be blank / none).

The high-level procedure is:

1. Parse the article contents using Spacy and split into sentences
2. Process each sentence and attempt to identify:
    - Locations
    - Date
    - Reporting Term
    - Reporting Unit
    - Quantity
3. If the necessary reporting elements are correctly extracted, a Report is created
4. Multiple reports can be created for a given article

---

#### Location Identification

Sentence parsing to identify locations is based upon the following procedure:

- Examines the sentence and identify if any constituent tokens describe a location (based on Spacy named entity recognition)
- If a root token is specified, only location tokens below the level of this token in the tree will be examined.
- If no root is specified, location tokens will be drawn from the entirety of the span.

***Fallback location:***

- In many cases the event location may be referenced one or more sentences prior to the sentence containing the reporting term and unit.
- In order to deal with this, during article processing, a local variable is maintained for keeping track of the last extracted location.
- When a Report is extracted, if it has no specific location, then its location can be set to be the most recently identified prior location
- If a new location is extracted for a Report, then the local fallback location variable is updated

---

#### Date Identification

Sentence parsing to identify dates is based upon the following procedure:

- Examines the sentence and identify if any constituent tokens describe a date (based on Spacy named entity recognition)
- If a root token is specified, only location tokens below the level of this token in the tree will be examined.
- If no root is specified, location tokens will be drawn from the entirety of the span.

***Fallback date:***

- In many cases the event date may be referenced one or more sentences prior to the sentence containing the reporting term and unit.
- In order to deal with this, during article processing, a local variable is maintained for keeping track of the last extracted date.
- When a Report is extracted, if it has no specific date, then its date can be set to be the most recently identified prior date
- If a new date is extracted for a Report, then the local fallback date variable is updated

---

#### Reporting Term and Unit Identification

- Each sentence is split into tokens
- Each token is compared to reporting terms for both people and structures
- If a given token matches a reporting term:
    + Each branch below the token is examined to search for reporting units and numbers
    + If a reporting unit and number are identified, then a Report is created
    + If only a reporting unit (but no number) is identified, then look further up the tree above the reporting term to see if a number is present

***Special Cases:***

- In addition to this general procedure, there are also some special cases that can be more simply identified by looking at specific combinations of Reporting Terms and Reporting Units
- In some cases, these 'term-unit phrases' do not have a dependency within the parse tree that will be matched by the above algorithm i.e., 'families homeless'
- Should a specific phrase be encountered, then similar methods to above are used for extracting:
    + Location
    + Date
    + Number

---

### Required Enhancements

See [Issue #62](https://github.com/Data4Democracy/internal-displacement/issues/62)