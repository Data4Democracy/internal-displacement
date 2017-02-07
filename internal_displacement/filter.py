from langdetect import detect

class Filter(object):
    '''Filter that accepts an article and identifies the 
    language and relevance of the article
    '''

    def __init__:
        pass

    def check_language(self, article):
        '''Identify the language of the article content
        '''
        language = detect(article.content)
        article.language = language

    def check_relevance(self, article):
        '''Tag the article as relevant or not based
        upon its content.
        '''
        pass