from unittest import TestCase
from internal_displacement.pipeline import SQLArticleInterface
from internal_displacement.article import Article
import os
import datetime
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
        db_datetime = article_from_db[3]
        self.assertEqual(db_datetime,test_article_date_string)
        db_domain = article_from_db[4]
        self.assertEqual(db_domain,"www.butts.com")
        db_text = article_from_db[5]
        self.assertEqual(db_text,"test_content")
        db_content_type = article_from_db[6]
        self.assertEqual(db_content_type,"test_content_type")
        db_language = article_from_db[7]
        self.assertEqual(db_language,"")


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