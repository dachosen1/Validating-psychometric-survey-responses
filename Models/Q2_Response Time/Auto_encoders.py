import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pyod.models.auto_encoder import AutoEncoder
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, normalize

os.chdir("/Users/luislosada/Columbia Drive/Capstone - Fall 2019/Project Data")
data = pd.read_csv("final_outliers (1).csv", index_col = 0).reset_index(drop = True)

df = data[['user_id', 'scroll count', 'mouse movement count',
           'click count', 'Total Time', 'Total Distance', 'Max Score Value',
           'bf _votes_ 1 _count', 'bf _votes_ 5 _count', 'bf _votes_ 3 _count',
           'bs _votes_ 3 _count', 'pgi _votes_ 4 _count',
           'bs _votes_ 1 _count', 'bs _votes_ 4 _count', 'bs _votes_ 5 _count',
           'miq _votes_ 1 _count', 'miq _votes_ 2 _count', 'miq _votes_ 4 _count',
           'miq _votes_ 5 _count', 'pgi _votes_ 1 _count', 'pgi _votes_ 2 _count',
           'pgi _votes_ 3 _count', 'pgi _votes_ 5 _count', 'pgi _votes_ 7 _count',
           'bf _votes_ 4 _count', 'bf _votes_ 2 _count', 'bs _votes_ 2 _count',
           'pgi _votes_ 6 _count', 'measure_width_covered',
           'measure_height_covered', 'movesleft', 'movesright',
           'no_horizontal_movement', 'perc_left_movement', 'perc_right_movement',
           'perc_no_movement_x', 'movesup', 'movesdown', 'no_vertical_movement',
           'perc_upwward_movement', 'perc_downward_movement', 'perc_no_movement_y',
           'Max Speed', 'Avg Speed', 'Sd Speed', 'displacement',
           'displacement_time', 'speed', 'speed_times', 'acceleration',
           'acceleration_times', 'traj_step_angles', 'traj_heading', 'length', 'net_displacement',
           'stdevonsimilarquestions', 'read_time_seconds', 'timeElapsed',
           'factorofdifference', 'n_pages_with_same_value',
           'flag_pages_with_same_value']]

df.columns = df.columns.str.replace(' ', '')
data.columns = data.columns.str.replace(' ', '')
data = data.replace([np.inf, -np.inf], np.nan).dropna()

good_users = pd.read_csv(
    '/Users/luislosada/PycharmProjects/Dotin-Columbia-Castone-Team-Alpha/Data/Extra/List_Good_User.csv',
    index_col = 0).reset_index(drop = True)

ix = []
for a in data['user_id']:
    if a in list(good_users.iloc[:, 0]):
        ix.append(np.array(np.where(data['user_id'] == a)).tolist())

train_index = [item for sublist in [item for sublist in ix for item in sublist] for item in sublist]
test_index = [item for item in list(data.index) if item not in train_index]

train = data.loc[train_index, df.columns].reset_index(drop = False)
test = data.loc[test_index, df.columns].reset_index(drop = False)
train = train.apply(pd.to_numeric)
test = test.apply(pd.to_numeric)
train_x = train.drop(columns = ['user_id', 'index'])
test_x = test.drop(columns = ['user_id', 'index'])

np.any(np.isnan(train_x))
np.all(np.isfinite(train_x))
train_norm = StandardScaler().fit_transform(train_x.dropna())
test_norm = StandardScaler().fit_transform(test_x.dropna())

clf1 = AutoEncoder(hidden_neurons = [25, 2, 2, 25])
clf1.fit(train_norm)

y_train_scores = clf1.decision_scores_  # raw outlier scores

# get the prediction on the test data
y_test_pred = clf1.predict(test_norm)  # outlier labels (0 or 1)

y_test_scores = clf1.decision_function(test_norm)  # outlier scores

y_test_pred = pd.Series(y_test_pred)
y_test_scores = pd.Series(y_test_scores)

y_test_pred.value_counts()

y_test_scores.describe()

plt.hist(y_test_scores, bins = 'auto')
plt.title("Histogram for Model Clf1 Anomaly Scores")
plt.xlim(-1, 2)
plt.show()

df_test = test_x.copy()
df_test.insert(loc = 0, column = "user_id", value = test.dropna()['user_id'])
df_test['score'] = y_test_scores
df_test['cluster'] = np.where(df_test['score'] < 8, 1, 0)
df_test['cluster'].value_counts()

suspicious = df_test[(df_test['cluster'] == 1)]
non_out = df_test[(df_test['cluster'] == 0)]
inspect_df = pd.DataFrame({'mean_outliers': suspicious.describe().loc['mean', :],
                           'mean_non_outliers': non_out.describe().loc['mean', :]})
inspect_df.drop(['cluster'], inplace = True)

ins_2 = pd.DataFrame(StandardScaler().fit_transform(inspect_df.loc[['scrollcount', 'clickcount', 'TotalTime',
                                                                    'MaxScoreValue', 'stdevonsimilarquestions',
                                                                    'read_time_seconds', 'timeElapsed',
                                                                    'factorofdifference', 'n_pages_with_same_value',
                                                                    'flag_pages_with_same_value', 'score'], :]))

plt.figure(figsize = (20, 20))
x = list(inspect_df.loc[['scrollcount', 'clickcount', 'TotalTime',
                         'MaxScoreValue', 'stdevonsimilarquestions', 'read_time_seconds', 'timeElapsed',
                         'factorofdifference', 'n_pages_with_same_value',
                         'flag_pages_with_same_value', 'score'], :].index)
_X = np.arange(len(x))
leg = ['Outliers', 'Non Outliers']
plt.barh(_X - 0.2, ins_2.iloc[:, 0], 0.4, color = 'red')
plt.barh(_X + 0.2, ins_2.iloc[:, 1], 0.4, color = 'green')
plt.yticks(_X, x, fontsize = 20)  # set labels manually
plt.title('Outliers vs Non Outliers Stats', fontsize = 30)
plt.legend(leg, loc = (1.04, 0.8), fontsize = 20)
plt.show()

X = normalize(df_test.drop(columns = ['cluster']))
pca = PCA(n_components = 2)
X_pca = pca.fit_transform(X)

principalDf = pd.DataFrame(data = X_pca
                           , columns = ['principal component 1', 'principal component 2'])

finalDf = pd.concat([principalDf, df_test[['cluster']]], axis = 1)

fig = plt.figure(figsize = (20, 20))
plt.scatter(finalDf[finalDf['cluster'] == 1]['principal component 1'],
            finalDf[finalDf['cluster'] == 1]['principal component 2'], alpha = 0.75, c = 'red', label = 'Outlier')
plt.scatter(finalDf[finalDf['cluster'] == 0]['principal component 1'],
            finalDf[finalDf['cluster'] == 0]['principal component 2'], alpha = 0.75, c = 'green', label = "Non Outlier")
plt.title("Outliers Identified With an Autoencoder", fontsize = 30)
plt.xlabel('PC1', fontsize = 20)
plt.ylabel('PC2', fontsize = 20)
plt.legend(prop = {'size': 20})
plt.show()

df_test.to_csv("DF_autoenc.csv")
