'''
This script will parse a csv file like the one here: https://docs.google.com/spreadsheets/d/1n1Sv8fCgGCw6555ckJ83z-sgWDKz5ydXkqpJXbcGD5g/edit?usp=sharing
It expects the path to the file to be listed as a command line argument when invoking the script.
It scrapes the urls associated with news story to extract the text.
It processes the texts to give tf-idf and prints the cross validation scores for the model.
'''


import sys
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from scrape_articles import removeNewline,textFromUrl,prepareDataset


def evaluateModel(dataframe,model):
    '''
    Accepts the dataframe created by prepareDataset in scrape_articles.py, preprocesses using tf-idf, 
    and evaluates the provided model using cross-validation.
    When more data is available a train test split step should be included.
    '''
    X = dataframe.Text.values
    tags = dataframe.Tag.values
    count_vect = CountVectorizer()
    tfidf_transformer = TfidfTransformer()
    pipeline = make_pipeline(count_vect,tfidf_transformer,model)
    return cross_val_score(pipeline,X,tags)




d = pd.read_csv(sys.argv[1])
d = d[~d.URL.str.contains("pdf")] 
# beautifulsoup was not coping with pdfs, so  I have removed these where possible.
df_with_texts = prepareDataset(d)


# basic multinomial naive bayes as a proof of concept. Other models can/should be substituted.
model = MultinomialNB()
scores = evaluateModel(df_with_texts,model)
print(scores)
