import csv
from internal_displacement.interpreter import Interpreter
from internal_displacement.model.model import Status, Session, Category, Article, Content, Country, CountryTerm, \
    Location, Report, ReportDateSpan, ArticleCategory, Base
import concurrent
from concurrent import futures
import sqlite3
import pandas as pd
import numpy as np
import json
from datetime import datetime
import requests
from itertools import *


"""
CSV Functions
"""


def csv_read(csvfile):
    '''
    Takes csv in the form of the training dataset and returns as list of lists
    representing each row.
    Parameters
    ----------
    csvfile: directory of csv file

    Returns
    -------
    dataset: dataset including header as list of lists
    '''
    with open(csvfile, 'r') as f:
        reader = csv.reader(f)
        dataset = list(reader)
    return dataset


def csv2dict(csvfile):
    '''
    Takes csv in the form of the training dataset and returns as list of
    ordered dictionaries each representing a row.
    Parameters
    ----------
    csvfile: directory of csv file

    Returns
    -------
    dataset: dataset including header as list of ordered dictionaries
    '''
    with open(csvfile, 'r') as f:
        reader = csv.DictReader(f)
        dataset = [line for line in reader]
    return dataset


def urls_from_csv(dataset, column=None, header=1):
    '''
    Takes csv in the form of the training dataset and returns list of URLs
    Parameters
    ----------
    csv: path to csv file containing urls
    column: integer number (0 indexed) or name of column with urls
            if not given, function will try to find column with urls
    header: used to index beginning of rows
            defaults to 1, assumes header present

    Returns
    -------
    urls: a list of URLs
    '''
    # if a column is given
    if column:
        # check whether it is a valid integer
        if isinstance(column, int) and column < len(dataset[0]):
            # take urls from that column
            urls = [line[column] for line in dataset[header:]]
        # if a column name is given, check header also selected and is present
        elif isinstance(column, str) and header == 1 and column in dataset[0]:
            # find the column index containing the string
            column = dataset[0].index(column)
            urls = [line[column] for line in dataset[header:]]
        elif isinstance(column, str) and header == 0:
            raise ValueError("Invalid use of column name."
                             "No header present in dataset.")
        elif isinstance(column, str) and column not in dataset[0]:
            raise ValueError("Invalid column name."
                             "Column name specified not in dataset."
                             "Please use a valid column name.")
        else:
            raise ValueError("Column index not in range of dataset."
                             "Please choose a valid column index.")
    # if no column specified, try to find by looking for
    elif column is None:
        first_row = dataset[header]
        index = [i for i, s in enumerate(first_row) if 'http' in s]
        urls = [line[index] for line in dataset[header:]]
    else:
        raise ValueError("Can't find any URLs!")

    return urls


def sample_urls(urls, size=0.25, random=True):
    '''Return a subsample of urls
    Parameters
    ----------
    size: float or int, default 0.25.
        If float, should be between 0.0 and 1.0 and is
        the size of the subsample of return. If int, represents
        the absolute size of the sample to return.

    random: boolean, default True
        Whether or not to generate a random or direct subsample.

    Returns
    -------
    urls_sample: subsample of urls as Pandas Series
    '''
    if isinstance(size, int) and size <= len(urls):
        sample_size = size
    elif isinstance(size, int) and size > len(urls):
        raise ValueError("Sample size cannot be larger than the"
                         " number of urls.")
    elif isinstance(size, float) and size >= 0.0 and size <= 1.0:
        sample_size = int(size * len(urls))
    else:
        raise ValueError("Invalid sample size."
                         " Please specify required sample size as"
                         " a float between 0.0 and 1.0 or as an integer.")

    if isinstance(random, bool):
        randomize = random
    else:
        raise ValueError("Invalid value for random."
                         " Please specify True or False.")

    if randomize:
        return np.random.choice(urls, sample_size)
    else:
        return urls[:sample_size]


"""
Coordinates extraction functions
"""

