# Internal Displacement

**Slack Channel:** [#refugees](https://datafordemocracy.slack.com/messages/refugees/)

**Project Description:**  Classifying, tagging, analyzing and visualizing news events about [internal displacement](https://en.wikipedia.org/wiki/Internally_displaced_person). Based on a [challenge from the IDMC](https://unite.un.org/ideas/content/idetect). Our aim is to build a tool that can populate a database with displacement events which can be both classified by a machine and verified by a human. The details of each event are to be fed into a tool for analysis and visualization.

**Project Lead:**  

- [@grichardson](https://datafordemocracy.slack.com/messages/@grichardson/)

**Maintainers:** These are the additional people mainly responsible for reviewing pull requests, providing feedback and monitoring issues.
 
- [@simonb](https://datafordemocracy.slack.com/messages/@simonb/)

## Getting started:

1. Join the [Slack channel]((https://datafordemocracy.slack.com/messages/refugees/))
2. Read the pinned posts to get a full idea of the project.
* Browse our [issues](https://github.com/Data4Democracy/internal-displacement/issues) for `help-wanted`, `beginner-friendly`, and `discussion` tags (full issue label guide [here](https://github.com/Data4Democracy/assemble/blob/master/issue-labels-explained.md))
* See something you want to work on? Make a comment on the issue or ping us on Slack so we can assign you the task or discuss it. 
* Write the code and submit a pull request to add it to the project. Reach out for help any time!

### Tips

- Try to keep each contribution and pull request focussed mostly on solving the issue at hand. If you see more things that are needed, feel free to let us know and/or make another issue.
- Datasets can be accessed from [Dropbox](https://www.dropbox.com/sh/59lyts9d4ar1jcc/AADMyxDSQC_NGbpaPiuDGJ2ha?dl=0)
- Not ready to submit code to the main project? Feel free to play around with notebooks and submit them to the repository.

### Things you should know

* **"First-timers" are welcome!** Whether you're trying to learn data science, hone your coding skills, or get started collaborating over the web, we're happy to help. *(For beginners with Git and GitHub specifically, our [github-playground](https://github.com/Data4Democracy/github-playground) repo and the [#github-help](https://datafordemocracy.slack.com/messages/github-help/) Slack channel are good places to start.)*
* **We believe good code is reviewed code.** All commits to this repository are approved by project maintainers and/or leads (listed above). The goal here is *not* to criticize or judge your abilities! Rather, sharing insights and achievements. Code reviews help us continually refine the project's scope and direction, as well as encourage the discussion we need for it to thrive.
* **This README belongs to everyone.** If we've missed some crucial information or left anything unclear, edit this document and submit a pull request. We welcome the feedback! Up-to-date documentation is critical to what we do, and changes like this are a great way to make your first contribution to the project.


## Project Outline

The main components of the project:

* Scraping
 * Take lists of URLs and  and scrape the content of their web pages.
 * Extract the main body text and metadata
 * Store the information
* Machine Learning & NLP
 * Filter broken URLs in [master input dataset](https://www.dropbox.com/s/c2vzdzrljlrn3y0/idmc_uniteideas_input_url.csv?dl=0) and those containing non-useful data (videos etc.)
 * Classify URLs in [master input dataset](https://www.dropbox.com/s/c2vzdzrljlrn3y0/idmc_uniteideas_input_url.csv?dl=0) as conflict/violence, disaster or other. There is a [training dataset](https://www.dropbox.com/s/50sgd3mztuhf5f6/training_dataset.csv?dl=0) to help with tagging.
 * Extract information from articles within URLs: location and number of reporting units (households or individuals) displaced, date published and reporting term (conflict/violence, disaster or other). The larger [extended input dataset](https://www.dropbox.com/s/2qt52uy1g3ci4rr/idmc_uniteideas_input_full.csv?dl=0) can be used to help here.
* Visualize! 
 * A mapping tool is desired to visualize the displacement figures and locations, identify hotspots and trends.
 * Histogram or other visualization for a selected region to identify reporting frequency on the area
 * Taking into account only the documents that report actual displacement figures, visualize the excerpts of documents where the relevant information is reported (either looking at the map or browsing the list of URLs).
 * Some pre-tagged datasets ([1](https://www.dropbox.com/s/p42dq6gxvdugo3d/counts_displaced_idmc_uniteideas_input_full_conflict_tag.csv?dl=0), [2](https://www.dropbox.com/s/0h71jlfc5tmm7bk/counts_evacuation_idmc_uniteideas_input_full_conflict_tag.csv?dl=0)) can be used to start exploring visualization options.


### Current Skills and Languages
* Languages - Python 3
* Skills - NLP, ML, web scraping, geospatial, visualization

Don't see your skill here? Don't worry, we are looking to make all kinds of enhancements to the project so there will likely be a place for you. We especially need developer/web dev experience.