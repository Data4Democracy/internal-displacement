from bs4 import BeautifulSoup
import pandas as pd
from urllib import request
import numpy as np


class Scraper(object):
    '''Scraper that accepts a url (or urls) and returns an instance of Article
    Parameters
    ----------
    urls: a url to be scraped

    Returns
    -------
    article: instance of Article containing body text and 
    '''
    def __init__(self, urls):
        if isinstance(urls, list):
            self.urls = urls
        if isinstance(urls, pd.Series):
            self.urls = list(urls)
        if isinstance(urls, str):
            self.urls = [urls]

    # Main Functions #

    def sample_urls(self, size=0.25, random=True):
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
        if isinstance(size, int) and size <= len(self.urls):
            sample_size = size
        elif isinstance(size, int) and size > len(self.urls):
            raise ValueError("Sample size cannot be larger than the"
                             " number of urls.")
        elif isinstance(size, float) and size >= 0.0 and size <= 1.0:
            sample_size = int(size * len(self.urls))
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
            return np.random.choice(self.urls, sample_size)
        else:
            return self.urls[:sample_size]

    def get_content():
        '''Returns the main text body from the url
        '''
        pass

    def get_title():
        '''Returns the article title from the url
        '''
        pass

    def get_meta():
        '''Returns date published
        '''
        pass

    def tag_type():
        '''Returns type of content (article/video/image/pdf)
        '''
        pass

    def export_article():
        '''Returns instance of article with content and all metadata
        '''
        pass

    # Helper Functions #

    def remove_newline(text):
        ''' Removes new line and &nbsp characters.
        '''
        text = text.replace('\n', ' ')
        text = text.replace('\xa0', ' ')
        return text

    def text_from_url(url):
        ''' Takes a url and returns a single string of the main text on the web page.
        '''
        html = request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        _extracted = [s.extract() for s in soup(
            ['script', 'link', 'style', 'id', 'class', 'li', 'head', 'a'])]
        text = remove_newline(soup.get_text())

class Article(object):
    '''Contains article text, metadata, extracted information and tag
    '''
    def __init__(self):
        pass

    def tag():
        '''Use interpreter to tag article
        '''
        pass

    def parse():
        '''Use interpreter to parse article
        '''
        pass

    def export():
        '''Save article to external file
        '''
        pass


class Interpreter(oject):
    '''The interpreter can use a pre-trained model or be trained to tag 
    articles and extract useful information from them.
    '''
    def __init__(self):
        pass

    def train_tagger():
        '''Train interpreter to tag articles as "distaster/violence/other"
        '''
        pass

    def train_parser():
        '''Train interpreter to parse articles and extract numbers and reporting unit
        '''
        pass

    def load_model():
        '''Load previously trained interpreter model
        '''
        pass

    def save_model():
        '''Export and save interpreter
        '''
        pass

    def tag():
        '''Tag article as "distaster/violence/other"
        '''
        pass

    def parse():
        '''Parse article to extract numbers and reporting unit
        '''
        pass


