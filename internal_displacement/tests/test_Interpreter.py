from unittest import TestCase
from internal_displacement.interpreter import *
from internal_displacement.article import Article
from langdetect import detect
import pycountry
import spacy
import datetime


class TestInterpreter(TestCase):

    def setUp(self):
        self.pipeline = Interpreter(data_path='data')
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

    def test_strip_words(self):
        test_place_name = 'the province county district city'
        self.assertEqual(strip_words(test_place_name), '')
        test_place_name = 'the United States'
        self.assertEqual(strip_words(test_place_name), 'United States')

    def test_extract_countries(self):
        test_article = Article("The United Kingdom plus Afghanistan plus Sichuan Province, as well as Toronto, Cuba and Bosnia", \
                                self.date, "test_title", "test_content_type", [
                               "test_author_1", "test_author_2"], "www.butts.com", "www.butts.com/disasters")
        countries = self.pipeline.extract_countries(test_article)
        self.assertIsInstance(countries, list)
        self.assertEqual(len(countries), 6)
        self.assertIn('GB', countries)
        self.assertIn('AF', countries)
        self.assertIn('CN', countries)
        self.assertIn('CA', countries)
        self.assertIn('CU', countries)
        self.assertIn('BA', countries)
        test_article = Article("No countries mentioned", \
                                self.date, "test_title", "test_content_type", [
                               "test_author_1", "test_author_2"], "www.butts.com", "www.butts.com/disasters")
        countries = self.pipeline.extract_countries(test_article)
        self.assertIsInstance(countries, list)
        self.assertEqual(len(countries), 0)