import gensim
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
import re
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from pprint import pprint
import numpy as np
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize
from nltk.corpus import stopwords
path = "./Data/Feature Engineering"
lemma = WordNetLemmatizer()


model = gensim.models.KeyedVectors.load_word2vec_format('/Users/luislosada/PycharmProjects/Anomaly_Detection/models/GoogleNews-vectors-negative300.bin', binary=True)

data = pd.read_csv("/Users/luislosada/PycharmProjects/Dotin-Columbia-Castone-Team-Alpha-/Data/Extra/survey_questions_with_id_final.csv")

questions = data["question"]
questions =[re.sub(r'[^\w\s]','', str(x)) for x in questions]
questions = [new_str.lower() for new_str in questions]

def tokenize(words):
    lst = []
    tokenlst = []
    for i in range(len(words)):
        lst = list(word_tokenize(words[i]))
        tokenlst.append(lst)
    return tokenlst

words = tokenize(questions)

def cleanup_pretokenize(text):
    text = re.sub(r'http\S+', '', text)
    text = text.replace("'s", " ")
    text = text.replace("n't", " not ")
    text = text.replace("'ve", " have ")
    text = text.replace("'re", " are ")
    text = text.replace("I'm"," I am ")
    text = text.replace("you're"," you are ")
    text = text.replace("You're"," You are ")
    text = text.replace("-"," ")
    text = text.replace("/"," ")
    text = text.replace("("," ")
    text = text.replace(")"," ")
    text = text.replace("%"," percent ")
    return text


sw = stopwords.words('english')
for l in words:
    for word in l:
        if word in sw:
            l.remove(word)

for l in words:
    for word in l:
        cleanup_pretokenize(word)
l=[]
i,j=0,0
ll=[]
for m in words:
    for word in m:
        l.append(lemma.lemmatize(word))
    ll.append(l)
    l=[]


def wordvec(words):
    tokens = []
    bad = []
    ind=[]
    c = 0
    for list in words:
        for word in list:
            try:
                tokens.append(model[word])
                c+=1
            except KeyError:
                bad.append(word)
                ind.append(c)
                c=+1
    #x = {'word':bad,'row':ind}
    #bb = pd.DataFrame(x)
    return (tokens)

wordvec = wordvec(ll)
#words_to_fix = list(np.unique(wordvec[1]['word']))
#pprint(words_to_fix)




index2word_set = set(model.wv.index2word)

def avg_feature_vector(sentence, model, num_features, index2word_set):
    words = sentence.split()
    feature_vec = np.zeros((num_features, ), dtype='float32')
    n_words = 0
    for word in words:
        if word in index2word_set:
            n_words += 1
            feature_vec = np.add(feature_vec, model[word])
    if (n_words > 0):
        feature_vec = np.divide(feature_vec, n_words)
    return feature_vec

#with open('words_to_fix.json', 'w') as json_file:
 #   json.dump(words_to_fix, json_file)


np.random.seed(100)
tsne_model = TSNE(perplexity=100, n_components=2, init='pca',metric='cosine', n_iter=5000, random_state=23)
new_values = tsne_model.fit_transform(wordvec)

def label(words):
    labels = []
    for word in words:
        labels.append(word)
    return labels

vector_of_words = pd.DataFrame(new_values)
label_for_vector = label(words)
label_for_vector = pd.Series([item for sublist in label_for_vector for item in sublist])

vector_of_words['labels'] = label_for_vector



def plotvec(tsne_value,labels):
    x = []
    y = []
    for value in tsne_value:
        x.append(value[0])
        y.append(value[1])

    plt.figure(figsize=(16, 16))
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        try:
            plt.annotate(labels[i],
                         xy=(x[i], y[i]),
                         xytext=(5, 2),
                         textcoords='offset points',
                         ha='right',
                         va='bottom')
        except IndexError:
            plt.annotate(" ",
                         xy=(x[i], y[i]),
                         xytext=(5, 2),
                         textcoords='offset points',
                         ha='right',
                         va='bottom')

    plt.show()

plotvec(new_values,label_for_vector)

vector_of_words.to_csv(r'vector_of_words.csv', index=True)