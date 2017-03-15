import csv
from internal_displacement.article import Article
from internal_displacement.report import Report
from internal_displacement.interpreter import Interpreter
from internal_displacement.model.model import Status, Session, Category, Article, Content, Country, CountryTerm, \
    Location, Report, ReportDateSpan, ArticleCategory, Base
import concurrent
from concurrent import futures
import sqlite3
import pandas as pd
import numpy as np
import json
from datetime import datetime


"""
CSV Functions
"""


def csv_read(csvfile):
    '''
    Takes csv in the form of the training dataset and returns as list of lists
    representing each row.
    Parameters
    ----------
    csvfile: directory of csv file

    Returns
    -------
    dataset: dataset including header as list of lists
    '''
    with open(csvfile, 'r') as f:
        reader = csv.reader(f)
        dataset = list(reader)
    return dataset


def csv2dict(csvfile):
    '''
    Takes csv in the form of the training dataset and returns as list of
    ordered dictionaries each representing a row.
    Parameters
    ----------
    csvfile: directory of csv file

    Returns
    -------
    dataset: dataset including header as list of ordered dictionaries
    '''
    with open(csvfile, 'r') as f:
        reader = csv.DictReader(f)
        dataset = [line for line in reader]
    return dataset


def urls_from_csv(dataset, column=None, header=1):
    '''
    Takes csv in the form of the training dataset and returns list of URLs
    Parameters
    ----------
    csv: path to csv file containing urls
    column: integer number (0 indexed) or name of column with urls
            if not given, function will try to find column with urls
    header: used to index beginning of rows
            defaults to 1, assumes header present

    Returns
    -------
    urls: a list of URLs
    '''
    # if a column is given
    if column:
        # check whether it is a valid integer
        if isinstance(column, int) and column < len(dataset[0]):
            # take urls from that column
            urls = [line[column] for line in dataset[header:]]
        # if a column name is given, check header also selected and is present
        elif isinstance(column, str) and header == 1 and column in dataset[0]:
            # find the column index containing the string
            column = dataset[0].index(column)
            urls = [line[column] for line in dataset[header:]]
        elif isinstance(column, str) and header == 0:
            raise ValueError("Invalid use of column name."
                             "No header present in dataset.")
        elif isinstance(column, str) and column not in dataset[0]:
            raise ValueError("Invalid column name."
                             "Column name specified not in dataset."
                             "Please use a valid column name.")
        else:
            raise ValueError("Column index not in range of dataset."
                             "Please choose a valid column index.")
    # if no column specified, try to find by looking for
    elif column is None:
        first_row = dataset[header]
        index = [i for i, s in enumerate(first_row) if 'http' in s]
        urls = [line[index] for line in dataset[header:]]
    else:
        raise ValueError("Can't find any URLs!")

    return urls


def sample_urls(urls, size=0.25, random=True):
    '''Return a subsample of urls
    Parameters
    ----------
    size: float or int, default 0.25.
        If float, should be between 0.0 and 1.0 and is
        the size of the subsample of return. If int, represents
        the absolute size of the sample to return.

    random: boolean, default True
        Whether or not to generate a random or direct subsample.

    Returns
    -------
    urls_sample: subsample of urls as Pandas Series
    '''
    if isinstance(size, int) and size <= len(urls):
        sample_size = size
    elif isinstance(size, int) and size > len(urls):
        raise ValueError("Sample size cannot be larger than the"
                         " number of urls.")
    elif isinstance(size, float) and size >= 0.0 and size <= 1.0:
        sample_size = int(size * len(urls))
    else:
        raise ValueError("Invalid sample size."
                         " Please specify required sample size as"
                         " a float between 0.0 and 1.0 or as an integer.")

    if isinstance(random, bool):
        randomize = random
    else:
        raise ValueError("Invalid value for random."
                         " Please specify True or False.")

    if randomize:
        return np.random.choice(urls, sample_size)
    else:
        return urls[:sample_size]


