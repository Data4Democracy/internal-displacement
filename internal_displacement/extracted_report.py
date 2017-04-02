import hashlib
from spacy.tokens import Token, Span
from datetime import datetime


def convert_tokens_to_strings(value):
    if isinstance(value, Token):
        return value.text
    if isinstance(value, Span):
        return value.text
    else:
        return str(value)


def convert_quantity(value):
    '''Convert an extracted quantity to an integer.
    If unable to convert, return None.
    '''
    try:
        return int(value)
    except ValueError:
        return None


class ExtractedReport:

    def __init__(self, locations, event_term, subject_term, quantity, story, tag_spans=[]):
        if locations:
            self.locations = [convert_tokens_to_strings(l) for l in locations]
        else:
            self.locations = []
        self.event_term = convert_tokens_to_strings(event_term)
        self.subject_term = convert_tokens_to_strings(subject_term)
        self.quantity = convert_quantity(convert_tokens_to_strings(quantity))
        self.story = story

    def display(self):
        print("Location: {}  DateTime: {}  EventTerm: {}  SubjectTerm:  {}  Quantity: {}"
              .format(self.locations, self.event_term, self.subject_term, self.quantity))

    def __eq__(self, other):
        if isinstance(other, ExtractedReport):
            return ((self.locations == other.locations) and
                    (self.event_term == other.event_term) and
                    (self.subject_term == other.subject_term) and
                    (self.quantity == other.quantity)
                    )
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __repr__(self):
        locations = ",".join(self.locations)
        rep = "Locations:{} Verb:{} Noun:{} Quantity:{}".format(
            locations, self.event_term, self.subject_term, self.quantity)
        return rep

    def __hash__(self):
        return hash(self.__repr__())

    def to_json(self):
        d = {}
        d['Location'] = self.locations
        d['EventTerm'] = self.event_term
        d['SubjectTerm'] = self.subject_term
        d['Quantity'] = self.quantity
        return d


class Fact(object):
    '''Wrapper for individual facts found within articles
    '''

    def __init__(self, token, full_span=None, lemma_=None, fact_type=None, start_offset=0):
        self.token = token
        self.type_ = fact_type
        if full_span:
            self.text = full_span.text
        else:
            self.text = ''
        self.lemma_ = lemma_
        # Set the start index
        if isinstance(token, Token):
            self.start_idx = token.idx + start_offset
        elif isinstance(token, Span):
            self.start_idx = token[0].idx + start_offset
        else:
            self.start_idx = 0
        # Set the end index
        token_length = len(self.text)
        self.end_idx = self.start_idx + token_length

    def __str__(self):
        return self.text
