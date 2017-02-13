# Internal Displacement

**Slack Channel:** [#internal-displacement](https://datafordemocracy.slack.com/messages/internal-displacement/)

**Project Description:**  Classifying, tagging, analyzing and visualizing news articles about [internal displacement](https://en.wikipedia.org/wiki/Internally_displaced_person). Based on a [challenge from the IDMC](https://unite.un.org/ideas/content/idetect). Our aim is to build a tool that can populate a database with displacement events from online news articles, which can be both classified by a machine, and then verified and analyzed by a human. 

We are using a Python back end to scrape, tag, classify and extract information from articles, which will be wrapped in a pretty UI, so that an analyst can interact with the data.

**Project Lead:**  

- [@grichardson](https://datafordemocracy.slack.com/messages/@grichardson/)

**Maintainers:** These are the additional people mainly responsible for reviewing pull requests, providing feedback and monitoring issues.
 
- [@simonb](https://datafordemocracy.slack.com/messages/@simonb/)
- [@jlln](https://datafordemocracy.slack.com/messages/@jlln/)

## Getting started:

1. Join the [Slack channel]((https://datafordemocracy.slack.com/messages/internal-displacement/)).
2. Read the rest of this page to understand the project.
* Browse the repository [issues](https://github.com/Data4Democracy/internal-displacement/issues) for `help-wanted`, `beginner-friendly`, and `discussion` tags.
* See something you want to work on? Before you start to work on it, make a comment under the issue or ping us on Slack so we can assign you the task or discuss it.
* Before writing any code, make sure you've read the [steps for contributing to a D4D project on GitHub](https://github.com/Data4Democracy/github-playground).
* Write your code and submit a pull request to add it to the project. Reach out for help any time!

### Things you should know

* **Beginners are welcome!** We're happy to help you get started. *(For beginners with Git and GitHub specifically, our [github-playground](https://github.com/Data4Democracy/github-playground) repo and the [#github-help](https://datafordemocracy.slack.com/messages/github-help/) Slack channel are good places to start.)*
* **We believe good code is reviewed code.** All commits to this repository are approved by project maintainers and/or leads (listed above). The goal here is *not* to criticize or judge your abilities! Rather, sharing insights and achievements. Code reviews help us continually refine the project's scope and direction, and encourage discussion.
* **This README belongs to everyone.** If we've missed some crucial information or left anything unclear, edit this document and submit a pull request. We welcome the feedback! Up-to-date documentation is critical to what we do, and changes like this are a great way to make your first contribution to the project.

## Project Overview and Progress

### Project Components

* **Scraper and Pipeline**
 * Take lists of URLs as input from [input dataset](https://www.dropbox.com/s/c2vzdzrljlrn3y0/idmc_uniteideas_input_url.csv?dl=0)
 * Filter irrelevant articles and types of content (videos etc.)
 * Scrape the main body text and metadata (publish date, language etc.)
 * Store the information in a database
* **Interpreter**
 * Classify URLs as *conflict/violence*, *disaster* or *other*. There is a [training dataset](https://www.dropbox.com/s/50sgd3mztuhf5f6/training_dataset.csv?dl=0) to help with tagging.
 * Extract information from articles within URLs: location and number of reporting units (households or individuals) displaced, date published and reporting term (conflict/violence, disaster or other). The larger [extended input dataset](https://www.dropbox.com/s/2qt52uy1g3ci4rr/idmc_uniteideas_input_full.csv?dl=0) and the text from articles we have already scraped can be used to help here.
* **Visualizer**
 * A mapping tool to visualize the displacement figures and locations, identify hotspots and trends.
 * Other visualizations for a selected region to identify reporting frequency on the area
 * Visualizing the excerpts of documents where the relevant information is reported (either looking at the map or browsing the list of URLs).
 * Visualise relability of 
 * Some pre-tagged datasets ([1](https://www.dropbox.com/s/p42dq6gxvdugo3d/counts_displaced_idmc_uniteideas_input_full_conflict_tag.csv?dl=0), [2](https://www.dropbox.com/s/0h71jlfc5tmm7bk/counts_evacuation_idmc_uniteideas_input_full_conflict_tag.csv?dl=0)) can be used to start exploring visualization options.
* **App**
 * A non-technical-user friendly front end to wrap around the components above for inputting URLs, managing the databases, verifying data and interacting with visualisations

### Progress

The flow chart below shows the main project aims and their level of completion:

- Green - mostly complete
- Amber - in progress/being explored
- Red - work not started
- (Gray text - non essential feature)

If you would like to help with any of the incomplete features, we'd love to have you on the team!

![](images/internal-displacement-plan.png?raw=true)

So far we have used **Python 3** for the internal engine of our application. 

We currently need people with skills in:

- **JavaScript/HTML/css** (making the UI)
- **Web frameworks - (django/nodejs, we’re undecided)** - (building the application)
- **AWS or other devops** - (automating and infrastructure)
- **Visualisation** - (visualise internal displacement crises and machine learning reliability)

### Tips for working on this project

- Try to keep each contribution and pull request focussed mostly on solving the issue at hand. If you see more things that are needed, feel free to let us know and/or make another issue.
- Datasets can be accessed from [Dropbox](https://www.dropbox.com/sh/59lyts9d4ar1jcc/AADMyxDSQC_NGbpaPiuDGJ2ha?dl=0)
- We have a [working plan](workplan.md) for the project.
- Not ready to submit code to the main project? Feel free to play around with notebooks and submit them to the repository.