class Pipeline(object):
    """
    Interface for article processing
    """

    def __init__(self, session, scraper, interpreter):
        self.session = session
        self.scraper = scraper
        self.interpreter = interpreter

    def process_url(self, url):
        # Create an article
        article = self.create_article(url)
        # Attempt to download the url and update article attributes
        self.fetch_article(article)
        if article.status == Status.FETCHING_FAILED:
            return Status.FETCHING_FAILED
        # Start processing
        article.update_status(Status.PROCESSING)
        # Check and update language
        self.check_language(article)
        if article.language != 'en':
            article.update_status(Status.PROCESSED)
            return "Processed: Not in English"
        # Try and extract reports
        self.fetch_reports(article)
        # Set the relevance status
        status = len(article.reports) > 0
        article.relevance = status
        self.session.commit()
        if not article.relevance:
            article.update_status(Status.PROCESSED)
            return "Processed: Not relevant"
        # TO DO: call the classifier and set the category
        article.update_status(Status.PROCESSED)
        return Status.PROCESSED

    def create_article(self, url):
        article = Article(url=url, status=Status.NEW)
        self.session.add(article)
        self.session.commit()
        return article

    def fetch_article(self, article):
        content, publish_date, title, content_type, authors, domain = self.scraper.scrape(
            article.url)
        if content == 'retrieval_failed':
            article.update_status(Status.FETCHING_FAILED)
        else:
            self.session.query(Article).filter(Article.id == article.id).\
                update({"domain": domain, "status": Status.FETCHED, "title": title, "publication_date": publish_date,
                        "authors": ", ".join(authors)})
            # Add the article content
            content = Content(article_id=article.id, retrieval_date=datetime.now(),
                              content=content, content_type=content_type)
            self.session.add(content)
            self.session.commit()

    def check_language(self, article):
        article.language = self.interpreter.check_language(
            article.content.content)
        self.session.commit()

    def fetch_reports(self, article):
        reports = self.interpreter.process_article_new(article.content.content)
        if len(reports) == 0:
            return
        for report in reports:
            self.process_report(article, report)

    def process_report(self, article, rep):
        report = Report(article_id=article.id, event_term=rep.event_term, subject_term=rep.subject_term,
                        quantity=0, tag_locations=json.dumps(rep.tag_spans),
                        analysis_date=datetime.now())
        self.session.add(report)
        self.session.commit()

        for location in rep.locations:
            self.process_location(report, location)

    def process_location(self, report, location):
        country_code = self.interpreter.country_code(location)
        if country_code:
            country = self.session.query(Country).filter_by(code=country_code).one_or_none() or Country(code=country_code)
            self.session.add(country)
            self.session.commit()
            location = Location(description=location, country=country)
            self.session.add(location)
            self.session.commit()
            report.locations.append(location)


