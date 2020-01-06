import warnings

import matplotlib.pyplot as plt
import nltk
import pandas as pd
import re
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import GridSearchCV

warnings.filterwarnings('ignore')

stopwords = set(nltk.corpus.stopwords.words('english'))  # unique set of stopwords
df = pd.read_csv('./Data/Extra/psyc_data.csv',
                 error_bad_lines = False, index_col = 0)
[nltk.tokenize.word_tokenize(df.iloc[i, 0]) for i in range(len(df))]


def tokenize_titles():
    tokens = None
    lmtzr = WordNetLemmatizer()
    filtered_tokens = []

    for token in tokens:
        token = token.replace("'s", " ").replace("n’t", " not").replace("’ve", " have")
        token = re.sub(r'[^a-zA-Z0-9 ]', '', token)
        if token not in stopwords:
            filtered_tokens.append(token.lower())

    lemmas = [lmtzr.lemmatize(t, 'v') for t in filtered_tokens]

    return lemmas


# Fine tuning  Model
max_tf = 0.50
min_tf = 0.05
tf_vectorizer = CountVectorizer(max_df = max_tf, min_df = min_tf, max_features = 1000,
                                tokenizer = tokenize_titles, ngram_range = (3, 4))
data_vec = tf_vectorizer.fit_transform(df)
lda = LatentDirichletAllocation()
search_params = {'n_components': [5, 10, 15, 20, 25], 'learning_decay': [.5, .7, .9]}
model = GridSearchCV(lda, param_grid = search_params)

# Do the Grid Search
model.fit(data_vec)

gg = pd.DataFrame(model.cv_results_).sort_values(by = ['rank_test_score'])

n_topics = [5, 10, 15, 20, 25]
log_likelyhoods_5 = [round(gg.loc[i, 'mean_test_score']) for i in range(len(gg)) if
                     gg.loc[i, 'param_learning_decay'] == 0.5]
log_likelyhoods_7 = [round(gg.loc[i, 'mean_test_score']) for i in range(len(gg)) if
                     gg.loc[i, 'param_learning_decay'] == 0.7]
log_likelyhoods_9 = [round(gg.loc[i, 'mean_test_score']) for i in range(len(gg)) if
                     gg.loc[i, 'param_learning_decay'] == 0.9]

# Show graph
plt.figure(figsize = (12, 8))
plt.plot(n_topics, log_likelyhoods_5, label = '0.5')
plt.plot(n_topics, log_likelyhoods_7, label = '0.7')
plt.plot(n_topics, log_likelyhoods_9, label = '0.9')
plt.title("Choosing Optimal LDA Model")
plt.xlabel("Num Topics")
plt.ylabel("Log Likelyhood Scores")
plt.legend(title = 'Learning decay', loc = 'best')
plt.show()


# Final Topic Output
def clstr_lda(stories, max_, min_, lda_):
    # top words to be identified
    n_top_words = 10

    tf_vectorizer_ = CountVectorizer(max_df = max_, min_df = min_, max_features = 500,
                                     tokenizer = tokenize_titles, ngram_range = (3, 4))

    tf = tf_vectorizer_.fit_transform(stories)

    lda_ = lda_
    lda_.fit(tf)
    tf_feature_names = tf_vectorizer_.get_feature_names()

    # print top topic words
    topics_updated = dict()
    for topic_idx, topic in enumerate(lda_.components_):
        topics_updated[topic_idx] = [tf_feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
        print("Topic #%d:" % topic_idx)
        print(" | ".join([tf_feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))

    return topics_updated


topics = clstr_lda(10, feed_titles, 100, 0.01, model.best_estimator_)

best_lda_model = model.best_estimator_
