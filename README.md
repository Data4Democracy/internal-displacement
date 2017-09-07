# Internal Displacement

**This repository is now archived. The project is being continued but is currently closed to new members.**
Data for Democracy is a community driven organization. If you want to start a new project in a similar area, you are welcome to do so! Check out the [#refugees](https://datafordemocracy.slack.com/messages/refugees/) channel and rally your fellow data nerds!

**Slack Channel:** [#internal-displacement](https://datafordemocracy.slack.com/messages/internal-displacement/)

**Project Description:**  Classifying, tagging, analyzing and visualizing news articles about [internal displacement](https://en.wikipedia.org/wiki/Internally_displaced_person). Based on a [challenge from the IDMC](https://unite.un.org/ideas/content/idetect).

The tool we are building carries out a number of functions:

1. Ingest a list of URLs
2. Scrape content from the respective web pages
3. Tag the article as relating to *disaster* or *conflict*
4. Extract key information from text
5. Store information in a database
6. Display data in interactive visualisations

The final aim is a simple app that can perform all of these functions with little technical knowledge needed by the user. 

**Project Lead:**  

- [@grichardson](https://datafordemocracy.slack.com/messages/@grichardson/)

**Maintainers:** These are the additional people mainly responsible for reviewing pull requests, providing feedback and monitoring issues.

Scraping, processing, NLP

- [@simonb](https://datafordemocracy.slack.com/messages/@simonb/)
- [@jlln](https://datafordemocracy.slack.com/messages/@jlln/)

Front end and infrastructure

- [@aneel](https://datafordemocracy.slack.com/messages/@aneel/)
- [@wwymak](https://datafordemocracy.slack.com/messages/@wwymak/)
- [@frenski](https://datafordemocracy.slack.com/messages/@frenski/)

## Getting started:

1. Join the [Slack channel]((https://datafordemocracy.slack.com/messages/internal-displacement/)).
2. Read the rest of this page and the [IDETECT challenge page](https://unite.un.org/ideas/content/idetect) to understand the project.
3. Check out our [issues](https://github.com/Data4Democracy/internal-displacement/issues) (small tasks) and [milestones](https://github.com/Data4Democracy/internal-displacement/milestones). Keep an eye out for `help-wanted`, `beginner-friendly`, and `discussion` tags. 
4. See something you want to work on? Make a comment on the issue or ping us on Slack to let us know.
5. Beginner with GitHub? Make sure you've read the [steps for contributing to a D4D project on GitHub](https://github.com/Data4Democracy/github-playground).
6. Write your code and submit a pull request to add it to the project. Reach out for help any time!

### Things you should know

* **Beginners are welcome!** We're happy to help you get started. *(For beginners with Git and GitHub specifically, our [github-playground](https://github.com/Data4Democracy/github-playground) repo and the [#github-help](https://datafordemocracy.slack.com/messages/github-help/) Slack channel are good places to start.)*
* **We believe good code is reviewed code.** All commits to this repository are approved by project maintainers and/or leads (listed above). The goal here is *not* to criticize or judge your abilities! Rather, sharing insights and achievements. Code reviews help us continually refine the project's scope and direction, and encourage discussion.
* **This README belongs to everyone.** If we've missed some crucial information or left anything unclear, edit this document and submit a pull request. We welcome the feedback! Up-to-date documentation is critical to what we do, and changes like this are a great way to make your first contribution to the project.

## Project Overview

There are millions of articles containing information about displaced people. Each of these is a rich source of information that can be used to analyse the flow of people and reporting about them. 

We are looking to record:

- URL
- Number of times URL has been submitted
- Main text
- Source (eg. new york times)
- Publication date
- Title
- Author(s)
- Language of article
- Reason for displacement (violence/disaster/both/other)
- The location where the displacement happened
- Reporting term: displaced/evacuated/forced to fee/homeless/in relief camp/sheltered/relocated/destroyed housing/partially destroyed housing/uninhabitable housing
- Reporting unit: people/persons/individuals/children/inhabitants/residents/migrants or families/households/houses/homes
- Number displaced
- Metrics relating to machine learning accuracy and reliability

### Project Components

These are the main parts and functions that make up the project.

* **Scraper and Pipeline**
 * Take lists of URLs as input from [input dataset](https://www.dropbox.com/s/c2vzdzrljlrn3y0/idmc_uniteideas_input_url.csv?dl=0)
 * Filter irrelevant articles and types of content (videos etc.)
 * Scrape the main body text and metadata (publish date, language etc.)
 * Store the information in a database
* **Interpreter**
 * Classify URLs as *conflict/violence*, *disaster* or *other*. There is a [training dataset](https://www.dropbox.com/s/50sgd3mztuhf5f6/training_dataset.csv?dl=0) to help with tagging.
 * Extract information from articles: location and number of reporting units (households or individuals) displaced, date published and reporting term (conflict/violence, disaster or other). The larger [extended input dataset](https://www.dropbox.com/s/2qt52uy1g3ci4rr/idmc_uniteideas_input_full.csv?dl=0) and the text from articles we have already scraped can be used to help here.
* **Visualizer**
 * A mapping tool to visualize the displacement figures and locations, identify hotspots and trends.
 * Other visualizations for a selected region to identify reporting frequency on the area
 * Visualizing the excerpts of documents where the relevant information is reported (either looking at the map or browsing the list of URLs).
 * Visualise relability of classification and information extraction algorithms (either overall or by article)
 * Some pre-tagged datasets ([1](https://www.dropbox.com/s/p42dq6gxvdugo3d/counts_displaced_idmc_uniteideas_input_full_conflict_tag.csv?dl=0), [2](https://www.dropbox.com/s/0h71jlfc5tmm7bk/counts_evacuation_idmc_uniteideas_input_full_conflict_tag.csv?dl=0)) can be used to start exploring visualization options.
* **App** is in the `internal-displacement-web` folder
 * A non-technical-user friendly front end to wrap around the components above for inputting URLs, managing the databases, verifying data and interacting with visualisations
 * Automation of scraping, pipeline and interpreter

### Running in Docker

You can run everything as you're accustomed to by installing dependencies locally, but
another option is to run in a Docker container. That way, all of the dependencies will
be installed in a controlled, reproducible way.

1. Install Docker: https://www.docker.com/products/overview

2. Run this command:

   ```
   docker-compose up
   ```

   or

   ```
   docker-compose -f docker-compose-spacy.yml up
   ```

   The `spacy` version will include the [en_core_web_md 1.2.1 NLP model](https://github.com/explosion/spacy-models)
   It is multiple gigabytes in size. The one without the model is much smaller.

   Either way, this will take some time the first time. It's fetching and building
   all of its dependencies. Subsequent runs should be much faster.

   This will start up several docker containers, running postgres, a Jupyter notebook server, and the node.js
   front end.

   In the output, you should see a line like:
   ```
   jupyter_1  |         http://0.0.0.0:3323/?token=536690ac0b189168b95031769a989f689838d0df1008182c
   ```

   That URL will connect you to the Jupyter notebook server.


4. Visit the node.js server at [http://localhost:3322](http://localhost:3322)

Note: You can stop the docker containers using Ctrl-C.

Note: If you already have something running on port 3322 or 3323, edit `docker-compose.yml` and change the first
number in the ports config to a free port on your system. eg. for 9999, make it:
```
    ports:
      - "9999:3322"
```

Note: If you want to add python dependencies, add them to `requirements.txt` and run the jupyter-dev version
of the docker-compose file:

```
docker-compose -f docker-compose-dev.yml up --build
```

You'll need to use the jupyter-dev version until your dependencies are merged to master and a new version is
built. Talk to @aneel on Slack if you need to do this.

Note: if you want to run SQL commands againt the database directly, you can do
that by starting a Terminal within Jupyter and running the PostgreSQL shell:

```
psql -h localdb -U tester id_test
```

Note: If you want to connect to a remote database, edit the `docker.env` file with the DB url for your remote database.


### Skills Needed

- **Python 3**
- **JavaScript/HTML/css**
- **Nodejs**
- **AWS**
- **Visualisation (D3)**

### Tips for working on this project

- Try to keep each contribution and pull request focussed mostly on solving the issue at hand. If you see more things that are needed, feel free to let us know and/or make another issue.
- Datasets can be accessed from [Dropbox](https://www.dropbox.com/sh/59lyts9d4ar1jcc/AADMyxDSQC_NGbpaPiuDGJ2ha?dl=0)
- We have a [working plan](workplan.md) for the project.
- Not ready to submit code to the main project? Feel free to play around with notebooks and submit them to the repository.


### Things that inspire us

[Refugees on IBM Watson News Explorer](http://news-explorer.mybluemix.net/?query=Refugees&type=unconstrained)
