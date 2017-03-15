from unittest import TestCase
from internal_displacement.interpreter import strip_words, Interpreter
from internal_displacement.scraper import Scraper
from sqlalchemy import create_engine

from internal_displacement.model.model import Status, Session, Category, Article, Content, Country, CountryTerm, \
    Location, Report, ReportDateSpan, ArticleCategory, UnexpectedArticleStatusException
from internal_displacement.pipeline import Pipeline
import spacy
import os


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

test_urls = [
    'http://www.independent.co.uk/news/somefakenewsstory',
    'http://www.eluniversal.com.mx/articulo/nacion/politica/2017/03/13/manifestantes-obligan-acortar-evento-de-amlo-en-ny',
    'http://www.bbc.com/news/world-europe-39258436',
    'http://www.independent.co.uk/news/world/asia/160-killed-and-hundreds-left-stranded-by-flooding-across-afghanistan-and-pakistan-8746566.html'
]


class TestPipeline(TestCase):

    def setUp(self):
        db_host = os.environ.get('DB_HOST')
        db_url = 'postgresql://{user}:{passwd}@{db_host}/{db}'.format(
           user='tester', passwd='tester', db_host=db_host, db='id_test')
        engine = create_engine(db_url)
        Session.configure(bind=engine)
        session = Session()
        scraper = Scraper()
        interpreter = Interpreter(nlp, person_reporting_terms, structure_reporting_terms,
                                  person_reporting_units, structure_reporting_units, relevant_article_lemmas, 'data/')
        self.pipeline = Pipeline(session, scraper, interpreter)
        self.session = session

    def tearDown(self):
        self.session.rollback()
        for url in test_urls:
            self.session.query(Article).filter_by(url=url).delete()
        self.session.commit()

    def test_bad_url(self):
        url = test_urls[0]
        response = self.pipeline.process_url(url)
        self.assertEqual(response, 'fetching failed')
        article = self.session.query(Article).filter_by(url=url).first()
        self.assertIsNone(article.content)

    def test_non_english_url(self):
        url = test_urls[1]
        response = self.pipeline.process_url(url)
        self.assertEqual(response, 'Processed: Not in English')
        article = self.session.query(Article).filter_by(url=url).first()
        self.assertEqual(len(article.reports), 0)
        self.assertEqual(article.status, Status.PROCESSED)

    def test_irrelevant(self):
        url = test_urls[2]
        response = self.pipeline.process_url(url)
        self.assertEqual(response, 'Processed: Not relevant')
        article = self.session.query(Article).filter_by(url=url).first()
        self.assertEqual(len(article.reports), 0)
        self.assertEqual(article.status, Status.PROCESSED)

    def test_good_url(self):
        url = test_urls[3]
        response = self.pipeline.process_url(url)
        self.assertEqual(response, 'processed')
        article = self.session.query(Article).filter_by(url=url).first()
        self.assertEqual(len(article.reports), 9)
        self.assertEqual(article.status, Status.PROCESSED)
        country_codes = set([
            location.country.code for report in article.reports for location in report.locations])
        self.assertIn('AFG', country_codes)
        self.assertIn('PAK', country_codes)
        terms = [report.event_term for report in article.reports]
        self.assertIn('collapse', terms)
        self.assertIn('strand', terms)
        units = [report.subject_term for report in article.reports]
        self.assertIn('villager', units)
        self.assertIn('house', units)
