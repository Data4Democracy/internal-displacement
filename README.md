# Internal Displacement

**Slack:** #internal-displacement

**Project Description:**  
Classifying, tagging, analyzing and visualizing news events about internal displacement.

**Project Lead:**
[@grichardson](https://datafordemocracy.slack.com/messages/@grichardson/)

### Getting started:
* We welcome contributions from first timers
* Browse our help wanted issues. See if there is anything that interests you.
* Core maintainers and project leads are responsible for reviewing and merging all pull requests. In order to prevent frustrations with your first PR we recommend you reach out to our core maintainers who can help you through your first PR.
* Need to practice working with github in a group setting? Checkout [github-playground](https://github.com/Data4Democracy/github-playground)
* Updates to documentation or readme are greatly appreciated and make for a great first PR. They do not need to be discussed in advance and will be merged as soon as possible.

### Outline

The main components of the project:

* Machine Learning & NLP
 * Filter broken URLs in *"master input"* dataset and those containing non-useful data (videos etc.)
 * Classify URLs in *"master input"* dataset as `conflict/violence`, `disaster` or `other`. There is a *"training"* dataset to help with tagging.
 * Extract information from articles within URLs: location and number or households or individuals displaced, date published and reporting term*. The larger *"extended"* dataset can be used to help here.
* Visualize! 
 * A mapping tool is desired to visualize the displacement figures and locations, identify hotspots and trends.
 * Histogram or other visualization for a selected region to identify reporting frequency on the area
 * Taking into account only the documents that report actual displacement figures, visualize the excerpts of documents where the relevant information is reported (either looking at the map or browsing the list of URLs).


### Skills
* NLP, ML, geospatial, visualization, webdev

##### * Reporting Terms
* Displaced
* Evacuated
* Forced to Flee
* Homeless
* In Relief Camp
* Sheltered
* Relocated
* Destroyed Housing
* Partially Destroyed Housing
* Uninhabitable Housing

##### ** Reporting Units
**People**

* People
* Persons
* Individuals
* Children
* Inhabitants
* Residents
* Migrants

**Households**

* Families
* Households
* Houses
* Homes
