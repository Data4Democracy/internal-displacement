from unittest import TestCase
from internal_displacement.interpreter import strip_words, Interpreter
from internal_displacement.article import Article
from langdetect import detect
import pycountry
import spacy
import datetime

nlp = spacy.load("en")
person_reporting_terms = [
    'displaced', 'evacuated', 'forced', 'flee', 'homeless', 'relief camp',
    'sheltered', 'relocated', 'stranded', 'stuck', 'stranded', "killed", "dead", "died", "drown"
]

structure_reporting_terms = [
    'destroyed', 'damaged', 'swept', 'collapsed',
    'flooded', 'washed', 'inundated', 'evacuate'
]

person_reporting_units = ["families", "person", "people", "individuals", "locals", "villagers", "residents",
                          "occupants", "citizens", "households"]

structure_reporting_units = ["home", "house", "hut", "dwelling", "building", "shop", "business", "apartment",
                                     "flat", "residence"]

relevant_article_terms = ['Rainstorm', 'hurricane',
                          'tornado', 'rain', 'storm', 'earthquake']
relevant_article_lemmas = [t.lemma_ for t in nlp(
    " ".join(relevant_article_terms))]


class TestInterpreter(TestCase):

    def setUp(self):

        self.interpreter = Interpreter(nlp, person_reporting_terms, structure_reporting_terms,
                                       person_reporting_units, structure_reporting_units, relevant_article_lemmas, 'data/')
        self.date = datetime.datetime.now()

    def tearDown(self):
        pass

    def test_check_language(self):
        test_article = Article("A decent amount of test content which will be used for extracting the language",
                               self.date, "test_title", "test_content_type", [
                                   "test_author_1", "test_author_2"], "www.butts.com", "www.butts.com/disasters")
        language = self.interpreter.check_language(test_article.content)
        self.assertEqual(language, "en")

    def test_strip_words(self):
        test_place_name = 'the province county district city'
        self.assertEqual(strip_words(test_place_name), '')
        test_place_name = 'the United States'
        self.assertEqual(strip_words(test_place_name), 'United States')

    def test_extract_countries(self):
        test_article = Article("The United Kingdom plus Afghanistan plus Sichuan Province, as well as Toronto, Cuba and Bosnia",
                               self.date, "test_title", "test_content_type", [
                                   "test_author_1", "test_author_2"], "www.butts.com", "www.butts.com/disasters")
        countries = self.interpreter.extract_countries(test_article.content)
        self.assertIsInstance(countries, list)
        self.assertEqual(len(countries), 6)
        self.assertIn('GBR', countries)
        self.assertIn('AFG', countries)
        self.assertIn('CHN', countries)
        self.assertIn('CAN', countries)
        self.assertIn('CUB', countries)
        self.assertIn('BIH', countries)
        test_article = Article("No countries mentioned",
                               self.date, "test_title", "test_content_type", [
                                   "test_author_1", "test_author_2"], "www.butts.com", "www.butts.com/disasters")
        countries = self.interpreter.extract_countries(test_article)
        self.assertIsInstance(countries, list)
        self.assertEqual(len(countries), 0)
