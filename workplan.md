
### Raw Data
We already have certain datasets containing URLs.

__Activities:__
- *Do we need activities for obtaining more urls for our own dev / testing?*

### Scraping
To be moved to `info-sources` repo. Interested parties can contribute there.

__Activities:__
- Maintain some sort of link to `info-sources` to understand how these tools can be used / fit into the `internal-displacement` pipeline,  
i.e., function arguments, what they return, API type stuff.

### Filtering (Interpreter)

The first two could likely be part of 'Scraping', and returned as part of meta-data:

- Identify language of a document (English vs. not English)
- Broken URLs

The third filtering requirement is more specific to the `internal-displacement` domain:

- Filtering out documents not reporting on human mobility (binary classification)

__Activities:__
- Build classifier for binary classification of documents into relevant vs. not relevant (modeling)

+ *It is unclear to me if we have a training dataset for this part*
+ *This probably also needs to be trainable in the future through some type of online learning or larger datasets.*

### Tagging (Interpreter)

- Classification of documents into 3 classes (Disasters, Conflict & Violence, Other)

__Activities:__
- Select approach / model that will allow for online learning or re-training in the future with new datasets. (discussion)
- Build and train classifier for classifiying into the 3 required classes. (modeling)

### NLP

"Fact extraction" from documents:
- Publication date, locaction (ISO 3166 country codes) , reporting term, reporting units etc.

__Activities:__
- Select NLP tool or framework (discussion)
- Build and test working tool for extracting facts (modeling)

### Article Class

__Activities:__
- Define the properties each Article needs to have and fill out code for instantiating new Articles (beginner friendly)
- Define how to export / store articles (discussion):
    + My feeling is that some sort of Database will be necessary to facilitate the online / interactive tool for modeling and analysis
- Create / fill-out functions for update articles properties by calling and using return values from Scraper and Interpreter functions (beginner friendly)
- Fill out function for saving articles along with relevant properties (beginner friendly)

### Visualization

Including but not limited to Interactive Map, Histograms

__Activities:__
- Design of visualizations (data-viz)
- Selection of tool for online visualizations (i.e. D3) (discussion)
- Create visualization functions that take in data in standard format and produce desired and interactive visualizations (data-viz)

### Quantitative Analysis

Online tool that allows analysts to interact directly with data, choose what they visualize and how etc.

__Activities:__
- Design / build front-end page(s) for analysts
- Create back-end functionality for connecting to database and returning necessary data, facts etc.

### All Deliverables:

- URL to working version of the tool
- Source code repo
- Analysis of the test dataset
- User guide
- Admin guide

__Activities:__
- Create, maintain and update user guide (documentation)
- Create, maintain and update admin guide (documentation)


