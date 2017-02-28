
import hashlib
from spacy.tokens import Token,Span

def convert_tokens_to_strings(value):
    if isinstance(value,Token):
        return value.text
    if isinstance(value,Span):
        return value.text
    else:
        return str(value)


class Report:
    def __init__(self, locations, date_times, event_term, subject_term, quantity, story, tag_spans=[]):
        if locations:
            self.locations = [convert_tokens_to_strings(l) for l in locations]
        else:
            self.locations = []
        if date_times:
            self.date_times = [convert_tokens_to_strings(dt) for dt in date_times]
        else:
            self.date_times = []
        self.event_term = convert_tokens_to_strings(event_term)
        self.subject_term = convert_tokens_to_strings(subject_term)
        self.quantity = convert_tokens_to_strings(quantity)
        self.story = story

    def display(self):
        print("Location: {}  DateTime: {}  EventTerm: {}  SubjectTerm:  {}  Quantity: {}"
              .format(self.locations, self.date_times, self.event_term, self.subject_term, self.quantity))

    def __eq__(self, other):
        if isinstance(other, Report):
            return ((self.locations == other.locations) and
                    (self.date_times == other.date_times) and
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
        dates = ",".join(self.date_times)
        rep = "Locations:{} Dates:{} Verb:{} Noun:{} Quantity:{}".format(locations,dates,self.event_term,self.subject_term,self.quantity)
        return rep

    def __hash__(self):
        return hash(self.__repr__())



    def to_json(self):
        d = {}
        d['Location'] = self.locations
        d['DateTime'] = self.date_times
        d['EventTerm'] = self.event_term
        d['SubjectTerm'] = self.subject_term
        d['Quantity'] = self.quantity
        return d