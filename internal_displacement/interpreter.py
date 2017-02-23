import re
import pycountry
import json
import spacy
import os
import textacy
from internal_displacement.report import Report


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


class Interpreter():
    def __init__(self, nlp, person_reporting_terms, structure_reporting_terms, person_reporting_units,
                 structure_reporting_units, relevant_article_lemmas, data_path='../data'):
        self.nlp = nlp
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
        self.relevant_article_lemmas = relevant_article_lemmas

    def check_language(self, article):
        '''Identify the language of the article content
        and update the article property 'language'
        '''
        try:
            language = textacy.text_utils.detect_language(article.content)
        except ValueError:
            language = 'na'
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

    def test_token_equality(self, token_a, token_b):
        if token_a.i == token_b.i:
            return True
        else:
            return False

    def check_if_collection_contains_token(self, token, collection):
        for c in collection:
            if self.test_token_equality(token, c):
                return True
        return False

    def get_descendents(self, sentence, root=None):
        """
        Retrieves all tokens that are descended from the specified root token.
        param: root: the root token
        param: sentence: a span from which to retrieve tokens.
        returns: a list of tokens
        """
        if not root:
            root = sentence.root
        return [t for t in sentence if root.is_ancestor_of(t)]

    def check_if_entity_contains_token(self, tokens, entity):
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

    def get_distance_from_root(self, token, root):
        """
        Gets the parse tree distance between a token and the sentence root.
        :param token: a token
        :param root: the root token of the sentence

        returns: an integer distance
        """
        if token == root:
            return 0
        d = 1
        p = token.head
        while p is not root:
            d += 1
            p = p.head
        return d

    def get_common_ancestors(self, tokens):
        ancestors = [set(t.ancestors) for t in tokens]
        if len(ancestors) == 0:
            return []
        common_ancestors = ancestors[0].intersection(*ancestors)
        return common_ancestors

    def get_distance_between_tokens(self, token_a, token_b):

        if token_b in token_a.subtree:
            distance = self.get_distance_from_root(token_b, token_a)
        elif token_a in token_b.subtree:
            distance = self.get_distance_from_root(token_a, token_b)
        else:
            common_ancestors = self.get_common_ancestors([token_a, token_b])
            distance = 10000
            for ca in common_ancestors:
                distance_a = self.get_distance_from_root(ca, token_a)
                distance_b = self.get_distance_from_root(ca, token_b)
                distance_ab = distance_a + distance_b
                if distance_ab < distance:
                    distance = distance_ab
        return distance

    def get_closest_contiguous_location_block(self, entity_list, root_node):
        location_entity_tokens = [[token for token in sentence]
                                  for sentence in entity_list]
        token_list = [
            item for sublist in location_entity_tokens for item in sublist]
        location_tokens_by_distance = sorted([(token, self.get_distance_between_tokens(token, root_node))
                                              for token in token_list], key=lambda x: x[1])
        closest_location = location_tokens_by_distance[0]
        contiguous_block = [closest_location]
        added_tokens = 1
        while added_tokens > 0:
            contiguous_block_ancestors = [[token for token in token_list if token.is_ancestor_of(toke)] for toke in
                                          contiguous_block]
            contiguous_block_subtrees = [
                token.subtree for token in contiguous_block]
            contiguous_block_neighbours = contiguous_block_ancestors + contiguous_block_subtrees
            contiguous_block_neighbours = [
                item for sublist in contiguous_block_neighbours for item in sublist]
            added_tokens = 0
            for toke in token_list:
                if not self.check_if_collection_contains_token(toke, contiguous_block):
                    if toke in contiguous_block_neighbours:
                        added_tokens += 1
                        contiguous_block.append(toke)
        return contiguous_block

    def get_contiguous_tokens(self, token_list):
        common_ancestor_tokens = self.get_common_ancestors(token_list)
        highest_contiguous_block = []
        for toke in token_list:
            if self.check_if_collection_contains_token(toke.head, common_ancestor_tokens):
                highest_contiguous_block.append(toke)
        added_tokens = 1
        while added_tokens > 0:
            added_tokens = 0
            for toke in token_list:
                if self.check_if_collection_contains_token(toke.head, highest_contiguous_block):
                    if not self.check_if_collection_contains_token(toke, highest_contiguous_block):
                        highest_contiguous_block.append(toke)
                        added_tokens += 1
        return highest_contiguous_block

    def match_entities_in_block(self, entities, token_block):
        matched = []
        # For some reason comparing identity on tokens does not always work.
        text_block = [t.text for t in token_block]
        for e in entities:
            et = [t.text for t in e]
            et_in_b = [t for t in et if t in text_block]
            if len(et_in_b) == len(et):
                matched.append(e)
        return matched

    def extract_locations(self, sentence, root=None):
        """
        Examines a sentence and identifies if any of its constituent tokens describe a location.
        If a root token is specified, only location tokens below the level of this token in the tree will be examined.
        If no root is specified, location tokens will be drawn from the entirety of the span.
        param: sentence       a span
        param: root           a token
        returns: A list of strings, or None
        """

        if not root:
            root = sentence.root
        descendents = self.get_descendents(sentence, root)
        location_entities = [e for e in self.nlp(
            sentence.text).ents if e.label_ == "GPE"]
        if len(location_entities) > 0:
            descendent_location_tokens = []
            for location_ent in location_entities:
                if self.check_if_entity_contains_token(location_ent, descendents):
                    descendent_location_tokens.extend(
                        [token for token in location_ent])
            contiguous_token_block = self.get_contiguous_tokens(
                descendent_location_tokens)

            block_locations = self.match_entities_in_block(
                location_entities, contiguous_token_block)
            if len(block_locations) > 0:
                return [location.text for location in block_locations]
            else:
                return location_entities  # If we cannot decide which one is correct, choose them all
                # and figure it out at the report merging stage.
        else:
            return []

    def extract_dates(self, sentence, root=None):
        """
        Examines a sentence and identifies if any of its constituent tokens describe a date.
        If a root token is specified, only date tokens below the level of this token in the tree will be examined.
        If no root is specified, date tokens will be drawn from the entirety of the span.
        Unlike the extract dates function (which returns a list of strings),
        this function returns a list of spacy spans. This is because numerical quantities detected in the
        branch_search need to be checked to ensure they are not in fact parts of a date.

        param: sentence       a span
        param: root           a token
        returns: A list of spacy spans
        """
        if not root:
            root = sentence.root
        descendents = self.get_descendents(sentence, root.head)
        date_entities = [e for e in self.nlp(
            sentence.text).ents if e.label_ == "DATE"]
        if len(date_entities) > 0:
            descendent_date_tokens = []
            for date_ent in date_entities:
                if self.check_if_entity_contains_token(date_ent, descendents):
                    descendent_date_tokens.extend(
                        [token for token in date_ent])
            contiguous_token_block = self.get_contiguous_tokens(
                descendent_date_tokens)

            block_dates = self.match_entities_in_block(
                date_entities, contiguous_token_block)
            return block_dates
        else:
            return None

    def basic_number(self, token):
        if token.text in ("dozens", "hundreds", "thousands", "fifty"):
            return True
        if token.like_num:
            return True
        else:
            return False

    def process_sentence_new(self, sentence, dates_memory, locations_memory, story):
        """
        Extracts the main verbs from a sentence as a starting point
        for report extraction.
        """
        sentence_reports = []
        # Find the verbs
        main_verbs = textacy.spacy_utils.get_main_verbs_of_sent(sentence)
        for v in main_verbs:
            unit_type, verb_lemma = self.verb_relevance(v, story)
            if unit_type:
                reports = self.branch_search_new(v, verb_lemma, unit_type, dates_memory, locations_memory, sentence,
                                                 story)
                sentence_reports.extend(reports)
        return sentence_reports

    def article_relevance(self, article):
        for token in article:
            if token.lemma_ in self.relevant_article_lemmas:
                return True

    def verb_relevance(self, verb, article):
        """
        Checks a verb for relevance by:
        1. Comparing to structure term lemmas
        2. Comparing to person term lemmas
        3. Looking for special cases such as 'leave homeless'
        """
        if verb.lemma_ in self.structure_term_lemmas:
            return self.structure_unit_lemmas, verb.lemma_
        elif verb.lemma_ in self.person_term_lemmas:
            return self.person_unit_lemmas, verb.lemma_
        elif verb.lemma_ == 'leave':
            children = verb.children
            obj_predicate = None
            for child in children:
                if child.dep_ in ('oprd', 'dobj'):
                    obj_predicate = child
            if obj_predicate:
                if obj_predicate.lemma_ in self.structure_term_lemmas:
                    return self.structure_unit_lemmas, 'leave ' + obj_predicate.lemma_
                elif obj_predicate.lemma_ in self.person_term_lemmas:
                    return self.person_unit_lemmas, 'leave ' + obj_predicate.lemma_
        elif verb.lemma_ == 'affect' and self.article_relevance(article):
            return self.structure_unit_lemmas + self.person_unit_lemmas, verb.lemma_
        elif verb.lemma_ in ('fear', 'assume'):
            verb_objects = textacy.spacy_utils.get_objects_of_verb(verb)
            if verb_objects:
                verb_object = verb_objects[0]
                if verb_object.lemma_ in self.person_term_lemmas:
                    return self.person_unit_lemmas, verb.lemma_ + " " + verb_object.text
                elif verb_object.lemma_ in self.structure_term_lemmas:
                    return self.structure_unit_lemmas, verb.lemma_ + " " + verb_object.text

        return None, None

    def get_quantity_from_phrase(self, phrase):
        """
        Look for number-like tokens within noun phrase.
        """
        for token in phrase:
            if self.basic_number(token):
                return token

    def get_quantity(self, sentence, unit):
        """
        Split a sentence into noun phrases.
        Search for quantities within each noun phrase.
        If the noun phrase is part of a conjunction, then
        search for quantity within preceding noun phrase
        """
        noun_phrases = list(self.nlp(sentence.text).noun_chunks)
        # Case one - if the unit is a conjugated noun phrase,
        # look for numeric tokens descending from the root of the phrase.
        for i, np in enumerate(noun_phrases):
            if self.check_if_collection_contains_token(unit, np):
                if unit.dep_ == 'conj':
                    return self.get_quantity_from_phrase(noun_phrases[i - 1])
                else:
                    return self.get_quantity_from_phrase(np)
        # Case two - get any numeric child of the unit noun.
        for child in unit.children:
            if self.basic_number(child):
                return child

    def simple_subjects_and_objects(self, verb):
        verb_objects = textacy.spacy_utils.get_objects_of_verb(verb)
        verb_subjects = textacy.spacy_utils.get_subjects_of_verb(verb)
        verb_objects.extend(verb_subjects)
        return verb_objects

    def nouns_from_relative_clause(self, sentence, verb):
        possible_clauses = list(
            textacy.extract.pos_regex_matches(sentence, r'<NOUN>+<VERB>'))
        for clause in possible_clauses:
            if verb in clause:
                for token in clause:
                    if token.tag_ == 'NNS':
                        return token

    def get_subjects_and_objects(self, story, sentence, verb):
        """
        Identify subjects and objects for a verb
        Also check if a reporting unit directly precedes
        a verb and is a direct or prepositional object
        """
        # Get simple or standard subjects and objects
        verb_objects = self.simple_subjects_and_objects(verb)
        # Special Cases

        # see if unit directly precedes verb
        if verb.i > 0:
            preceding = story[verb.i - 1]
            if preceding.dep_ in ('pobj', 'dobj') and preceding not in verb_objects:
                verb_objects.append(preceding)

        # See if verb is part of a conjunction
        if verb.dep_ == 'conj':
            lefts = list(verb.lefts)
            if len(lefts) > 0:
                for token in lefts:
                    if token.dep_ in ('nsubj', 'nsubjpass'):
                        verb_objects.append(token)
            else:
                ancestors = verb.ancestors
                for anc in ancestors:
                    verb_objects.extend(self.simple_subjects_and_objects(anc))

        # Look for 'pobj' in sentence
        if verb.dep_ == 'ROOT':
            for token in sentence:
                if token.dep_ == 'pobj':
                    verb_objects.append(token)

        # Look for nouns in relative clauses
        if verb.dep_ == 'relcl':
            relcl_noun = self.nouns_from_relative_clause(sentence, verb)
            if relcl_noun:
                verb_objects.append(relcl_noun)

        return list(set(verb_objects))

    def test_noun_conj(self, sentence, noun):
        possible_conjs = list(textacy.extract.pos_regex_matches(
            sentence, r'<NOUN><CONJ><NOUN>'))
        for conj in possible_conjs:
            if noun in conj:
                return conj

    def next_word(self, story, token):
        if token.i == len(story):
            return None
        else:
            return story[token.i + 1]


    def branch_search_new(self, verb, verb_lemma, search_type, dates_memory, locations_memory, sentence, story):
        """
        Extract reports based upon an identified verb (reporting term).
        Extract possible locations or use most recent locations
        Extract possible dates or use most recent dates
        Identify reporting unit by looking in objects and subjects of reporting term (verb)
        Identify quantity by looking in noun phrases.
        """

        possible_locations = self.extract_locations(sentence, verb)
        possible_dates = self.extract_dates(sentence, verb)
        if not possible_locations:
            possible_locations = locations_memory
        if not possible_dates:
            possible_dates = dates_memory
        reports = []
        quantity = None
        verb_objects = self.get_subjects_and_objects(story, sentence, verb)
        # If there are multiple possible nouns and it is unclear which is the correct one
        # choose the one with the fewest descendents. A verb object with many descendents is more likely to
        # have its own verb as a descendent.
        verb_descendent_counts = [(v, len(list(v.subtree)))
                                  for v in verb_objects]
        verb_objects = [x[0] for x in sorted(
            verb_descendent_counts, key=lambda x: x[1])]
        for o in verb_objects:
            if self.basic_number(o):
                # Test if the following word is either the verb in question
                # Or if it is of the construction 'leave ____', then ____ is the following word
                next_word = self.next_word(story, o)
                if next_word and next_word.i == verb.i or next_word.text == verb_lemma.split(" ")[-1]:
                    quantity = o
                    if search_type == self.structure_term_lemmas:
                        unit = 'house'
                    else:
                        unit = 'person'
                    report = Report(possible_locations, possible_dates, verb_lemma,
                                    unit, quantity, story.text)
                    # report.display()
                    reports.append(report)
                    break
            elif o.lemma_ in search_type:
                reporting_unit = o.lemma_
                noun_conj = self.test_noun_conj(sentence, o)
                if noun_conj:
                    reporting_unit = noun_conj
                    # Try and get a number - begin search from noun conjunction root.
                    quantity = self.get_quantity(sentence, reporting_unit.root)
                else:
                    # Try and get a number - begin search from noun.
                    quantity = self.get_quantity(sentence, o)
                report = Report(possible_locations, possible_dates, verb_lemma,
                                reporting_unit, quantity, story.text)
                reports.append(report)
                # report.display()
                break
        return reports

    def cleanup(self, text):
        text = re.sub(r'([a-zA-Z0-9])(IMPACT)', r'\1. \2', text)
        text = re.sub(r'([a-zA-Z0-9])(RESPONSE)', r'\1. \2', text)
        text = re.sub(r'(IMPACT)([a-zA-Z0-9])', r'\1. \2', text)
        text = re.sub(r'(RESPONSE)([a-zA-Z0-9])', r'\1. \2', text)
        text = re.sub(r'([a-zA-Z])(\d)', r'\1. \2', text)
        return text

    def process_article_new(self, story):
        """
        Process a story once sentence at a time
        """
        story = self.cleanup(story)
        processed_reports = []
        story = self.nlp(story)
        sentences = list(story.sents)  # Split into sentences
        dates_memory = None  # Keep a running track of the most recent dates found in articles
        # Keep a running track of the most recent locations found in articles
        locations_memory = None
        for sentence in sentences:  # Process sentence
            reports = []
            reports = self.process_sentence_new(
                sentence, dates_memory, locations_memory, story)
            current_locations = self.extract_locations(sentence)
            if current_locations:
                locations_memory = current_locations
            current_dates = self.extract_dates(sentence)
            if current_dates:
                dates_memory = current_dates
            processed_reports.extend(reports)
        return list(set(processed_reports))