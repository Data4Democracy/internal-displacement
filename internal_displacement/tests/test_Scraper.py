import os
from unittest import TestCase

from sqlalchemy import create_engine

from internal_displacement.model.model import Session, Article
from internal_displacement.scraper import is_pdf_simple_tests, is_pdf_iframe_test, format_date, html_article


class TestScraper(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_pdf_simple_tests(self):
        url = "http://www.securitycouncilreport.org/atf/cf/%7B65BFCF9B-6D27-4E9C-8CD3-CF6E4FF96FF9%7D/S_2015_302.pdf"
        pdf_test = is_pdf_simple_tests(url)
        self.assertEqual(pdf_test, url)
        url = "http://www.independent.co.uk/news/world/asia/160-killed-and-hundreds-left-stranded-by-flooding-across-afghanistan-and-pakistan-8746566.html"
        self.assertFalse(is_pdf_simple_tests(url))

    def test_is_pdf_iframe_test(self):
        url = "http://erccportal.jrc.ec.europa.eu/getdailymap/docId/1125"
        pdf_test = is_pdf_iframe_test(url)
        self.assertEqual(
            pdf_test, "http://erccportal.jrc.ec.europa.eu/ERCmaps/ECDM_20150415_Natural_Disasters_Afghanistan_v02.pdf")
        url = "http://html.com/tags/iframe/"
        self.assertFalse(is_pdf_simple_tests(url))

    def test_format_date(self):
        date_string = 'Mon, 01 Jun 2015 16:25:25 GMT'
        formatted_date = format_date(date_string)
        self.assertEqual(formatted_date, '2015-06-01 16:25:25')
        date_string = '16:25:25 GMT'
        formatted_date = format_date(date_string)
        self.assertEqual(formatted_date, '')
        date_string = None
        formatted_date = format_date(date_string)
        self.assertEqual(formatted_date, '')


class TestFetch(TestCase):

    def setUp(self):
        DB_URL = os.environ.get('DB_URL')
        if not DB_URL.endswith('/id_test'):
            raise RuntimeError('Refusing to run tests against non-test database')
        engine = create_engine(DB_URL)
        Session.configure(bind=engine)
        self.session = Session()

    def tearDown(self):
        # self.session.rollback()
        pass


    def test_html(self):
        old = self.session.query(Article)\
            .filter_by(url='http://www.independent.co.uk/news/world/asia/160-killed-and-hundreds-left-stranded-by-flooding-across-afghanistan-and-pakistan-8746566.html')\
            .one_or_none()
        if old:
            self.session.delete(old)
        self.session.commit()
        article = html_article(
            self.session,
            'http://www.independent.co.uk/news/world/asia/160-killed-and-hundreds-left-stranded-by-flooding-across-afghanistan-and-pakistan-8746566.html')
        self.assertEquals(article.domain, 'http://www.independent.co.uk')
        self.assertRegexpMatches(article.content.content, 'Flash flood')