class SQLArticleInterface(object):
    """
    Core SQL interface.
    """

    def __init__(self, sql_database_file):
        """
        Initialize an instance of SQLArticleInterface with the path to a SQL database file.
            - If the file does not exist it will be created.
            - If the file does exist, all previously stored data will be accessible through the object methods
        :param sql_database_file:   The path to the sql database file
        """
        self.sql_connection = sqlite3.connect(
            sql_database_file, isolation_level=None)
        self.sql_cursor = self.sql_connection.cursor()
        self.sql_cursor.execute(
            """CREATE TABLE IF NOT EXISTS Articles (title TEXT, url TEXT,author TEXT,publish_date TEXT,domain TEXT,
                content TEXT, content_type TEXT, language TEXT)""")
        self.sql_cursor.execute(
            "CREATE TABLE IF NOT EXISTS Labels (url TEXT,category TEXT)")

    def insert_article(self, article):
        """
        Inserts an article into the database.
        :param article:     An Article object
        """
        url = article.url
        authors = ",".join(article.authors)
        pub_date = article.get_pub_date_string()
        domain = article.domain
        content = article.content
        content_type = article.content_type
        title = article.title
        language = article.language
        reports = article.reports

        if article.content == "retrieval_failed":
            return None
        try:
            self.sql_cursor.execute("INSERT INTO Articles VALUES (?,?,?,?,?,?,?,?)",
                                    (title, url, authors, pub_date, domain, content, content_type, language))
            self.sql_connection.commit()
        except sqlite3.IntegrityError:
            print(
                "URL{url} already exists in article table. Skipping.".format(url))
        except Exception as e:
            print("Exception: {}".format(e))

        # Insert reports
        # Note: This may need to modify to work with sqlalchemy
        if len(reports) == 0:
            # If no reports, article is not relevant
            article.relevance = False
        elif language == 'en':
            # There are reports. Insert them if article is english
            for report in reports:
                try:
                    self.insert_report(report)
                except Exception as e:
                    print("Exception: {}".format(e))

    def update_article(self, article):
        """
        Updates certain fields of article in database
        Fields that can be updated are: language
        TODO: Do we want to update other fields like Reports here too?
        :param article:     An Article object
        """
        language = article.language
        url = article.url
        try:
            self.sql_cursor.execute("""UPDATE Articles SET language = ? WHERE url = ?""",
                                    (language, url))
            self.sql_connection.commit()
        except Exception as e:
            print("Exception: {}".format(e))

    def insert_report(self, report):
        '''
        Insert the given Report and its other relevant info to DB.
        (Note: this will need to be modified to use the sqlalchemy and the 
            updated schema from @aneel's #100 PR)
        :param report:      A Report schema object
        :param article:     An Article schema object
        '''
        try:
            self.sql_cursor.execute('''
            INSERT INTO REPORT VALUES (?,?,?,?,?,?,?,?,)''',
                                    (report.story, report.event_term, report.subject_term, report.quantity,
                                     report.tag_spans, report.accuracy, report.analyzer, report.analysis_date))

            for loc in report.locations:
                self.sql_cursor.execute('''
                INSERT INTO REPORT_LOCATION VALUES (?,?)''',
                                        (report, loc))

            for date_time in report.date_times:
                # (@domingohui Mar 9 2017) Need to revise how date spans work in Report
                self.sql_cursor.execute('''
                INSERT INTO REPORT_DATESPAN VALUES (?,?)''',
                                        (report, date_time))

        except Exception as e:
            print("Exception: {}".format(e))

    def process_urls(self, url_csv, url_column="URL", scrape_pdfs=True):
        """
        Populate the Articles SQL table with the data scraped from urls in a csv file.
        URLS that are already in the table will not be added again.
        Relies on scraper.scrape to handle extraction of data from an URL.

        :param url_csv:         Path to a csv file containing the URLs
        :param url_column:      The column of the csv file containing the URLs
        """
        dataset = csv_read(url_csv)
        urls = urls_from_csv(dataset, url_column)
        existing_urls = [r[0]
                         for r in self.sql_cursor.execute("SELECT url FROM Articles")]
        urls = [u for u in urls if u not in existing_urls]

        article_futures = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            interpreter = None  # To be initialized later
            for url in urls:
                article_futures.append(
                    executor.submit(scrape, url, scrape_pdfs))
            for f in concurrent.futures.as_completed(article_futures):
                try:
                    article = f.result()
                    if article is None:
                        continue
                    else:
                        print(article.title)
                        if interpreter is None:
                            # Lazy initialize Interpreter
                            interpreter = Interpreter()
                        # Obtain langugae of the article
                        article.language = interpreter.check_language(article)
                        # Obtain reports of the article
                        article.reports = interpreter.process_article_new(
                            article)
                        # Obtain codes of countries related to the article
                        article.country_codes = interpreter.extract_countries(
                            article)

                        self.insert_article(article)
                except Exception as e:
                    print("Exception: {}".format(e))

    def process_labeled_data(self, csv_filepath, url_column_name="URL", label_column_name="Tag"):
        """
        Populates the Labels SQL table. URLs that are already present in the table will not be added again.
        :param csv_filepath: path to a csv file containing labeled URLS.
        :param url_column_name: a string containing the name of the URL column name
        :param label_column_name: a string containing the name of the label column name

        """
        df = pd.read_csv(
            csv_filepath)  # For now just using pandas, but could replace with a custom function
        urls = list(df[url_column_name].values)
        existing_urls = [r[0]
                         for r in self.sql_cursor.execute("SELECT url FROM Labels")]
        urls = [u for u in urls if u not in existing_urls]
        labels = list(df[label_column_name].values)
        values = list(zip(urls, labels))
        self.sql_cursor.executemany("INSERT INTO Labels VALUES (?, ?)", values)
        self.sql_connection.commit()

    def to_csv(self, table, output):
        """
        Method to export SQL table to CSV file.
        :param table: The name of the table to export
        :param output: The path of the output file
        """
        try:
            data = self.sql_cursor.execute("SELECT * FROM " + table)
            headers = cursor = list(
                map(lambda x: x[0], self.sql_cursor.description))
        except ValueError:
            print("Not a valid table.")
        with open(output, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(data)

    def get_training_data(self):
        """
        Retrieves the labels and features for use in a classification task
        Returns:
            Two numpy arrays; one containing texts and one containing labels.
        """

        training_cases = self.sql_cursor.execute(
            "SELECT content,category FROM Articles INNER JOIN Labels ON Articles.url = Labels.url").fetchall()
        labels = [r[1] for r in training_cases]
        features = [r[0] for r in training_cases]
        return labels, features