def get_coordinates_mapzen(city=None, subdivision=None, country=None, hints=[]):
    '''Return geo coordinates by supplying location name
    Parameters
    ----------
    city: string, default None
    subdivision: string, default None
    country: string, default None
    hints: array, default [], other locations mentioned in the text that might
           help identify the proper location 

    Returns
    -------
    coordinates: string of comma separated lat an long
    '''
    
    def coords_tostring(coords_list, separator=','):
        return separator.join(map(str,coords_list))
    
    api_key = 'mapzen-neNu6xZ'
    base_url = 'https://search.mapzen.com/v1/search'
    
    # turns all empty entities to none
    place_units = [city, subdivision, country]
    for unit in place_units:
        if unit == '':
            unit == None
    
    # creates the extra parameter in order to make sure
    # we are looking for the correct type of location    
    place_layers = 'locality'
    if city is None:
        place_layers = 'region'
        if subdivision is None:
            place_layers = 'country'
    
    # creates the text parameter
    place_name = ','.join([p for p in place_units if p is not None])

    # makes a call to mapzen an retrieves the data
    qry = {'text': place_name, 'api_key': api_key}
    resp = requests.get(base_url, params = {'api_key': api_key, 
                                            'text': place_name,
                                            'layers':place_layers})
    res = resp.json()
    data = res["features"]

    # if there are no results from the call ...
    if len(data) == 0:
	    return {u'coordinates':'', u'flag':"no-results"}
    # best case - there is just a single result ...
    elif len(data) == 1:
        return {u'coordinates':coords_tostring(data[0]['geometry']['coordinates']),
                u'flag':"single-result"}
    # most complicated case - there are multiple results
    elif len(data) > 1:
        # if there are hints, ry to make a best guess and 
        # and if not - returns the first result in the list
        data_filt = [data]
        if len(hints) > 0:
            layers_mapzen = {0:'locality', 1:'region', 2:'country'}
            hints.append ('')
            # creates a new list with indices of all missing items in 
            # the places list
            miss_idx = [i for i,v in enumerate(place_units) if v is None]
            # creates a list of all the possible combinations
            combs = list(permutations(hints, len(miss_idx)))
            for comb in combs:
                c = 0
                for i, idx in enumerate(miss_idx):
                    if comb[i] != '':
                        # filters the dictionary based on the different options
                        if c==0:
                            # if it's a first valid iteration, the data source is
                            # basically the raw dictionary
                            data_filt.append([l for l in data 
                                if layers_mapzen[idx] in l['properties'] 
                                and l['properties'][layers_mapzen[idx]] == comb[i]])
                        else:
                            # if it's one of the later tierations, the data source
                            # is the newly created filtered dictionary
                            data_filt[-1] = [l for l in data_filt[-1] 
                                if layers_mapzen[idx] in l['properties'] 
                                and l['properties'][layers_mapzen[idx]] == comb[i]]
                        c += 1
                
            # trying to get the best match (minimum number of results gt zero)
            # creating a list with all the options filtered
            data_filt = [d for d in data_filt if len(d) > 0]
            data_filt = sorted(data_filt, key=lambda k: len(k))
        coords = coords_tostring(data_filt[0][0]['geometry']['coordinates'])
        return {u'coordinates': coords, u'flag':"multiple-results"}


