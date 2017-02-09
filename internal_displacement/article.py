
import datetime


def date_time_converter(dt):
    if isinstance(dt,datetime.datetime):
        return dt.__str__()
    else:
        raise ValueError("{} is not a valid datetime object")


class Article(object):
    """Contains article text, date, extracted information and tag
     Parameters
        ----------
        content:                the text from the article:String
        publication_date:       the date of publication:datetime.datetime
        title:                  the title:String
        authors:                the authors:list[String]
        domain:                 the domain:String
        content_type:           the type of content (text,image,video etc):String
        url:                    the url of the article:String
        language:               the two-letter language code of the article:String

    """

    def __init__(self, content, pub_date, title, content_type, authors, domain, url,language=""):
        self.content = content
        self.publication_date = pub_date
        self.title = title
        self.authors = authors
        self.domain = domain
        self.content_type = content_type
        self.url = url
        self.language = language

    def change_language(self,language):
        self.language = language
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

