from bs4 import BeautifulSoup
import pandas as pd
from urllib import request
import numpy as np
import dateutil
import concurrent
from concurrent import futures

class Article(object):
    '''Contains article text, date, extracted information and tag
     Parameters
        ----------
        content:       the text from the article
        date:       the date
        title:      the title
                    
    '''
    def __init__(self,content,date,title):
        self.content = content
        self.date = date
        self.title = title


    def tag(self,tag):
        '''Use interpreter to tag article
        '''
        self.tag = tag
    def add_label(self,label):
        '''Store a label for training 
        '''
        self.label = label
    def parse():
        '''Use interpreter to parse article
        '''
        pass

    def export():
        '''Save article to external file
        '''
        pass


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


        #Class Functions
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


    def get_soup(self,url):
        '''
        Retrieves the soup for the given url, ready for use in the other get_ functions
        Parameters
        ----------
        url: the url from which to scrape content

        Returns
        -------
        soup: BeautifulSoup object containing content scraped from page
        '''
        # attempt to request page from url and return BeaufitulfSoup object
        try:
            html = request.urlopen(url,timeout=15).read()
            soup = BeautifulSoup(html, 'html.parser')
            return soup
        # if link is broken or timesout return empty variable
        except Exception as e:
            return None

    def get_content(self,soup):
        '''Returns the main text body from the soup
        Parameters
        ----------
        soup: BeautifulSoup object containing contents of web page

        Returns
        -------
        text: string of text from webpage with script, styling, links and more removed
        '''
        # if soup contained no information return empty string
        if soup is None:
            return ""
        else:
            # extract all components of soup matching the following tags
            ## is there an alternative to having this hard coded?
            _extracted = [s.extract() for s in soup(['script', 'link', 'style', 'id', 'class', 'li', 'head', 'a'])]
            # remove newline and &nbsp characters
            text = self.remove_newline(soup.get_text())
            return text

    def get_title(self,soup):
        '''Returns the article title from the soup
        Parameters
        ----------
        soup: BeautifulSoup object containing contents of web page

        Returns
        -------
        title: string with title of web page
        '''
        try:
            return soup.title.string
        except:
            return ""

    def get_date(self,soup):
        '''Returns date published - standardizes formatting with dateutil
        ## There has to be a better way of doing this. This current method misses most date entries.
        Parameters
        ----------
        soup: BeautifulSoup object containing contents of web page

        Returns
        -------
        title: string with title of web page
        '''
        # if soup contained no information return empty string
        if soup is None:
            return ""
        # try some searches for data type elements in the meta tag
        # dateutil parser returns a datetime object for most inputs
        else:
            html_meta = soup.find('meta', itemprop='Last-Modified', content=True)
            if html_meta is not None:
                return dateutil.parser.parse(html_meta['content'],ignoretz=True)
            html_meta = soup.find('meta', itemprop='datePublished', content=True)
            if html_meta is not None:
                return dateutil.parser.parse(html_meta['content'],ignoretz=True)
            html_meta = soup.find('meta', itemprop='og:updated_time', content=True)
            if html_meta is not None:
                return dateutil.parser.parse(html_meta['content'],ignoretz=True)
            else:
                return None
                

    def tag_type():
        '''Returns type of content (article/video/image/pdf)
        '''
        pass

    def export_article(self,url):
        '''Returns instance of article with content and all metadata
        '''
        soup = self.get_soup(url)
        title = self.get_title(soup)
        content = self.get_content(soup)
        date = self.get_date(soup)
        return Article(content,date,title)

    def export_all_articles(self,dataframe):
        '''
        Returns a list of articles created by scraping the urls contained in a dataframe. Can be used to create both unlabeled and labeled data.
        Parameters
        ----------
        dataframe:  A pandas dataframe containing a column "URL". 
                    It may optionally contain a a column "Tag", in which case the articles will be 
                    instantiated with their true_tag fields populated.
        Returns
        ----------
        articles: A list of Articles
        '''
        URLS = dataframe.URL.values
        with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
            # Start the load operations and mark each future with its URL
            future_to_article = {executor.submit(self.export_article, url): url for url in URLS}
            articles = []
            for future in concurrent.futures.as_completed(future_to_article):
                articles.append(future.result())
            if "Tag" in dataframe.columns:
                tags = dataframe["Tag"].values
                for i,a in enumerate(articles):
                    a.add_label(tags[i])
                return articles
            else:
                return articles













class Interpreter(object):
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

    def evaluate_new_model(self,model):
        pass


