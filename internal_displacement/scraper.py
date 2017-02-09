import newspaper
import csv
import urllib
from urllib import request
from urllib.parse import urlparse
from internal_displacement.article import Article
import textract
import os
from collections import OrderedDict
import datetime
from bs4 import BeautifulSoup
import re


# PDF helper functions
def is_pdf_simple_tests(url):
    '''Test a url to see if it is a pdf by looking at url and content headers
    If so, return the relevant pdf url for parsing
    '''
    # Simple url-based test
    if re.search(r'\.pdf$', url):
        return url

    # Test based on headers
    page = request.urlopen(url)
    content_type = response.getheader('Content-Type')
    if content_type == 'application/pdf':
        return url


def is_pdf_iframe_test(url):
    '''Test a url to see if the page contains an iframe
    and if the iframe content is pdf or not; if True, return the pdf url
    '''
    page = request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    iframes = soup.find_all('iframe')
    if len(iframes) > 0:
        for frame in iframes:
            src = frame.attrs['src']
            if is_pdf_simple_tests(src):
                return src


def is_pdf_consolidated_test(url):
    '''Run a series of tests to determine if it is a pdf
    If True, return the relevant url
    '''

    # Carry out simple tests based upon url and content type
    pdf_attempt_1 = is_pdf_simple_tests(url)
    if pdf_attempt_1:
        return pdf_attempt_1

    # Carry out additional test based by looking for iframe
    pdf_attempt_2 = is_pdf_iframe_test(url)
    if pdf_attempt_2:
        return pdf_attempt_2

    return False


def remove_newline(text):
    ''' Removes new line and &nbsp characters.
    '''
    text = text.replace('\n', ' ')
    text = text.replace('\xa0', ' ')
    return text


def html_article(url):
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
        # currently default to text but should be able to determine img/video
        # etc
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
    flepath = get_pdf(url)
    text = str(textract.process(filepath, method='pdfminer'), 'utf-8')
    text = text.replace('\n', ' ')  # can replace with a call to
    text = text.replace('\xa0', ' ')  # the helper function.
    return text

def remove_pdf(filepath):
    ''' Deletes pdf from disk
    Not currently in use as pdfs downloads overwrite self, but may come in 
    useful later if pdfs are downloaded and stored under different names.
    '''
    os.remove(filepath)

def pdf_article(url):
    article_text = get_body_text(url)
    article_domain = urlparse(url).hostname
    article_content_type = 'pdf'
    # improve parsing of pdfs to extract these?
    article_title = ''
    article_pub_date = ''
    article_authors = ''
    article = Article(article_text, article_pub_date, article_title,
                      article_content_type, article_authors, article_domain, url)
    return article


def scrape(url, scrape_pdfs=True):
    """
    Scrapes content and metadata from an url
    Parameters
    ----------
    url: the url to be scraped
    scrape_pdfs: determines whether pdf files will be scraped or not
                 default: True

    Returns
    -------
    article: An article object prepared by scraping the url.


    """
    pdf_check = is_pdf_consolidated_test(url)
    if pdf_check and scrape_pdfs:
        article = pdf_article(pdf_check)
        return article
    elif not pdf_check:
        article = html_article(url)
        return article
    else:
        pass
