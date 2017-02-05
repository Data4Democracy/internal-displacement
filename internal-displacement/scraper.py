import newspaper
import csv
import urllib
from urllib import request
import textract
import os
from collections import OrderedDict

class Scraper(object):
    '''Scraper that accepts a url (or urls) and returns an instance of Article
    Parameters
    ----------
    urls: a url to be scraped

    Returns
    -------
    article: instance of Article containing body text and
    '''

        # Helper Functions #

    def remove_newline(self,text):
        ''' Removes new line and &nbsp characters.
        '''
        text = text.replace('\n', ' ')
        text = text.replace('\xa0', ' ')
        return text

        # Class Functions #
    def __init__(self, urls):
        if isinstance(urls, list):
            self.urls = urls
        if isinstance(urls, pd.Series):
            self.urls = list(urls)
        if isinstance(urls, str):
            self.urls = [urls]

    def html_article(self, url):
        '''Downloads and extracts content plus metadata for html page
        Parameters
        ----------
        url: url of page to be scraped
        Returns
        -------
        report: dictionary containing page content and metadata
        '''
        article = OrderedDict()
        a = newspaper.Article(url)
        a.download()
        a.parse()
        article['domain'] = a.source_url
        article['title'] = a.title
        article['authors'] = a.authors
        article['date_pub'] = a.publish_date
        article['text'] = remove_newline(a.text)
        # tag the type of article
        ## currently default to text but should be able to determine img/video etc
        article['type'] = 'text'
        return article
    def get_pdf(url):
        ''' Takes a pdf url, downloads it and saves it locally.'''
        try:
            response = request.urlopen(url)  #not sure if this is needed?
        except urllib.error.HTTPError as e:
            if e.getcode() != 404:
                raise
            else:
                print('Error 404')
        pdf_file = open('file_to_convert.pdf', 'wb')
        pdf_file.write(response.read())
        pdf_file.close()
        return os.path.join('./','file_to_convert.pdf')

    def get_body_text(url):
        ''' This function will extract all text from the url passed in
        '''
        text = str(textract.process(get_pdf(url), method='pdfminer'), 'utf-8')
        text = text.replace('\n', ' ')   #can replace with a call to
        text = text.replace('\xa0', ' ') # the helper function. 
        return text
    def scrape(self, urls):
        '''Scrapes content and metadata from all pages in a list
        if URL is a .pdf calls get_body_text
        otherwise, calls html_report
        ** Currently skips pdfs and only calls html_report
        Parameters
        ----------
        urls: list of urls of pages to be scraped

        Returns
        -------
        reports: list of dictionaries containing all reports
        '''
        articles = []
        pdf_articles = []
        for url in urls:
            if url[-3:] == '.  ':       # Found this anomaly in some urls
                url = url.rstrip('.  ')
            if url[-3:] == 'pdf':
                pdf_text = get_body_text(url)
                pdf_articles.append(pdf_text)
            else:
                article = html_article(url)
                articles.append(article)
        return articles
