from langdetect import detect
import pycountry
import spacy


class Filter(object):
    '''Filter that accepts an article and identifies the 
    language and relevance of the article
    '''

    # Helper methods

    def country_code(country_name):
        try:
            country_code = pycountry.countries.get(name=s).alpha_2
            return country_code
        except KeyError:
            return False

    def __init__(self):
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

    def extract_countries(self, article):
        '''Extract the ISO codes for the countries mentioned
        in the article.
        '''
        nlp = spacy.load('en')
        doc = nlp(u"{}".format(s))
        possible_entities = []
        for ent in doc.ents:
            if ent.label_ == 'GPE':
                possible_entities.append(ent.text)
        possible_entities = set(possible_entities)

        countries = []
        for c in possible_entities:
            code = country_code(c)
            if code:
                countries.append(code)

        return countries