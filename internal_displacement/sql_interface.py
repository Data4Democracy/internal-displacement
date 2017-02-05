from internal_displacement.scraper import scrape
from internal_displacement.article import Article
from internal_displacement.csv_tools import urls_from_csv, csv_read
import os
import json
import pandas as pd
import dateutil
import sqlite3
import numpy as np
import concurrent
from concurrent import futures
import itertools



class SQLArticleInterface(object):

    def __init__(self, sql_database_file):
        """
      Initialize an instance of URLArticlePipelineSQL with the path to a SQL database file.
            - If the file does not exist it will be created.
            - If the file does exist, all previously stored data will be accessible through the object methods
        :param sql_database_file:   The path to the sql database file
        """
        self.sql_connection = sqlite3.connect(sql_database_file, isolation_level=None)
        self.sql_cursor = self.sql_connection.cursor()
        self.sql_cursor.execute(
            "CREATE TABLE IF NOT EXISTS Articles (title TEXT, url TEXT,author TEXT,datetime TEXT,domain TEXT, content TEXT, content_type TEXT)")
        self.sql_cursor.execute("CREATE TABLE IF NOT EXISTS Labels (url TEXT,category TEXT)")

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
        try:
            self.sql_cursor.execute("INSERT INTO Articles VALUES (?,?,?,?,?,?,?)",
                                    (title, url, authors, pub_date, domain, content, content_type))
            self.sql_connection.commit()
        except sqlite3.IntegrityError:
            print("URL{url} already exists in article table. Skipping.".format(self.url))
        except Exception as e:
            print("Exception: {}".format(e))

    def process_urls(self, url_csv, url_column="URL"):
        """
        Populate the Articles SQL table with the data scraped from urls in a csv file. URLS that are already in the
        table will not be added again.
        Relies on scraper.scrape to handle extraction of data from an URL.

        :param url_csv:         Path to a csv file containing the URLs
        :param url_column:      The column of the csv file containing the URLs
        """
        dataset = csv_read(url_csv)
        urls = urls_from_csv(dataset, url_column)
        existing_urls = [r[0] for r in self.sql_cursor.execute("SELECT url FROM Articles")]
        urls = [u for u in urls if u not in existing_urls]

        article_futures = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for url in urls:
                article_futures.append(executor.submit(scrape, url))
            for f in concurrent.futures.as_completed(article_futures):
                try:
                    article = f.result()
                    if article is None:
                        continue
                    else:
                        print(article.title)
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
        df = pd.read_csv(csv_filepath) # For now just using pandas, but could replace with a custom function
        urls = list(df[url_column_name].values)
        existing_urls = [r[0] for r in self.sql_cursor.execute("SELECT url FROM Labels")]
        urls = [u for u in urls if u not in existing_urls]
        labels = list(df[label_column_name].values)
        values = list(zip(urls, labels))
        self.sql_cursor.executemany("INSERT INTO Labels VALUES (?, ?)", values)
        self.sql_connection.commit()

    def get_training_data(self):
        """
        Retrieves the labels and features for use in a classification task
        Returns:
            Two numpy arrays; one containing texts and one containing labels.
        """

        training_cases = self.sql_cursor.execute(
            "SELECT content,category FROM Articles INNER JOIN Labels ON Articles.url = Labels.url")
        labels = np.array([r[1] for r in training_cases])
        features = np.array(r[0] for r in training_cases)
        return labels, features


