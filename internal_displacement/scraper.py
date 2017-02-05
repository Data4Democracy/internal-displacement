import newspaper
import csv
from internal_displacement.article import Article
import datetime


# Helper Functions #

def remove_newline(text):
    """
    Removes new line and &nbsp characters.
    """
    text = text.replace('\n', ' ')
    text = text.replace('\xa0', ' ')
    return text

class Scraper(object):


    """Scraper that accepts a url (or urls) and returns an instance of Article
    Parameters
    ----------
    urls: a url to be scraped

    Returns
    -------
    article: instance of Article containing body text and 
    """



    # Class Functions #
    def __init__(self):
        pass

    def sample_urls(self, size=0.25, random=True):
        """Return a subsample of urls
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
        """
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
        
    def html_report(self, url):
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
            print(article_pub_date)
            article_text = remove_newline(a.text)
            # tag the type of article
            ## currently default to text but should be able to determine img/video etc
            article_content_type = 'text'
            article = Article(article_text, article_pub_date, article_title,
                              article_content_type, article_authors, article_domain, url)
            return article
        else: ##Temporary fix to deal with https://github.com/codelucas/newspaper/issues/280
            return Article("", datetime.datetime.now(), "retrieval_failed", "", "", "", "")


    def scrape(self, urls):
        """
        Scrapes content and metadata from all pages in a list
        ** Currently skips pdfs and only calls html_report
        Parameters
        ----------
        urls: list of urls of pages to be scraped 

        Returns
        -------
        reports: list of dictionaries containing all reports
        """
        articles = []
        for url in urls:
            if url[-3:] == 'pdf':
                continue
            else:
                article = self.html_report(url)
                articles.append(article)
                
        return articles