class Pipeline(object):
    """
    Interface for article processing
    """

    def __init__(self, session, scraper, interpreter):
        self.session = session
        self.scraper = scraper
        self.interpreter = interpreter

    def process_url(self, url):
        # Create an article
        article = self.create_article(url)
        # Attempt to download the url and update article attributes
        self.fetch_article(article)
        if article.status == Status.FETCHING_FAILED:
            return Status.FETCHING_FAILED
        # Start processing
        article.update_status(Status.PROCESSING)
        # Check and update language
        self.check_language(article)
        if article.language != 'en':
            article.update_status(Status.PROCESSED)
            return "Processed: Not in English"
        # Try and extract reports
        self.fetch_reports(article)
        # Set the relevance status
        status = len(article.reports) > 0
        article.relevance = status
        self.session.commit()
        if not article.relevance:
            article.update_status(Status.PROCESSED)
            return "Processed: Not relevant"
        # Get the dates and set the datespans for all reports
        self.fetch_dates(article)
        # Categorize the article
        self.categorize(article)
        article.update_status(Status.PROCESSED)
        return Status.PROCESSED

    def create_article(self, url):
        '''Create an article from a provided url.
        '''
        article = Article(url=url, status=Status.NEW)
        self.session.add(article)
        self.session.commit()
        return article

    def fetch_article(self, article):
        '''Attempt to download and parse article.
        Update status and add content to database (if successful).
        '''
        content, publish_date, title, content_type, authors, domain = self.scraper.scrape(
            article.url)
        if content == 'retrieval_failed':
            article.update_status(Status.FETCHING_FAILED)
        else:
            self.session.query(Article).filter(Article.id == article.id).\
                update({"domain": domain, "status": Status.FETCHED, "title": title, "publication_date": publish_date,
                        "authors": ", ".join(authors)})
            # Add the article content
            content = Content(article_id=article.id, retrieval_date=datetime.now(),
                              content=content, content_type=content_type)
            self.session.add(content)
            self.session.commit()

    def check_language(self, article):
        '''Check article language and update attribute.
        '''
        article.language = self.interpreter.check_language(
            article.content.content)
        self.session.commit()

    def categorize(self, article, text='content'):
        if text == 'content':
            category = self.interpreter.classify_category(
                article.content.content, text=text)
        elif text == 'title':
            category = self.interpreter.classify_category(
                article.title, text=text)
        category = ArticleCategory(category=category)
        self.session.add(category)
        self.session.commit()

    def fetch_reports(self, article):
        '''Fetch reports for a given article.
        '''
        reports = self.interpreter.process_article_new(article.content.content)
        if len(reports) == 0:
            return
        for report in reports:
            self.process_report(article, report)

    def process_report(self, article, rep):
        '''Create Reports for each extracted report.
        Add locations and date-spans.
        '''
        report = Report(article_id=article.id, event_term=rep.event_term, subject_term=rep.subject_term,
                        quantity=rep.quantity, tag_locations=json.dumps(
                            rep.tag_spans),
                        analysis_date=datetime.now())
        self.session.add(report)
        self.session.commit()

        for location in rep.locations:
            self.process_location(report, location)

    def fetch_dates(self, article):
        '''Fetch all dates referred to in the article
        and update all article reports'''
        date_times = self.interpreter.extract_all_dates(
            article.content.content, article.publication_date)
        if len(date_times) > 0:
            start = min(date_times)
            finish = max(date_times)
            self.set_datespans(article, start, finish)
        elif article.publication_date:
            self.set_datespans(
                article, article.publication_date, article.publication_date)

    def set_datespans(self, article, start, finish):
        '''Set the datespans for all reports in an article.'''
        for report in article.reports:
            date_span = ReportDateSpan(
                report_id=report.id, start=start, finish=finish)
            self.session.add(date_span)
            self.session.commit()
            report.datespans.append(date_span)

    def process_location(self, report, location):
        '''Process each location.
        If location already exists, use existing location.
        Otherwise create new location.
        '''
        loc = self.session.query(Location).filter_by(
            description=location).one_or_none()
        if loc:
            report.locations.append(loc)
        else:
            loc_dict = self.interpreter.city_subdivision_country(location)
            if loc_dict:
                country = self.session.query(Country).filter_by(
                    code=loc_dict['country']).one_or_none()
                latlong = get_coordinates_mapzen(loc_dict['city'],
											    loc_dict['subdivision'],
												loc_dict['country'])
                location = Location(description=location,
                                    city=loc_dict['city'],
                                    subdivision=loc_dict['subdivision'],
                                    country=country,
                                    latlong=latlong.coordinates)
                self.session.add(location)
                self.session.commit()
                report.locations.append(location)

    def categorize(self, article):
        '''Categorize the report
        '''
        category = self.interpreter.classify_category(article.content.content)
        article_category = ArticleCategory(
            article_id=article.id, category=category)
        self.session.add(article_category)
        self.session.commit()
        article.categories.append(article_category)
