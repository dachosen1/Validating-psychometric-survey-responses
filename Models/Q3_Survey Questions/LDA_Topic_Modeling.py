import gensim
import nltk
import numpy as np
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
from nltk.stem.porter import *

nltk.download('wordnet')
np.random.seed(400)

# read in data
df = pd.read_csv('Data/Extra/psyc_data.csv')
del df['index']


# NEED BETTER DATA CLEANING / PREPROCESSING APPROACH ###

# Lemmatize and stem
def lemmatize_stemming(text):
    """Function to lemmatize and stem the text"""
    stemmer = PorterStemmer()
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos = 'v'))


# Tokenize and lemmatize
def preprocess(text):
    '''Function to preprocess the text'''
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            lemmatized_token = lemmatize_stemming(token)
            result.append(lemmatized_token)
    return result


# process all docs
processed_docs = df['item'].map(preprocess)

# view first 10 processed docs
processed_docs[:10]
# create dictionary
dictionary = gensim.corpora.Dictionary(processed_docs)

# remove very rare and very common words
dictionary = dictionary.filter_extremes(no_below = 15, no_above = 0.1, keep_n = 100000)

# with 10 topics - change if needed
lda_model = gensim.models.LdaMulticore(bow_corpus,
                                       num_topics = 10,
                                       id2word = dictionary,
                                       passes = 2,
                                       workers = 2)

for idx, topic in lda_model.print_topics(-1):
    print("Topic: {} \nWords: {}".format(idx, topic))
    print("\n")

# check topic prediction for one document in the dataset
for index, score in sorted(lda_model[bow_corpus[document_num]], key = lambda tup: -1 * tup[1]):
    print("\nScore: {}\t \nTopic: {}".format(score, lda_model.print_topic(index, 10)))

# pick the one with the highest probability score

# check topic prediction for an unseen doc
unseen_document = "I find it easy to explain things to others."

# Data preprocessing step for the unseen document
bow_vector = dictionary.doc2bow(preprocess(unseen_document))

for index, score in sorted(lda_model[bow_vector], key = lambda tup: -1 * tup[1]):
    print("Score: {}\t Topic: {}".format(score, lda_model.print_topic(index, 5)))
