from langdetect import detect
import pycountry
import spacy
import json
import re
import os
from collections import namedtuple
from internal_displacement.report import Report

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


# Helper functions for fact extraction
def test_token_equality(token_a, token_b):
    if token_a.text == token_b.text:
        return True
    else:
        return False


def check_if_collection_contains_token(token, collection):
    if any([test_token_equality(token, t) for t in collection]):
        return True
    else:
        return False


def check_if_entity_contains_token(tokens, entity):
    """
    Function to test if a given entity contains at least one of a list of tokens.
    param: tokens: A list of tokens
    param: entity: A span

    returns: Boolean
    """
    tokens_ = [t.text for t in tokens]
    ret = False
    for token in entity:
        if token.text in tokens_:
            return True
    return False


def get_contiguous_tokens(token_list):
    common_ancestor_tokens = get_common_ancestors(token_list)
    highest_contiguous_block = []
    for toke in token_list:
        if check_if_collection_contains_token(toke.head, common_ancestor_tokens):
            highest_contiguous_block.append(toke)
    added_tokens = 1
    while added_tokens > 0:
        added_tokens = 0
        for toke in token_list:
            if check_if_collection_contains_token(toke.head, highest_contiguous_block):
                if not check_if_collection_contains_token(toke, highest_contiguous_block):
                    highest_contiguous_block.append(toke)
                    added_tokens += 1
    return highest_contiguous_block


def match_entities_in_block(entities, token_block):
    matched = []
    # For some reason comparing identity on tokens does not always work.
    text_block = [t.text for t in token_block]
    for e in entities:
        et = [t.text for t in e]
        et_in_b = [t for t in et if t in text_block]
        if len(et_in_b) == len(et):
            matched.append(e)
    return matched


def get_common_ancestors(tokens):
    ancestors = [set(t.ancestors) for t in tokens]
    if len(ancestors) == 0:
        return []
    common_ancestors = ancestors[0].intersection(*ancestors)
    return common_ancestors


def get_descendents(sentence, root=None):
    """
    Retrieves all tokens that are descended from the head of the specified root token.
    param: root: the root token
    param: sentence: a span from which to retrieve tokens.
    returns: a list of tokens
    """
    if not root:
        root = sentence.root
    else:
        root = root.head
    return [t for t in sentence if root.is_ancestor_of(t)]


def get_all_descendent_tokens(token):
    """
    Returns a list of all descendents of the specified token.
    """
    children_accum = []
    for child in token.children:
        children_accum.append(child)
        grandchildren = get_all_descendent_tokens(child)
        children_accum.extend(grandchildren)
    return children_accum

Fact = namedtuple('Fact', ['term', 'unit', 'quantity', 'token_spans'])

person_reporting_terms = [
    'displaced', 'evacuated', 'forced flee', 'homeless', 'relief camp',
    'sheltered', 'relocated', 'stranded', 'stuck', 'stranded', "killed", "dead", "died"
]

structure_reporting_terms = [
    'destroyed', 'damaged', 'swept', 'collapsed', 'flooded', 'washed'
]

person_reporting_units = ["families", "person", "people", "individuals",
                          "locals", "villagers", "residents", "occupants", "citizens", "households"]

structure_reporting_units = ["home", "house", "hut", "dwelling",
                             "building", "shop", "business", "apartment", "flat", "residence"]

special_cases = ['damage home', 'displace family', 'displace people', 'displace person', 'family homeless', 
                'home destroy', 'household displace', 'people dead', 'people displace', 'people evacuate',
                'resident homeless']

special_case_regex = re.compile("|".join(special_cases))

