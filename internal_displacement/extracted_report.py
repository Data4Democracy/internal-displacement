import hashlib
import re
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
    Solution forked from 
	https://github.com/ghewgill/text2num/blob/master/text2num.py 
	and enhanced with numerical and array input
    '''
	
	Small = {
	    'zero': 0,
	    'one': 1,
	    'two': 2,
	    'three': 3,
	    'four': 4,
	    'five': 5,
	    'six': 6,
	    'seven': 7,
	    'eight': 8,
	    'nine': 9,
	    'ten': 10,
	    'eleven': 11,
	    'twelve': 12,
	    'thirteen': 13,
	    'fourteen': 14,
	    'fifteen': 15,
	    'sixteen': 16,
	    'seventeen': 17,
	    'eighteen': 18,
	    'nineteen': 19,
	    'twenty': 20,
	    'thirty': 30,
	    'forty': 40,
	    'fifty': 50,
	    'sixty': 60,
	    'seventy': 70,
	    'eighty': 80,
	    'ninety': 90
	}

	Magnitude = {
	    'thousand':     1000,
	    'million':      1000000,
	    'billion':      1000000000,
	    'trillion':     1000000000000,
	    'quadrillion':  1000000000000000,
	    'quintillion':  1000000000000000000,
	    'sextillion':   1000000000000000000000,
	    'septillion':   1000000000000000000000000,
	    'octillion':    1000000000000000000000000000,
	    'nonillion':    1000000000000000000000000000000,
	    'decillion':    1000000000000000000000000000000000,
	}
	
	Vague = {
		'numbers':		5,
	    'dozens':		55,
	    'tens':			55,
		'hundreds':		550,
		'thousands':	5500,
		'millions':		5500000,
	    'billions':     5500000000,
	    'trillions':    5500000000000,
	    'quadrillions': 5500000000000000,
	    'quintillions': 5500000000000000000,
	    'sextillions':  5500000000000000000000,
	    'septillions':  5500000000000000000000000,
	    'octillions':   5500000000000000000000000000,
	    'nonillions':   5500000000000000000000000000000,
	    'decillions':   5500000000000000000000000000000000,
	}

	a = []
	if not type(value) is list:
		value = [value]
	for s_item in value:
		a += re.split(r"[\s-]+", str(s_item))
		
	n = 0
	g = 0
	vague_of = False
	for w in a:
		try:
			x = int(w)
			g += x
		except:
			if w.lower() == 'of':
				vague_of = True
				continue
			
			if vague_of:
				if w[-1:] != 's':
					w = w + 's'
				if w == 'hundreds' or w == 'hundred':
					g *= 100
				elif w[:-1] in Magnitude:
					g *= Magnitude[w[:-1]]
				continue
				
			if w in Small:
				g += Small[w]
			elif w == "hundred" and g != 0:
				g *= 100
			elif w in Magnitude:
				n += g * Magnitude[w]
				g = 0
			elif w in Vague:
				g = Vague[w]
			else:
				return None
				
		vague_of = False
		
	return n + g


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
