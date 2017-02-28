from spacy.tokens import Token,Span

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