import datetime


def date_time_converter(dt):
    if isinstance(dt, datetime.datetime):
        return dt.__str__()
    else:
        return "Invalid datetime"
#        raise ValueError("{} is not a valid datetime object")

def span_overlap(span1, span2):
    set1 = set(span1)
    if len(set1.intersection(span2)) > 0:
        return True


class Article(object):
    """Contains article text, date, extracted information and tag
     Parameters
        ----------
        content:                the text from the article:String
        publication_date:       the date of publication:datetime.datetime
        title:                  the title:String
        authors:                the authors:list[String]
        domain:                 the domain:String
        content_type:           the type of content (text,image,video etc):String
        url:                    the url of the article:String
        language:               the two-letter language code of the article:String
                                    see https://cloud.google.com/translate/docs/languages
        country_codes:          a list of ISO 3166 country codes:List
        reports:                a list of extracted reports
        relevance:              relevance of article to IDPs:Boolean

    """

    def __init__(self, content, pub_date, title, content_type, authors, domain, url, language="EN", country_codes=[], reports=[], relevance=False):
        self.content = content
        self.publication_date = pub_date
        self.title = title
        self.authors = authors
        self.domain = domain
        self.content_type = content_type
        self.url = url
        self.language = language
        self.relevance = relevance
        
    def change_language(self, language):
        self.language = language

    def get_unique_tag_spans(self):
        '''Get a list of unique token spans
        for visualizing a complete article along
        with all extracted facts.
        Each extracted report has its own list of spans
        which may in some cases overlap, particularly
        for date and location tags.
        '''
        ### need to deal with overlapping spans
        all_spans = []
        for report in self.reports:
            all_spans.extend(report.tag_spans)
        unique_spans = list({v['start']: v for v in all_spans}.values())
        unique_spans = sorted(unique_spans, key=lambda k: k['start'])
        ### Check for no overlap
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
                new_span['type'] = ", ".join([current_last_span['type'], span['type']])
                new_span['start'] = current_last_span['start']
                new_span['end'] = max(current_last_span['end'], span['end'])
                non_overlapping_spans[-1] = new_span
                current_end = new_span['end']

        return non_overlapping_spans

    def tag(self, tag):
        """Use interpreter to tag article
        """
        self.tag = tag

    def parse(self):
        """Use interpreter to parse article
        """
        pass

    def get_pub_date_string(self):
        return date_time_converter(self.publication_date)
