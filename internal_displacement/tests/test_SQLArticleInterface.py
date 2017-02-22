from unittest import TestCase
from internal_displacement.pipeline import SQLArticleInterface
from internal_displacement.article import Article
import os
import datetime
import pandas as pd

class TestSQLArticleInterface(TestCase):

    def setUp(self):
        self.pipeline = SQLArticleInterface("testing_db.sqlite")
        self.date = datetime.datetime.now()

    def tearDown(self):
        os.remove("testing_db.sqlite")



    def test_insert_article(self):
        test_article = Article("test_content",self.date,"test_title","test_content_type",["test_author_1","test_author_2"],"www.butts.com","www.butts.com/disasters")
        test_article_date_string = test_article.get_pub_date_string()
        self.pipeline.insert_article(test_article)
        article_from_db = self.pipeline.sql_cursor.execute("SELECT * FROM Articles").fetchall()[0]
        db_title = article_from_db[0]
        self.assertEqual(db_title,"test_title")
        db_url = article_from_db[1]
        self.assertEqual(db_url,"www.butts.com/disasters")
        db_authors = article_from_db[2]
        self.assertEqual(db_authors,"test_author_1,test_author_2")
        db_publish_date = article_from_db[3]
        self.assertEqual(db_publish_date,test_article_date_string)
        db_domain = article_from_db[4]
        self.assertEqual(db_domain,"www.butts.com")
        db_text = article_from_db[5]
        self.assertEqual(db_text,"test_content")
        db_content_type = article_from_db[6]
        self.assertEqual(db_content_type,"test_content_type")
        db_language = article_from_db[7]
        self.assertEqual(db_language,"EN")


    def test_update_article(self):
        test_article = Article("test_content", self.date, "test_title", "test_content_type",
                               ["test_author_1", "test_author_2"], "www.butts.com", "www.butts.com/disasters")
        self.pipeline.insert_article(test_article)
        updated_article = test_article
        updated_article.change_language("EN")
        self.assertEqual(updated_article.language,"EN")
        self.pipeline.update_article(updated_article)
        db_article_language = self.pipeline.sql_cursor.execute("SELECT language FROM Articles").fetchone()[0]
        self.assertEqual(db_article_language,"EN")

    def test_to_csv(self):
        test_article = Article("test_content", self.date, "test_title", "test_content_type",
                               ["test_author_1", "test_author_2"], "www.butts.com", "www.butts.com/disasters")
        test_article_date_string = test_article.get_pub_date_string()
        self.pipeline.insert_article(test_article)
        self.pipeline.to_csv("Articles","testing_csv.csv")
        test_csv_df = pd.read_csv("testing_csv.csv")
        columns = ["title" , "url" ,"author" ,"publish_date" ,"domain" ,
                "content" , "content_type" , "language"]
        self.assertEqual(list(test_csv_df.columns),columns)
        csv_first_row_values = list(test_csv_df.values[0])
        expected_csv_row = ["test_content", test_article_date_string, "test_title", "test_content_type","test_author_1,test_author_2","www.butts.com","www.butts.com/disasters","EN"]
        self.assertCountEqual(csv_first_row_values,expected_csv_row) #FYI assertCountEqual actually asserts that lists contains the same values (independent of order) (poorly named method).
        self.assertEqual(csv_first_row_values[0],"test_title")
        self.assertEqual(csv_first_row_values[1],"www.butts.com/disasters")
        self.assertEqual(csv_first_row_values[2],"test_author_1,test_author_2")
        self.assertNotEqual(csv_first_row_values[2], "Mr Bananarama") #Sanity check.
        os.remove("testing_csv.csv")