import json
import os
import hashlib
import datetime
import sqlite3

def date_time_converter(dt):
    if isinstance(dt,datetime.datetime):
        return dt.__str__()


class Article(object):
    """Contains article text, date, extracted information and tag
     Parameters
        ----------
        content:                the text from the article
        publication_date:       the date of publication
        title:                  the title
        authors:                the authors
        domain:                 the domain
        content_type:           the type of content (text,image,video etc)
        url:                    the url of the article
        language:               the two-letter language code of the article

    """

    def __init__(self, content, pub_date, title, content_type, authors, domain, url):
        self.content = content
        self.publication_date = pub_date
        self.title = title
        self.authors = authors
        self.domain = domain
        self.content_type = content_type
        self.url = url
        self.language = ''

    def tag(self, tag):
        """Use interpreter to tag article
        """
        self.tag = tag

    def parse(self):
        """Use interpreter to parse article
        """
        pass


    def get_pub_date_string(self):
        return date_time_converter(self.publication_date)

