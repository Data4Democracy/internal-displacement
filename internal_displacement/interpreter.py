from langdetect import detect
import pycountry
import spacy
import json
import re
import os

# Helper methods


def strip_words(place_name):
    '''Strip out common words that often appear in extracted entities
    '''
    place_name = place_name.lower()
    words_to_replace = {"the": "", "province": "",
                        "county": "", "district": "", "city": ""}
    rep = dict((re.escape(k), v) for k, v in words_to_replace.items())
    pattern = re.compile("|".join(rep.keys()))
    place_name = pattern.sub(lambda m: rep[re.escape(m.group(0))], place_name)
    return place_name.strip().title()


def common_names(place_name):
    '''Convert countries or places with commonly used names
    to their official names
    '''
    return{
        'Syria': 'Syrian Arab Republic',
        'Bosnia': 'Bosnia and Herzegovina'
    }.get(place_name, place_name)


def province_country_code(place_name):
    '''Try and extract the country code by looking
    at country subdivisions i.e. States, Provinces etc.
    return the country code if found
    '''
    subdivisions = (s for s in list(pycountry.subdivisions))
    for sub_division in subdivisions:
        if sub_division.name == place_name:
            return sub_division.country_code
            break


def match_country_name(place_name):
    '''Try and match the country name directly
    return the country code if found
    '''
    countries = (c for c in list(pycountry.countries))
    for country in countries:  # Loop through all countries
        if country.name == place_name:  # Look directly at country name
            return country.alpha_2
            break
        # In some cases the country also has a common name
        elif hasattr(country, 'common_name') and country.common_name == place_name:
            return country.alpha_2
            break
        # In some cases the country also has an official name
        elif hasattr(country, 'official_name') and country.official_name == place_name:
            return country.alpha_2
            break
        # In some cases the country name has the form Congo, The Democratic Republic of the
        # which may be hard to match directly
        elif re.match(r'\D+,\s{1}', country.name):
            common = re.search(r'(\D+),\s{1}', country.name).groups()[0]
            if common in place_name:
                return country.alpha_2
                break


class Interpreter(object):
    '''Intepreter for identifying and extracting relevant information
    from articles.
    '''

    def __init__(self, data_path='../data'):
        self.nlp = spacy.load('en')
        with open(os.path.join(data_path, 'cities_to_countries.json'), "r") as f:
            self.cities_to_countries = json.load(f)

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

    def country_code(self, place_name):
        '''Find the ISO-3166 alpha_2 country code 
        for a given country name
        '''
        place_name = common_names(place_name)
        country_code_from_name = match_country_name(place_name)
        if country_code_from_name:
            return country_code_from_name
        # Try getting the country code using a province name
        country_from_province = province_country_code(place_name)
        if country_from_province:
            return country_from_province
        # Try getting the country code using a city name
        return self.cities_to_countries.get(place_name, None)

    def extract_countries(self, article):
        '''Extract the ISO codes for the countries mentioned
        in the article, and return an array containing all
        mentioned countries
        '''
        text = " ".join([article.title, article.content])
        doc = self.nlp(u"{}".format(text))
        possible_entities = set()
        for ent in doc.ents:
            if ent.label_ in ('GPE', 'LOC'):
                possible_entities.add(strip_words(ent.text))
        possible_entities = set(possible_entities)

        countries = set()
        if len(possible_entities) > 0:
            for c in possible_entities:
                code = self.country_code(c)
                if code:
                    countries.add(code)

        return list(countries)
