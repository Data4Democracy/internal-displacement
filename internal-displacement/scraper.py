import newspaper
import csv

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


    def html_report(self, url):
        '''Downloads and extracts content plus metadata for html page
        Parameters
        ----------
        url: url of page to be scraped 

        Returns
        -------
        report: dictionary containing page content and metadata
        '''
        report = {}
        a = newspaper.Article(url)
        a.download()
        a.parse()
        report['domain'] = a.source_url
        report['title'] = a.title
        report['authors'] = a.authors
        report['date_pub'] = a.publish_date
        report['text'] = remove_newline(a.text)
        # tag the type of article
        ## currently default to text but should be able to determine img/video etc
        report['type'] = 'text'
        return report

    def scrape(self, urls):
        '''Scrapes content and metadata from all pages in a list
        ** Currently skips pdfs and only calls html_report
        Parameters
        ----------
        urls: list of urls of pages to be scraped 

        Returns
        -------
        reports: list of dictionaries containing all reports
        '''
        reports = []
        for url in urls:
            if url[-3:] == 'pdf':
                continue
            else:
                report = html_report(url)
                reports.append(report)
                
        return reports