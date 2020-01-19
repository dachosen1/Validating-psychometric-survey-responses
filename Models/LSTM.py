import re

import pandas as pd
import panel as pn
from fastai import *
from fastai import *
from fastai.tabular import *
from fastai.tabular import *
from fastai.text import *
from fastai.text import *
from fastai.text import *

df = pd.read_csv("data/id_direction_list.csv")

pat1 = re.compile("[.0]*[,\[\]\']*")
df["direction_list"] = df["direction_list"].apply(lambda x: re.sub(pat1, "", x))
df["direction_list"] = df["direction_list"].apply(lambda x: x.lower())

validations = pd.read_csv("data/validations.csv")
df = df.merge(validations, on = "user_id")
df = df.sample(frac = 1, random_state = 2019).reset_index(drop = True)
split = round(len(df) - (.3 * len(df)))
train = df.loc[:split]
val = df.loc[split:]

rus = RandomUnderSampler(random_state = 2019)
X, y = rus.fit_resample(train.drop("validation", axis = 1), train.validation)

train_clas = pd.DataFrame(X)
train_clas["4"] = y
train_clas.columns = df.columns

pn.extension()
pn.extension('katex')


def select_row(row = 0):
    return df[df.index == row]


pn.interact(select_row, row = (0, len(df) - 1))

# Language model data
data_lm = TextLMDataBunch.from_df(".", train, val, text_cols = "direction_list", mark_fields = False)
# Classifier model data
data_clas = TextClasDataBunch.from_df(".", train_clas, val, text_cols = "direction_list", label_cols = "validation",
                                      vocab = data_lm.train_ds.vocab, bs = 8, )

moms = (0.8, 0.7)

learn = language_model_learner(data_lm, AWD_LSTM, drop_mult = 0.5)
learn.unfreeze()
learn.lr_find()
learn.recorder.plot()

learn.fit_one_cycle(5, slice(1e-2), moms = moms)

learn.save_encoder('enc')
learn = text_classifier_learner(data_clas, AWD_LSTM)
learn.load_encoder('enc')

learn.lr_find()
learn.recorder.plot()

learn.fit_one_cycle(2, slice(1e-5, 1e-3), moms = moms)
learn.unfreeze()
learn.fit_one_cycle(8, slice(1e-5, 1e-3), moms = moms)
