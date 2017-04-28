'''Implement functions for adapting the broader solution to processing of specific fragments and excerpts.'''

import re
import string
import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
from internal_displacement.extracted_report import convert_quantity
from sklearn.externals import joblib
from collections import Counter
import numpy as np


class MeanEmbeddingVectorizer(object):

    def __init__(self, w2v):
        self.w2v = w2v
        # if a text is empty we should return a vector of zeros
        # with the same dimensionality as all the other vectors
        self.dim = (300,)

    def fit(self, X, y):
        return self

    def transform(self, X):
        return np.array([
            np.mean([self.w2v[w] for w in words if w in self.w2v]
                    or [np.zeros(self.dim)], axis=0)
            for words in X
        ])


class Helper(object):

    def __init__(self, nlp, unit_vec_path, unit_model_path, term_vec_path, term_model_path, term_svc_path):
        self.nlp = nlp
        self.reporting_unit_vectorizer = self.load_external(unit_vec_path)
        self.reporting_term_vectorizer = self.load_external(term_vec_path)
        self.reporting_unit_classifier = self.load_external(unit_model_path)
        self.reporting_term_classifier = self.load_external(term_model_path)
        self.reporting_term_svc = self.load_external(term_svc_path)

    def load_external(self, path):
        mod = joblib.load(path)
        return mod

    def remove_brackets(self, text):
        '''Remove items in brackets
        '''
        text = re.sub(r'(\(.+\))', '', text)
        text = re.sub(r'\s{2}', ' ', text)
        return text

    def cleanup(self, text):
        '''Clean common errors in the text and remove irrelevant tokens and stop words'''
        text = re.sub(r'([a-zA-Z0-9])(IMPACT)', r'\1. \2', text)
        text = re.sub(r'([a-zA-Z0-9])(RESPONSE)', r'\1. \2', text)
        text = re.sub(r'(IMPACT)([a-zA-Z0-9])', r'\1. \2', text)
        text = re.sub(r'(RESPONSE)([a-zA-Z0-9])', r'\1. \2', text)
        text = re.sub(r'([a-zA-Z])(\d)', r'\1. \2', text)
        text = re.sub(r'(\d)\s(\d)', r'\1\2', text)
        text = text.replace('\r', ' ')
        text = text.replace('  ', ' ')
        text = text.replace("peole", "people")
        output = ''
        for char in text:
            if char in string.printable:
                output += char
        output = self.remove_irrelevant_tokens(output)
        return output

    def remove_irrelevant_tokens(self, text):
        '''Remove phrases in brackets and irrelevant tokens (named entities and stop words)
        Return lemmatized text'''
        text = self.remove_brackets(text)
        output = []
        doc = self.nlp(text)
        for token in doc:
            if self.test_token(token):
                output.append(token)
        return " ".join([t.lemma_ for t in output])

    def test_token(self, token):
        '''Test tokens for exclusion'''
        if token.like_num:
            return False
        elif token.ent_type_ in ('LOC', 'GPE', 'PERSON', 'ORG', 'DATE', 'FAC', 'NORP'):
            return False
        elif token.is_stop:
            return False
        else:
            return True

    def minimum_loc(self, spans):
        '''Find the first character location in text for each report
        '''
        locs = []
        for s in spans:
            if s['type'] != 'loc':
                locs.append(s['start'])
        return min(locs)

    def choose_report(self, reports):
        '''Choose report based on the heuristics mentioned in the first cell
        '''
        people_reports = []
        household_reports_1 = []
        household_reports_2 = []

        for r in reports:
            if r.subject_term == "People":
                people_reports.append(r)
            elif r.subject_term == "Households":
                if r.event_term in ("Partially Destroyed Housing", "Uninhabitable Housing"):
                    household_reports_2.append(r)
                else:
                    household_reports_1.append(r)
        if len(people_reports) > 0:
            report = self.first_report(people_reports)
        elif len(household_reports_1) > 0:
            report = self.first_report(household_reports_1)
        elif len(household_reports_2) > 0:
            report = self.first_report(household_reports_2)
        else:
            report = reports[0]

        return report

    def first_report(self, reports):
        '''Choose the first report based on location in text'''
        report_locs = []
        for report in reports:
            report_locs.append((report, self.minimum_loc(report.tag_spans)))
        return sorted(report_locs, key=lambda x: x[1])[0][0]

    def get_report(self, reports):
        '''Get reports based on Excerpt and choose the most relevant one'''
        if len(reports) > 0:
            report = self.choose_report(reports)
            return report.quantity, report.event_term, report.subject_term, report.locations
        else:
            return 0, '', '', ''

    def combine_probabilities(self, p1, p2, classes):
        combined_probs = np.mean(np.array([p1, p2]), axis=0)
        predicted_indices = [np.argmax(arr) for arr in list(combined_probs)]
        predictions = [classes[i] for i in predicted_indices]
        return predictions

    def combine_predictions(self, classifier, rules):
        if classifier == rules:
            return classifier
        elif not rules or rules == '':
            return classifier
        else:
            return rules

    def choose_country(self, countries):
        '''Choose country out of possible countries
        Either return the most commonly mentioned country
        or the first country found
        '''

        if len(countries) == 0:
            return '', ''
        if len(countries) == 1:
            return countries[0]['location_text'], countries[0]['country_code']
        else:
            country_counter = Counter()
            for country in countries:
                country_counter[country['country_code']] += 1
            country_counts = list(country_counter.values())
            max_count = max(country_counts)
            if country_counts.count(max_count) > 1:
                sorted_countries = sorted(
                    countries, key=lambda k: k['order'])[0]
                return sorted_countries['location_text'], sorted_countries['country_code']
            else:
                country_subset = [d for d in countries if d[
                    'country_code'] == country_counter.most_common()[0][0]]
                sorted_countries = sorted(
                    country_subset, key=lambda k: k['order'])[0]
                return sorted_countries['location_text'], sorted_countries['country_code']

    def get_closest_number(self, possible_numbers, possible_units):
        '''Get closest number in text to word that most closely matches the given unit'''
        if len(possible_units) > 0:
            first_unit_place = possible_units[0][1]
            diffs = [(p, first_unit_place - n)
                     for p, n in possible_numbers if first_unit_place - n > 0]
            if len(diffs) > 0:
                return sorted(diffs, key=lambda x: x[1])[0][0]
        return 0

    def get_number(self, text, unit, person_lemmas, household_lemmas):
        '''Get number from text based on the given unit type'''
        # Remove brackets
        text = re.sub(r'(\(.+\))', '', text)
        text = re.sub(r'\s{2}', ' ', text)
        text = re.sub(r'(\d)\s(\d)', r'\1\2', text)
        lemmas = []
        if unit == "People":
            lemmas = person_lemmas
        else:
            lemmas = household_lemmas
        doc = self.nlp(text)
        possible_numbers = []
        possible_units = []
        for token in doc:
            if token.like_num:
                quantity = convert_quantity(token.text)
                if quantity:
                    possible_numbers.append((quantity, token.i))
            if token.lemma_ in lemmas:
                possible_units.append((token, token.i))

        closest_num = self.get_closest_number(possible_numbers, possible_units)
        if closest_num and closest_num > 0:
            return closest_num
        elif len(possible_numbers) > 0:
            highest_possible = sorted(
                possible_numbers, key=lambda x: x[0])[0][0]
            return highest_possible
        else:
            return 0

    def combine_quantities(self, r1, r2):
        '''Combine output of reports-based rules & new rules'''
        if r1 and r1 > 0:
            return r1
        elif r2:
            return r2
        else:
            return 0

    def get_unique_tag_spans(self, reports):
        '''Get a list of unique token spans
        for visualizing a complete article along
        with all extracted facts.
        Each extracted report has its own list of spans
        which may in some cases overlap, particularly
        for date and location tags.
        '''
        # need to deal with overlapping spans
        all_spans = []
        for report in reports:
            all_spans.extend(report.tag_spans)
        unique_spans = list({v['start']: v for v in all_spans}.values())
        unique_spans = sorted(unique_spans, key=lambda k: k['start'])
        # Check for no overlap
        non_overlapping_spans = []
        current_start = -1
        current_end = -1
        for span in unique_spans:
            if span['start'] > current_end:
                non_overlapping_spans.append(span)
                current_start, current_end = span['start'], span['end']
            else:
                # Create a new merged span and add it to the end of the result
                current_last_span = non_overlapping_spans[-1]
                new_span = {}
                new_span['type'] = ", ".join(
                    [current_last_span['type'], span['type']])
                new_span['start'] = current_last_span['start']
                new_span['end'] = max(current_last_span['end'], span['end'])
                non_overlapping_spans[-1] = new_span
                current_end = new_span['end']

        return non_overlapping_spans

    def tag_text(self, text, spans):
        text_blocks = []
        text_start_point = 0
        for span in spans:
            text_blocks.append(text[text_start_point: span['start']])

            tagged_text = '<mark data-entity="{}">'.format(
                span['type'].lower())
            tagged_text += text[span['start']: span['end']]
            tagged_text += '</mark>'
            text_blocks.append(tagged_text)
            text_start_point = span['end']
        text_blocks.append(text[text_start_point:])
        return("".join(text_blocks))
