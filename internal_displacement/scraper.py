import newspaper
import csv
import urllib
from urllib import request
from article import Article
import textract
import os
from collections import OrderedDict


def remove_newline(self, text):
    ''' Removes new line and &nbsp characters.
    '''
    text = text.replace('\n', ' ')
    text = text.replace('\xa0', ' ')
    return text


def html_report(url):
"""Downloads and extracts content plus metadata for html page
Parameters
----------
url: url of page to be scraped

Returns
-------
article: An object of class Article containing the content and metadata.
"""

a = newspaper.Article(url)
a.download()
if a.is_downloaded:
    a.parse()
    article_domain = a.source_url
    article_title = a.title
    article_authors = a.authors
    article_pub_date = a.publish_date
    article_text = remove_newline(a.text)
    # tag the type of article
    # currently default to text but should be able to determine img/video etc
    article_content_type = 'text'
    article = Article(article_text, article_pub_date, article_title,
                      article_content_type, article_authors, article_domain, url)
    return article
else:  # Temporary fix to deal with https://github.com/codelucas/newspaper/issues/280
    return Article("retrieval_failed", "", "", datetime.datetime.now(), "", "", url)


def get_pdf(url):
    ''' Takes a pdf url, downloads it and saves it locally.'''
    try:
        response = request.urlopen(url)  # not sure if this is needed?
    except urllib.error.HTTPError as e:
        if e.getcode() != 404:
            raise
        else:
            print('Error 404')
    pdf_file = open('file_to_convert.pdf', 'wb')
    pdf_file.write(response.read())
    pdf_file.close()
    return os.path.join('./', 'file_to_convert.pdf')


def get_body_text(url):
    ''' This function will extract all text from the url passed in
    '''
    text = str(textract.process(get_pdf(url), method='pdfminer'), 'utf-8')
    text = text.replace('\n', ' ')  # can replace with a call to
    text = text.replace('\xa0', ' ')  # the helper function.
    return text


def scrape(url):
"""
Scrapes content and metadata from an url
Parameters
----------
url: the url to be scraped

Returns
-------
article: An article object prepared by scraping the url.


"""
if "pdf" in url:
    pass
else:
    article = html_report(url)
    return article
