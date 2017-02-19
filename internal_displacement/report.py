class Report(object):
    """Contains reporting term, unit, quantity, date(s) and location(s)
        ----------
        locations:              identified location names:String
        date_time:              the estimated date of the event:String
        event_term:             the reporting term:String
        subject_term:           the reporting unit:String
        quantity:               the quantity of units affected:String
        story:                  the original story:String
        tag_spans:              the spans for visualization identified tags:List of Dicts
    """

    def __init__(self, locations, date_time, event_term, subject_term, quantity, story, tag_spans=[]):
        self.locations = locations
        self.date_time = date_time
        self.event_term = event_term
        self.subject_term = subject_term
        self.quantity = quantity
        self.story = story
        self.tag_spans = tag_spans

    def display(self):
        print("Location: {}  DateTime: {}  EventTerm: {}  SubjectTerm:  {}  Quantity: {}"
              .format(self.locations, self.date_time, self.event_term, self.subject_term, self.quantity))