class Interpreter(object):
    '''Intepreter for identifying and extracting relevant information
    from articles.
    '''

    def __init__(self, data_path='../data'):
        self.nlp = spacy.load('en')
        with open(os.path.join(data_path, 'cities_to_countries.json'), "r") as f:
            self.cities_to_countries = json.load(f)
        self.person_term_lemmas = [t.lemma_ for t in self.nlp(
            " ".join(person_reporting_terms))]
        self.structure_term_lemmas = [t.lemma_ for t in self.nlp(
            " ".join(structure_reporting_terms))]
        self.person_unit_lemmas = [t.lemma_ for t in self.nlp(
            " ".join(person_reporting_units))]
        self.structure_unit_lemmas = [t.lemma_ for t in self.nlp(
            " ".join(structure_reporting_units))]
        self.reporting_term_lemmas = self.person_term_lemmas + self.structure_term_lemmas
        self.reporting_unit_lemmas = self.person_unit_lemmas + self.structure_unit_lemmas

    def check_language(self, article):
        '''Identify the language of the article content
        and update the article property 'language'
        '''
        language = detect(article.content)
        article.language = language

    def check_relevance(self, article):
        '''Tag the article as relevant or not based
        upon whether or not any reports have been found.
        '''
        if len(article.reports) > 0:
            article.relevance = True

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

    def extract_dates(self, sentence):
        """
        Examines a sentence and identifies if any of its constituent tokens describe a date.
        If a root token is specified, only date tokens below the level of this token in the tree will be examined. 
        If no root is specified, date tokens will be drawn from the entirety of the span.
        Also identifies the start and end character locations of identified dates.
        param: sentence       a span
        returns: A list of strings, or None
        returns: A list of dicts of entity spans, or an empty list
        """
        dates_spans = []
        sentence_start = sentence.start_char
        root = sentence.root
        descendents = get_descendents(sentence, root)
        date_entities = [e for e in self.nlp(
            sentence.text).ents if e.label_ == "DATE"]
        if len(date_entities) > 0:
            descendent_date_tokens = []
            for date_ent in date_entities:
                if check_if_entity_contains_token(date_ent, descendents):
                    descendent_date_tokens.extend(
                        [token for token in date_ent])
            contiguous_token_block = get_contiguous_tokens(
                descendent_date_tokens)

            block_dates = match_entities_in_block(
                date_entities, contiguous_token_block)
            for location in block_dates:
                loc_start = location.start_char + sentence_start
                loc_end = location.end_char + sentence_start
                span = {'start': loc_start, 'end': loc_end, 'type': 'DATE'}
                dates_spans.append(span)
            return [location.text for location in block_dates] , dates_spans
        else:
            return None , dates_spans

    def extract_locations(self, sentence):
        """
        Examines a sentence and identifies if any of its constituent tokens describe a location.
        If a root token is specified, only location tokens below the level of this token in the tree will be examined. 
        If no root is specified, location tokens will be drawn from the entirety of the span.
        Also identifies the start and end character locations of identified locations.
        param: sentence       a span
        param: root           a token
        returns: A list of strings, or None
        returns: A list of dicts of entity spans, or an empty list
        """
        locations_spans = []
        sentence_start = sentence.start_char
        root = sentence.root
        descendents = get_descendents(sentence, root)
        location_entities = [e for e in self.nlp(
            sentence.text).ents if e.label_ == "GPE"]
        if len(location_entities) > 0:
            descendent_location_tokens = []
            for location_ent in location_entities:
                if check_if_entity_contains_token(location_ent, descendents):
                    descendent_location_tokens.extend(
                        [token for token in location_ent])
            contiguous_token_block = get_contiguous_tokens(
                descendent_location_tokens)

            block_locations = match_entities_in_block(
                location_entities, contiguous_token_block)
            for location in block_locations:
                loc_start = location.start_char + sentence_start
                loc_end = location.end_char + sentence_start
                span = {'start': loc_start, 'end': loc_end, 'type': 'LOC'}
                locations_spans.append(span)
            # , locations_spans
            return [location.text for location in block_locations], locations_spans
        else:
            return None , locations_spans

    def process_branch(self, token):
        """
        Process a branch of a parse tree and look for reporting units
        or number-like entities.
        Also identifies the start and end character locations of identified
        units or numbers.
        param: token           a token
        returns: reporting unit: A string or None
        returns: number: A string or None
        returns: spans: A list of dicts of entity spans, or an empty list
        """
        children = [token] + get_all_descendent_tokens(token)
        reporting_unit, number = None, None
        spans = []
        for child in children:
            if child.like_num:
                number = child.text
                span = {'start': child.idx, 'end': len(
                    child) + child.idx, 'type': 'NUM'}
                spans.append(span)
            elif child.lemma_ in self.reporting_unit_lemmas:
                reporting_unit = child.lemma_
                span = {'start': child.idx, 'end': len(
                    child) + child.idx, 'type': 'UNIT'}
                spans.append(span)
        return reporting_unit, number, spans

    def check_for_special_cases(self, sentence):
        """
        There are some cases not currently identified by the existing
        method of iterating over tokens and traversing the parse
        tree.
        Specifically, these are reporting unit and terms directly preceding
        one another, which do not have the right hierarchical relationship.
        See special_cases list above.
        These cases need to be identified and:
            1. Reporting term lemma and span identified
            2. Reporting unit lemma and span identified
            3. Quantity text and span identified
        """
        pass

    def extract_facts_from_sentence(self, sentence):
        """
        Process a sentence and look for reporting terms, units
        and number-like entities.
        Also identifies the start and end character locations of identified
        terms, units or numbers.
        param: sentence           a Spacy Span
        returns: reporting unit: A string or None
        returns: A named Fact tuple of reporting term, unit, quantity and extracted
                token spans: namedtuple
        """
        facts = []
        reporting_term, reporting_unit, reporting_quantity = None, None, None
        tokens = list(sentence.__iter__())
        for i, token in enumerate(tokens):
            if token.lemma_ in self.reporting_term_lemmas:
                spans = []
                term_span = {'start': token.idx, 'end': len(
                    token) + token.idx, 'type': 'TERM'}
                spans.append(term_span)
                term_token = token
                reporting_term = term_token.lemma_
                # Check for special cases here
                children = term_token.children
                for child in children:
                    reporting_unit, reporting_quantity, child_spans = self.process_branch(
                        child)
                    if reporting_unit:
                        spans.extend(child_spans)
                        facts.append(Fact(term=reporting_term, unit=reporting_unit, quantity=reporting_quantity, token_spans=spans))
        return facts

    def check_combination(self, term, unit):
        """
        Check a reporting term and unit to ensure that:
            - They both exist
            - There is no crossover between structure and people terms / units
        For example, this filters out cases like 'killed houses'
        param: reporting term           a lemmatized token
        param: reporting unit           a lemmatized token
        returns: Boolean
        """
        if not term or not unit:
            return False
        if term in self.person_term_lemmas and unit in self.structure_unit_lemmas:
            return False
        if term in self.structure_term_lemmas and unit in self.person_unit_lemmas:
            return False
        return True

    def extract_facts_from_article(self, article):
        """
        Process an article and look for reporting terms, units
        number-like entities, dates and locations.
        Keep a running track of locations and dates within the article
        and use these for creating reports.
        Extract the spans of start index, end index and fact type for all
        extracted reports.
        param: article           a string
        returns: list of reports or empty list
        """
        reports = []
        story = self.nlp(article.content)  # Parse the article content
        sentences = list(story.sents)  # Split the article into sentences
        last_date, last_date_span = None, []
        last_location, last_location_span = None, []  # Maintain running track
        for sentence in sentences:
            # Get and locations and or dates and update last date / location
            possible_dates, date_span = self.extract_dates(sentence)
            if possible_dates:
                last_date, last_date_span = possible_dates, date_span

            possible_locations, location_span = self.extract_locations(sentence)
            if possible_locations:
                last_location, last_location_span = possible_locations, location_span

            # Try and get terms / and or quantities
            facts = self.extract_facts_from_sentence(sentence)
            for fact in facts:
                if self.check_combination(fact.term, fact.unit):
                    fact_spans = fact.token_spans
                    fact_spans.extend(last_date_span)
                    fact_spans.extend(last_location_span)
                    report = Report(last_location, last_date,
                                    fact.term, fact.unit, fact.quantity, article.content, fact_spans)
                    reports.append(report)
        return reports
