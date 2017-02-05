class Article(object):
    '''Contains article text, date, extracted information and tag
     Parameters
        ----------
        content:                the text from the article
        publication_date:       the date of publication
        title:                  the title
        authors:                the authors
        domain:                 the domain
        content_type:           the type of content (text,image,video etc)

    '''

    def __init__(self, content, pub_date, title,content_type,authors,domain):
        self.content = content
        self.publication_date = pub_date
        self.title = title
        self.authors = authors
        self.domain = domain
        self.content_type = content_type

    def tag(self, tag):
        '''Use interpreter to tag article
        '''
        self.tag = tag

    def add_label(self, label):
        '''Store a label for training cases
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