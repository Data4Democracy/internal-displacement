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
    Accepts the dataframe created by prepareDataset, preprocesses using tf-idf, 
    and evaluates the provided model using cross-validation.
    '''
    X = dataframe.Text.values
    tags = dataframe.Tag.values
    count_vect = CountVectorizer()
    tfidf_transformer = TfidfTransformer()
    pipeline = make_pipeline(count_vect,tfidf_transformer,model)
    return cross_val_score(pipeline,X,tags)




d = pd.read_csv("datasets/IDMC Unite Ideas - Training dataset - TrainingDataset.csv")
d = d[~d.URL.str.contains("pdf")] 
# beautifulsoup was not coping with pdfs, so  I have removed these.
df_with_texts = prepareDataset(d.head(20))


# basic multinomial naive bayes as a proof of concept. Other models can be substituted.
model = MultinomialNB()
scores = evaluateModel(df_with_texts,model)
print(scores)
