import os
from datetime import datetime
from unittest import TestCase

from sqlalchemy import create_engine

from internal_displacement.model.model import Status, Session, Category, Article, Content, Country, CountryTerm, \
    Location, Report, ReportDateSpan, ArticleCategory, UnexpectedArticleStatusException


class TestModel(TestCase):
    def setUp(self):
        db_host = os.environ.get('DB_HOST')
        db_url = 'postgresql://{user}:{passwd}@{db_host}/{db}'.format(
            user='tester', passwd='tester', db_host=db_host, db='id_test')
        engine = create_engine(db_url)
        Session.configure(bind=engine)
        self.session = Session()

    def tearDown(self):
        self.session.rollback()
        self.session.query(Article).filter_by(domain='example.com').delete()
        self.session.commit()

    def test_article(self):
        article = Article(url='http://example.com',
                          domain='example.com',
                          status=Status.NEW)
        content = Content(article=article,
                          retrieval_date=datetime.now(),
                          content="La la la")
        ArticleCategory(article=article, category=Category.DISASTER)
        ArticleCategory(article=article, category=Category.OTHER)
        self.session.add(article)

        article2 = self.session.query(Article).filter_by(status=Status.NEW).one()
        self.assertEqual(article2.domain, 'example.com')
        self.assertEqual(article2.content.content, "La la la")
        self.assertCountEqual([c.category for c in article2.categories], ['disaster', 'other'])

        article3 = self.session.query(Article).filter_by(status=Status.NEW).one()
        self.assertEqual(article3.domain, 'example.com')

    def test_delete_article(self):
        article = None
        try:
            article = Article(url='http://example.com',
                              domain='example.com',
                              status=Status.NEW)
            content = Content(article=article,
                              retrieval_date=datetime.now(),
                              content="La la la")
            ArticleCategory(article=article, category=Category.DISASTER)
            ArticleCategory(article=article, category=Category.OTHER)
            self.session.add(article)
            self.session.commit()
            self.session.delete(article)
        finally:
            self.session.rollback()
            if article:
                self.session.delete(article)
            self.session.commit()

    def test_country_term(self):
        mmr = self.session.query(Country).filter_by(code="MMR").one_or_none() or Country(code="MMR")
        myanmar = CountryTerm(term="Myanmar", country=mmr)
        burma = CountryTerm(term="Burma", country=mmr)
        self.session.add(mmr)

        myanmar = self.session.query(Country).join(CountryTerm).filter_by(term='Myanmar').one()
        burma = self.session.query(Country).join(CountryTerm).filter_by(term='Burma').one()
        self.assertEqual(myanmar, burma)

    def test_location(self):
        mmr = self.session.query(Country).filter_by(code="MMR").one_or_none() or Country(code="MMR")
        naypyidaw = Location(description="Nay Pyi Taw",
                             city="Nay Pyi Taw",
                             region="Naypyitaw Union Territory",
                             country=mmr,
                             latlong='19°45′N 96°6′E')
        self.session.add(mmr)
        self.assertIn(naypyidaw, self.session.query(Location).filter_by(country=mmr))

    def test_report(self):
        article = None
        report = None
        mmr = self.session.query(Country).filter_by(code="MMR").one_or_none() or Country(code="MMR")
        bgd = self.session.query(Country).filter_by(code="BGD").one_or_none() or Country(code="BGD")
        try:
            article = Article(url='http://example.com',
                              domain='example.com',
                              status=Status.NEW)
            report = Report(article=article,
                            accuracy=0.55,
                            event_term='evacuation',
                            subject_term='family',
                            quantity='72')
            self.session.add(report)
            self.session.commit()  # have to commit here to get the ID set

            naypyidaw = Location(description="Nay Pyi Taw", country=mmr, latlong='19°45′N 96°6′E')
            report.locations.append(naypyidaw)
            dhaka = Location(description="Dhaka", country=bgd)
            report.locations.append(dhaka)
            now = datetime.now()
            when = ReportDateSpan(report=report, start=datetime.today(), finish=now)

            article2 = self.session.query(Article).filter_by(domain='example.com').first()
            self.assertEqual(len(article2.reports), 1)

            article3 = self.session.query(Article).join(Report).filter(Report.locations.contains(dhaka)).first()
            self.assertEqual(len(article3.reports), 1)
        finally:
            self.session.rollback()
            if report:
                self.session.delete(report)
            if article:
                self.session.delete(article)
            self.session.commit()

    def test_report_delete(self):
        article = None
        report = None
        mmr = self.session.query(Country).filter_by(code="MMR").one_or_none() or Country(code="MMR")
        bgd = self.session.query(Country).filter_by(code="BGD").one_or_none() or Country(code="BGD")
        try:
            article = Article(url='http://example.com',
                              domain='example.com',
                              status=Status.NEW)
            report = Report(article=article,
                            accuracy=0.55,
                            event_term='evacuation',
                            subject_term='family',
                            quantity='72')
            self.session.add(report)

            naypyidaw = Location(description="Nay Pyi Taw", country=mmr, latlong='19°45′N 96°6′E')
            report.locations.append(naypyidaw)
            dhaka = Location(description="Dhaka", country=bgd)
            report.locations.append(dhaka)
            now = datetime.now()
            when = ReportDateSpan(report=report, start=datetime.today(), finish=now)

            self.session.commit()
            report_id = report.id
            self.session.query(Report).filter_by(article=article).delete()
            report = None
            self.session.commit()
            self.assertEqual(self.session.query(ReportDateSpan).filter_by(report_id=report_id).all(), [])
        finally:
            self.session.rollback()
            if report:
                self.session.delete(report)
            if article:
                self.session.delete(article)
            self.session.commit()

    def test_status_update(self):
        article = Article(url='http://example.com',
                          domain='example.com',
                          status=Status.NEW)
        self.session.add(article)
        self.session.commit()

        article.update_status(Status.FETCHING)
        self.session.commit()
        self.assertEqual(article.status, Status.FETCHING)

        # meanwhile, some other process changed the status of this...
        self.session.execute("UPDATE article SET status = :status WHERE id = :id",
                             { 'status': Status.FETCHING_FAILED, 'id': article.id})

        with self.assertRaises(UnexpectedArticleStatusException):
            article.update_status(Status.FETCHED)
