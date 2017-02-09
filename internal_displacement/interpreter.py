from langdetect import detect
import pycountry
import spacy

# Helper methods


def country_code(country_name):
    '''Find the ISO-3166 alpha_2 country code 
    for a given country name
    '''
    try:
        country_code = pycountry.countries.get(name=country_name).alpha_2
        return country_code
    except KeyError:
        return False


class Interpreter(object):
    '''Intepreter for identifying and extracting relevant information
    from articles.
    '''

    def __init__(self):
        self.nlp = spacy.load('en')

    def check_language(self, article):
        '''Identify the language of the article content
        and update the article property 'language'
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
        in the article, and return an array containing all
        mentioned countries
        '''
        doc = self.nlp(u"{}".format(article.content))
        possible_entities = []
        for ent in doc.ents:
            if ent.label_ == 'GPE':
                possible_entities.append(ent.text)
        possible_entities = set(possible_entities)

        countries = []
        if len(possible_entities) > 0:
            for c in possible_entities:
                code = country_code(c)
                if code:
                    countries.append(code)

        return countries
