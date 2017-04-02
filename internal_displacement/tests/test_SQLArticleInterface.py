from unittest import TestCase
from internal_displacement.pipeline import SQLArticleInterface
from internal_displacement.article import Article
import os
import datetime
import pandas as pd

class TestSQLArticleInterface(TestCase):

    def setUp(self):
        pw = os.environ.get('TESTER_PASSWORD')
        if pw:
            self._POSTGRES = True
            db_url = f"postgresql://tester:{pw}@internal-displacement.cf1y5y4ffeey.us-west-2.rds.amazonaws.com/id_test"
            self.pipeline = SQLArticleInterface(db_url)
            schema = os.path.abspath(os.path.join(__file__, '..', '..', 'database', 'schema.sql'))
            self.pipeline.db.query_file(schema)
        else:
            self._POSTGRES = False
            self.pipeline = SQLArticleInterface("sqlite:///testing_db.sqlite")

        self.date = datetime.datetime.now()

    def tearDown(self):
        if self._POSTGRES:
            self.pipeline.db.close()
        else:
            os.remove("testing_db.sqlite")


    def test_insert_article(self):
        test_article = Article("test_content",self.date,"test_title","test_content_type",["test_author_1","test_author_2"],"www.butts.com","www.butts.com/disasters")
        test_article_date_string = test_article.get_pub_date_string()
        self.pipeline.insert_article(test_article)
        article_from_db = self.pipeline.db.query("SELECT * FROM Articles")[0]
        db_title = article_from_db.title
        self.assertEqual(db_title,"test_title")
        db_url = article_from_db.url
        self.assertEqual(db_url,"www.butts.com/disasters")
        db_authors = article_from_db.author
        self.assertEqual(db_authors,"test_author_1,test_author_2")
        db_publish_date = article_from_db[3]
        self.assertEqual(db_publish_date,test_article_date_string)
        db_domain = article_from_db[4]
        self.assertEqual(db_domain,"www.butts.com")
        db_text = article_from_db.content
        self.assertEqual(db_text,"test_content")
        db_content_type = article_from_db.content_type
        self.assertEqual(db_content_type,"test_content_type")
        db_language = article_from_db.language
        self.assertEqual(db_language,"EN")


    def test_update_article(self):
        test_article = Article("test_content", self.date, "test_title", "test_content_type",
                               ["test_author_1", "test_author_2"], "www.butts.com", "www.butts.com/disasters")
        self.pipeline.insert_article(test_article)
        updated_article = test_article
        updated_article.change_language("EN")
        self.assertEqual(updated_article.language,"EN")
        self.pipeline.update_article(updated_article)
        db_article_language = self.pipeline.db.query("SELECT language FROM Articles")[0].language
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
        csv_first_row_values[3] = dateutil.parser.parse(csv_first_row_values[3])
        expected_csv_row = ["test_content", self.date, "test_title", "test_content_type","test_author_1,test_author_2","www.butts.com","www.butts.com/disasters","EN"]
        self.assertCountEqual(csv_first_row_values,expected_csv_row) #FYI assertCountEqual actually asserts that lists contains the same values (independent of order) (poorly named method).
        self.assertEqual(csv_first_row_values[1],"test_title")
        self.assertEqual(csv_first_row_values[0],"www.butts.com/disasters")
        self.assertEqual(csv_first_row_values[2],"test_author_1,test_author_2")
        self.assertNotEqual(csv_first_row_values[2], "Mr Bananarama") #Sanity check.
        os.remove("testing_csv.csv")
