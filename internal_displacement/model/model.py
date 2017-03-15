import os

from sqlalchemy import Table, text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Numeric
from sqlalchemy.orm import sessionmaker, relationship, object_session

Base = declarative_base()
Session = sessionmaker()


class Status:
    NEW = 'new'
    FETCHING = 'fetching'
    FETCHED = 'fetched'
    PROCESSING = 'processing'
    PROCESSED = 'processed'
    FETCHING_FAILED = 'fetching failed'
    PROCESSING_FAILED = 'prodessing failed'


class Category:
    OTHER = 'other'
    DISASTER = 'disaster'
    CONFLICT = 'conflict'


class UnexpectedArticleStatusException(Exception):
    def __init__(self, article, expected, actual):
        super(UnexpectedArticleStatusException, self).__init__(
            "Expected article {id} to be in state {expected}, but was in state {actual}".format(
                id=article.id, expected=expected, actual=actual
            ))


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    domain = Column(String)
    status = Column(String)
    title = Column(String)
    publication_date = Column(DateTime)
    authors = Column(String)
    language = Column(String(2))
    relevance = Column(Boolean)
    reliability = Column(Numeric)
    content = relationship('Content', uselist=False, back_populates='article', cascade="all, delete-orphan")
    reports = relationship('Report', back_populates='article', cascade="all, delete-orphan")
    categories = relationship('ArticleCategory', cascade="all, delete-orphan")

    def update_status(self, new_status):
        """
        Atomically Update the status of this Article from to new_status.
        If something changed the status of this article since it was loaded, raise.
        """
        session = object_session(self)
        if not session:
            raise RuntimeError("Object has not been persisted in a session.")

        expected_status = self.status
        result = session.query(Article).filter(Article.id == self.id, Article.status == self.status).update({
            Article.status: new_status
        })
        if result != 1:
            updated = session.query(Article).filter(Article.id == self.id).one()
            raise UnexpectedArticleStatusException(self, expected_status, updated.status)


class ArticleCategory(Base):
    __tablename__ = 'article_category'

    article_id = Column('article', Integer, ForeignKey('article.id'), primary_key=True)
    category = Column('category', String, primary_key=True)
    article = relationship('Article', back_populates='categories')


class Content(Base):
    __tablename__ = 'content'

    article_id = Column('article', Integer, ForeignKey('article.id'), primary_key=True)
    article = relationship('Article', back_populates='content')
    retrieval_date = Column(DateTime)
    content = Column(String)
    content_type = Column(String)


class Country(Base):
    __tablename__ = 'country'

    code = Column(String(2), primary_key=True)
    terms = relationship('CountryTerm', back_populates='country', cascade="all, delete-orphan")
    locations = relationship('Location', back_populates='country', cascade="all, delete-orphan")

    @classmethod
    def lookup(cls, session, code):
        return session.query(cls).filter_by(code=code).one()


class CountryTerm(Base):
    __tablename__ = 'country_term'

    term = Column(String, primary_key=True)
    code = Column('country', String(2), ForeignKey('country.code'))
    country = relationship('Country', back_populates='terms')


report_location = Table(
    'report_location', Base.metadata,
    Column('report', ForeignKey('report.id'), primary_key=True),
    Column('location', ForeignKey('location.id'), primary_key=True)
)


class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    code = Column('country', String(2), ForeignKey('country.code'))
    country = relationship('Country', back_populates='locations')
    latlong = Column(String)  # Not tackling PostGIS right now
    reports = relationship('Report', secondary=report_location, back_populates='locations')


class Report(Base):
    __tablename__ = 'report'

    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column('article', Integer, ForeignKey('article.id'), primary_key=True)
    article = relationship('Article', back_populates='reports')
    event_term = Column(String)
    subject_term = Column(String)
    quantity = Column(Integer)
    tag_locations = Column(String)
    accuracy = Column(Numeric)
    analyzer = Column(String)
    analysis_date = Column(DateTime)
    locations = relationship('Location', secondary=report_location, back_populates='reports')
    datespans = relationship('ReportDateSpan', back_populates='report', cascade="all, delete-orphan")


class ReportDateSpan(Base):
    __tablename__ = 'report_datespan'

    id = Column(Integer, primary_key=True)
    report_id = Column('report', Integer, ForeignKey('report.id'))
    report = relationship('Report', back_populates='datespans')
    start = Column(DateTime)
    finish = Column(DateTime)


def init_db(db_url, i_know_this_will_delete_everything=False):
    """
    Warning! This will delete everything in the database!
    :param session: SQLAlchemy session
    """
    if not i_know_this_will_delete_everything:
        raise RuntimeError("Tried to init_db without knowing it would delete everything!")
    engine = create_engine(db_url)
    Session.configure(bind=engine)
    session = Session()
    sql_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(sql_path, 'r') as schema:
        session.execute(text(schema.read()))
    session.commit()