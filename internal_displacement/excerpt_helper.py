'''Implement functions for adapting the broader solution to processing of specific fragments and excerpts.'''

import re
import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
from internal_displacement.extracted_report import convert_quantity
from sklearn.externals import joblib


class Helper(object):

    def __init__(self, nlp):
        self.nlp = nlp
        self.reporting_unit_vectorizer = self.load_external('')
        self.reporting_term_vectorizer = self.load_external('')
        self.reporting_unit_classifier = self.load_external('')
        self.reporting_term_classifier = self.load_external('')

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

    def choose_report(self, reports):
    '''Get reports based on Excerpt and choose the most relevant one'''
        if len(reports) > 0:
            report = self.choose_report(reports)
            return report.quantity, report.event_term, report.subject_term, report.locations
        else:
            return 0, '', '', ''

    def combine_predictions(self, classifier, rules):
        if classifier == rules:
            return classifier
        elif not rules or rules == '':
            return classifier
        else:
            return rules

    def choose_country(self, countries, first_country=''):
        '''Choose country out of possible countries
        Either return the most commonly mentioned country
        or the first country found
        '''

        if len(countries) == 0:
            return ''
        if len(countries) <= 1:
            return countries.most_common()[0][0]
        else:
            country_counts = list(countries.values())
            max_count = max(country_counts)
            if country_counts.count(max_count) > 1:
                return first_country
            else:
                return countries.most_common()[0][0]

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
        doc = nlp(text)
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
