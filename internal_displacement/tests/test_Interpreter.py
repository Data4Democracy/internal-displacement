from unittest import TestCase
from internal_displacement.interpreter import Interpreter
from internal_displacement.article import Article
from langdetect import detect
import pycountry
import spacy
import datetime


class TestInterpreter(TestCase):

    def setUp(self):
        self.pipeline = Interpreter()
        self.date = datetime.datetime.now()

    def tearDown(self):
        pass

    def test_check_language(self):
        test_article = Article("A decent amount of test content which will be used for extracting the language", \
                                self.date, "test_title", "test_content_type", [
                               "test_author_1", "test_author_2"], "www.butts.com", "www.butts.com/disasters")
        self.pipeline.check_language(test_article)
        article_language = test_article.language
        self.assertEqual(article_language, "en")

    def test_extract_countries(self):
        test_article = Article("United Kingdom plus Afghanistan", \
                                self.date, "test_title", "test_content_type", [
                               "test_author_1", "test_author_2"], "www.butts.com", "www.butts.com/disasters")
        countries = self.pipeline.extract_countries(test_article)
        self.assertIsInstance(countries, list)
        self.assertEqual(len(countries), 2)
        self.assertIn('GB', countries)
        self.assertIn('AF', countries)
        test_article = Article("No countries mentioned", \
                                self.date, "test_title", "test_content_type", [
                               "test_author_1", "test_author_2"], "www.butts.com", "www.butts.com/disasters")
        countries = self.pipeline.extract_countries(test_article)
        self.assertIsInstance(countries, list)
        self.assertEqual(len(countries), 0)