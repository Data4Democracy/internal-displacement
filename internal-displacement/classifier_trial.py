

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

def evaluateModel(model,articles,scoring = None ):
    '''
    Accepts an sklearn model or pipeline and evaluates using cross-validation.
    Parameters
        ----------
        model: an sklearn model or pipeline

        articles: a list of article objects. These should possess instantiated label values. 
        scoring: a scoring function of the form score = scoring(estimator,X,y)

        Returns
        -------
        The cross-validation scores for the prediction accuracy of the model.

    '''
    texts = list(map(lambda x: x.content, articles))
    try:
        labels = list(map(lambda x: x.label,articles))
    except exception as e:
        print("This method requires labeled articles for training")
    return cross_val_score(model,texts,labels,scoring=scoring)











if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python classifier_trial.py <path_to_csv_file>")
    count_vect = CountVectorizer()
    tfidf_transformer = TfidfTransformer()
    nb_model = MultinomialNB()
    pipeline = make_pipeline(count_vect,tfidf_transformer,nb_model)
    df = pd.read_csv(sys.argv[1])
    scraper = Scraper(df.URL)
    articles = scraper.export_all_articles(df)


    scores = evaluateModel(pipeline,articles)
    print("CV Scores: ",scores)


