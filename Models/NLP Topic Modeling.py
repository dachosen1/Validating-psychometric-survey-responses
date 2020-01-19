import gensim
import nltk
import numpy as np
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *

df = pd.read_csv('Data/Extra/psyc_data.csv', error_bad_lines = False, index_col = None)

# remove special characters from item column
df['item'] = df['item'].replace('\W', ' ')
df['item'] = df['item'].replace('+AC0-', ' ')

# necessary step to get the preprocessing functions running- for some reason it's not
# considering all items as strings
df['item'] = df['item'].astype(str)

nltk.download('wordnet')
np.random.seed(300)


# lemmatizing and stemming text - we'll need to improve upon these
def lemmatize_stemming(text):
    stemmer = PorterStemmer()
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos = 'v'))


# Tokenize and lemmatize
def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 2:
            result.append(lemmatize_stemming(token))
    return result


processed_docs = train['item'].map(preprocess)

# create dictionary for processed_words with nr of times word appears in the dataset
dictionary = gensim.corpora.Dictionary(processed_docs)

# remove very rare (words appearing less than 10 times) and common words
# (words appearing in more than 10% of docs)
dictionary.filter_extremes(no_below = 10, no_above = 0.1)

# create bag of words corpus for the dictionary
bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

# train LDA model using BoW created
lda_model = gensim.models.LdaMulticore(bow_corpus,
                                       num_topics = 10,
                                       id2word = dictionary,
                                       passes = 2,
                                       workers = 2)

# inspect the words occuring in each topic and their relative weight
for idx, topic in lda_model.print_topics(-1):
    print("Topic: {} \nWords: {}".format(idx, topic))
    print("\n")

###HERE WE NEED TO GIVE THESE OUTPUT TOPICS SOME NAMES###

# testing on one document from the test set
num = 100
unseen_document = test.item[num]

# Data preprocessing step for the unseen document
bow_vector = dictionary.doc2bow(preprocess(unseen_document))

for index, score in sorted(lda_model[bow_vector], key = lambda tup: -1 * tup[1]):
    print("Score: {}\t Topic: {}".format(score,
                                         lda_model.print_topic(index, 5)))  # you can change the number to be anything

# for all data in the test dataset
test_unseen = list(test['item'])

for i in range(len(test_unseen)):
    test_unseen_dict = []
    bow_vector = dictionary.doc2bow(preprocess(i))
    test_unseen_dict.append(bow_vector)
return test_unseen_bow_vector

for i in test_unseen_bow_vector:
    for index, score in sorted(lda_model[i], key = lambda tup: -1 * tup[1]):
        print("Score: {}\t Topic: {}".format(score, lda_model.print_topic(index)))

        ###still needs to be completed###

# call in test dataset (our question dataset) and see LDA model performance
test_df = pd.read_csv('Data/Extra/survey_questions_with_id_final.csv')

# turn questions to list
test_documents = list(test_df['question'])
# Perform data preprocessing step for the test dataset
for i in range(len(test_documents)):
    testdoc_unseen_dict = []
    bow_vector = dictionary.doc2bow(preprocess(i))
    test_unseen_dict.append(bow_vector)
return testdoc_unseen_bow_vector

for i in testdoc_unseen_bow_vector:
    for index, score in sorted(lda_model[i], key = lambda tup: -1 * tup[1]):
        print("Score: {}\t Topic: {}".format(score, lda_model.print_topic(index)))

###still needs to be completed###
