from bs4 import BeautifulSoup
import pandas as pd
from urllib import request

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
    
    def sample_urls(self, index=None, sample=None):
        pass


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
        _extracted = [s.extract() for s in soup(['script', 'link', 'style', 'id', 'class', 'li', 'head', 'a'])]
        text = remove_newline(soup.get_text())