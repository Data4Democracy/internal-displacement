

import sys
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from scrape_artlces import Scraper,Article
from sklearn.metrics import accuracy_score

def evaluateModel(model,articles,scoring = accuracy_score ):
    '''
    Accepts an sklearn model or pipeline and evaluates using cross-validation.
    Parameters
        ----------
        model: an sklearn model or pipeline

        articles: a list of article objects. These should possess instantiated label values. 

        Returns
        -------
        The cross-validation scores for the prediction accuracy of the model.

    '''
        texts = map(lambda x: x.content, articles)
        labels = map(lambda x: x.label)












if __name__ == "__main__":

    count_vect = CountVectorizer()
    tfidf_transformer = TfidfTransformer()
    nb_model = MultinomialNB()
    pipeline = make_pipeline(count_vect,tfidf_transformer,nb_model)
    df = 
    scraper = Scraper()
    articles = Scraper.


    scores = evaluateModel()



