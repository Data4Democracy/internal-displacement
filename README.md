# Internal Displacement

**Slack:** #internal-displacement

**Project Description:**  
Classifying, tagging, analyzing and visualizing news events about internal displacement. Based on a [challenge from the IDMC](https://unite.un.org/ideas/content/idetect).

**Project Lead:**
[@grichardson](https://datafordemocracy.slack.com/messages/@grichardson/)

**Maintainers:**
[@simonb](https://datafordemocracy.slack.com/messages/@simonb/)

### Getting started:
* We welcome contributions from first timers
* Browse our help wanted issues. See if there is anything that interests you.
* Core maintainers and project leads are responsible for reviewing and merging all pull requests. In order to prevent frustrations with your first PR we recommend you reach out to our core maintainers who can help you through your first PR.
* Need to practice working with github in a group setting? Checkout [github-playground](https://github.com/Data4Democracy/github-playground)
* Updates to documentation or readme are greatly appreciated and make for a great first PR. They do not need to be discussed in advance and will be merged as soon as possible.
* Datasets can be accessed from [Dropbox](https://www.dropbox.com/sh/59lyts9d4ar1jcc/AADMyxDSQC_NGbpaPiuDGJ2ha?dl=0)

### Outline

The main components of the project:

* Machine Learning & NLP
 * Filter broken URLs in [master input dataset](https://www.dropbox.com/s/c2vzdzrljlrn3y0/idmc_uniteideas_input_url.csv?dl=0) and those containing non-useful data (videos etc.)
 * Classify URLs in [master input dataset](https://www.dropbox.com/s/c2vzdzrljlrn3y0/idmc_uniteideas_input_url.csv?dl=0) as conflict/violence, disaster or other. There is a [training dataset](https://www.dropbox.com/s/50sgd3mztuhf5f6/training_dataset.csv?dl=0) to help with tagging.
 * Extract information from articles within URLs: location and number of reporting units (households or individuals) displaced, date published and reporting term (conflict/violence, disaster or other). The larger [extended input dataset](https://www.dropbox.com/s/2qt52uy1g3ci4rr/idmc_uniteideas_input_full.csv?dl=0) can be used to help here.
* Visualize! 
 * A mapping tool is desired to visualize the displacement figures and locations, identify hotspots and trends.
 * Histogram or other visualization for a selected region to identify reporting frequency on the area
 * Taking into account only the documents that report actual displacement figures, visualize the excerpts of documents where the relevant information is reported (either looking at the map or browsing the list of URLs).
 * Some pre-tagged datasets ([1](https://www.dropbox.com/s/p42dq6gxvdugo3d/counts_displaced_idmc_uniteideas_input_full_conflict_tag.csv?dl=0), [2](https://www.dropbox.com/s/0h71jlfc5tmm7bk/counts_evacuation_idmc_uniteideas_input_full_conflict_tag.csv?dl=0)) can be used to start exploring visualization options.


### Skills
* NLP, ML, web scraping, geospatial, visualization, webdev
