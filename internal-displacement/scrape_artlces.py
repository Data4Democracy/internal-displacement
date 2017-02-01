from bs4 import BeautifulSoup
import pandas as pd
from urllib import request
import numpy as np


class UrlList(object):
    '''A wrapper for lists of urls in various formats.
    '''

    def __init__(self, obj):
        if isinstance(obj, list):
            self.urls = pd.Series(obj)
        if isinstance(obj, pd.Series):
            self.urls = obj
        if isinstance(obj, str):
            self.urls = pd.Series(obj)

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
            return pd.Series(np.random.choice(self.urls, sample_size))
        else:
            return self.urls[:sample_size]

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
