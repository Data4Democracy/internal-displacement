from internal_displacement.scraper import Scraper
from internal_displacement.article import Article
from internal_displacement.csv_tools import urls_from_csv,csv_read
import os
import json
import pandas as pd
import dateutil
import sqlite3

"""
A pipeline to facilitate the extraction and storage of data from URLS.
Purpose:
    - Ensure articles are only ever scraped once.
    - Facilitate ingestion of articles (which may or may not be labeled with a category)
    - Allow storage of features (ie text) extracted from articles
    - Allow storage of labels for training cases
    - Allow retrieval of labeled features for training.
    - Uses two SQL tables
        - one containing information common to all articles (ie all features except labels)
        - one containing the labels for training cases
    - Tables use URL as the primary key.
    - Training data can be retrieved by doing an inner join.
"""


class URLArticlePipeline(object):

    #Class Functions#

    def __init__(self, sql_database_file):
        """
        :param sql_database_file:   The path to the sql database file
        """
        self.sql_connection = sqlite3.connect(sql_database_file,isolation_level=None)
        self.sql_cursor = self.sql_connection.cursor()
        self.sql_cursor.execute("CREATE TABLE IF NOT EXISTS Articles (url TEXT,author TEXT,datetime TEXT,domain TEXT, content TEXT, content_type TEXT)")
        self.sql_cursor.execute("CREATE TABLE IF NOT EXISTS Labels (url TEXT,category TEXT)")


    def process_urls(self,url_csv,url_column = "URL",label_column=None):
        """
        Could make this multithreaded - collect the sql insertion strings in parallel then execute them all together.
        :param url_csv:         The csv file containing the URLs (and maybe the labels)
        :param url_column:      The column containing the URLs
        :param label_column:    Optional - the column containing the labels.
        :return:
        """
        dataset = csv_read(url_csv)
        urls = urls_from_csv(dataset,url_column,label_column)
        if label_column:
            for url,label in urls:
                print(url)
                article = Scraper.html_report(self,url)
                article.insert_into_sql_table(self.sql_cursor)
                self.sql_connection.commit()
                try:
                    self.sql_cursor.execute("INSERT INTO Labels VALUES(?,?)",(url,label))
                    self.sql_connection.commit()
                except sqlite3.IntegrityError:
                    print("URL{url} already exists in labels table. Skipping.".format(self.url))
                except Exception as e:
                    print("Exception: {}".format(e))
        else:
            for url in urls:
                article = Scraper.html_report(self, url)
                article.insert_into_sql_table(self.sql_cursor)






















d = "/home/james/Documents/DataForDemocracy/internal-displacement/internal-displacement/datasets/IDMC Unite Ideas - Training dataset - TrainingDataset.csv"

url_pipe = URLArticlePipeline("sql_db.sqlite")
url_pipe.process_urls(d,label_column="Tag")
# urls = [d.URL.values[1]]
# print(urls)
# up = URLArticlePipeline(urls)
# up.save_articles_to_json_files("test_storage")
#
# up2 = URLArticlePipeline([])
# up2.load_articles_from_json_files("test_storage")
# for article in up2.articles:
#     print(article.authors)
#     print(article.domain)




