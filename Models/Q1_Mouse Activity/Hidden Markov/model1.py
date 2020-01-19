import warnings

import hmm_scaled
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pyod.models.iforest import IForest
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")


def generate_dic(items):
    """ Genderates a dictionay for all values in item """
    new_dic = {}
    count = 0
    for unique in items:
        new_dic[unique] = count
        count += 1
    return new_dic


def column_scaler(data):
    """
    scales each column of data
    """
    scaler = StandardScaler()
    for value in data.columns:
        data_sub_ = pd.DataFrame(data.loc[:, value])
        data.loc[:, value] = scaler.fit_transform(data_sub_)
    return data


def kmean_prop(data, column):
    data_value = data.groupby(column).agg(count = pd.NamedAgg(column = column, aggfunc = 'count'))
    percentage = []
    for i in range(0, len(data_value)):
        result = round(((data_value.iloc[i, 0] / len(data)) * 100), 2)

        percentage.append(result)
    data_value['percentage (%)'] = percentage

    return data_value


def PCA_Col_names(count):
    """
    Remove columns in a PCA that meets the threshold count
    """
    colname = []
    rowname = 1
    while rowname <= count:
        colname.append(f'Principle Component {rowname}')
        rowname += 1
    return (colname)


# set working directory (Change for youe)
data = pd.read_csv('Models/Q1_Mouse Activity/Data/direction_data.csv')
data = data.drop(columns = 'Unnamed: 0')

unique_user = set(data['User Id'])

user_to_include = []
for user in unique_user:
    user_thresh_hold = data[data['User Id'] == user]['Page count'].value_counts() <= 100
    if sum(np.where(user_thresh_hold.values == False, 1, 0)) == 15:
        user_to_include.append(user)

# create a list with all the page number
page_number_list = []
for value in range(1, 16):
    page_ = f'page {value}'
    page_number_list.append(page_)

## limit page observation per page
final_data = data[0:0]

for page in range(0, len(page_number_list)):
    observation_limit = 200
    page_subset = data[data['Page count'] == page_number_list[page]]
    page_shrunk = page_subset[page_subset.observation <= observation_limit]
    page_ = page_shrunk.groupby('User Id').count()['observation']
    user_list = page_[page_ == observation_limit].index
    updated_dat = page_shrunk[page_shrunk['User Id'].isin(user_list)]
    final_data = pd.concat([final_data, updated_dat])

# count obse
for page in range(0, 15):
    pages___ = final_data[final_data['Page count'] == page_number_list[page]]
    user_count = len(pages___.groupby('User Id').count()['observation'])
    print(f' Page {page + 1}: {user_count}')

unique_page = set(data['Page count'])

final_data = data
user_list = []
page_count_list = []
for user in unique_user:
    user_list.append(user)
    num_pages_completed = len(set(data[data['User Id'] == user]['Page count']))
    page_count_list.append(num_pages_completed)

num_pages_user = pd.DataFrame({'User Id': user_list,
                               'Num page': page_count_list})

user_completed_all_page = num_pages_user[num_pages_user['Num page'] == 15]['User Id'].values

data = data[data['User Id'].isin(user_completed_all_page)]

user_direction = data[['User Id', 'Page count', 'Direction']]
flatten_data = user_direction.groupby(['User Id', 'Page count'], as_index = False).agg(list)

user_dict = generate_dic(set(data['Direction']))

direction_numerized = []
for row in range(0, len(flatten_data)):
    value = flatten_data.iloc[row, 2]
    numerized = [user_dict.get(key, value) for key in value]
    direction_numerized.append(numerized)
flatten_data['Direction Numerized'] = direction_numerized

page_number_list = []
for value in range(1, 16):
    page_ = f'page {value}'
    page_number_list.append(page_)

user_fraud_matrix = pd.DataFrame(data = 0, index = user_completed_all_page, columns = unique_page)
user_fraud_matrix = user_fraud_matrix[page_number_list]

hmm = hmm_scaled.HMM(hidden_states = 2)

for count in range(0, len(page_number_list)):
    page_ = flatten_data[flatten_data['Page count'] == page_number_list[count]]
    page_ = page_.set_index('User Id')
    hmm.fit(list(page_['Direction Numerized']))
    for index in user_fraud_matrix.index:
        try:
            user_fraud_matrix.loc[index, page_number_list[count]] = hmm.log_likelihood(
                page_.loc[index, 'Direction Numerized'])
        except KeyError:
            continue

# isolation forest
user_fraud_matrix = pd.read_csv('Models/Q1_Mouse Activity/Data/user_fraud_matrix.csv', index_col = 'Unnamed: 0')
user_fraud_matrix_scaled = column_scaler(user_fraud_matrix)
user_fraud_matrix_scaled = user_fraud_matrix_scaled[page_number_list]

fig = plt.figure(figsize = (16, 10))
corr = user_fraud_matrix_scaled.corr()

# Generate a mask for the upper triangle
mask = np.zeros_like(corr)
mask[np.triu_indices_from(mask)] = True

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap = True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask = mask, cmap = cmap, center = 0,
            square = True)
plt.title('Probability correlation by page')
plt.show()

iforest_1 = IForest(behaviour = "new", bootstrap = True, n_jobs = -1, )
iforest_1 = iforest_1.fit_predict(user_fraud_matrix_scaled)
unique, counts = np.unique(iforest_1, return_counts = True)

user_fraud_matrix_scaled['Iforest_1'] = np.where(iforest_1 == 0, 'Normal', 'Risk')
user_fraud_matrix_scaled.to_csv('Models/Q1_Mouse Activity/Data/user_fraud_matrix_labeled.csv')
user_fraud_matrix_scaled[user_fraud_matrix_scaled.Iforest_1 == 'Risk']

validations = pd.read_csv('Data/validations.csv')
validations_userid_fraud = validations[validations.validation == False]['user_id']
results_over_lap = validations_userid_fraud.isin(
    user_fraud_matrix_scaled[user_fraud_matrix_scaled.Iforest_1 == 'Risk'].index)
validations_userid_fraud[results_over_lap == True]

user_direction_summary = pd.read_csv('Models/Q1_Mouse Activity/Data/user_direction_summary.csv')
user_direction_summary = user_direction_summary.drop(columns = 'Unnamed: 0')


def plot_movement(user_id, page_number, user_label):
    user_data = user_direction_summary[user_direction_summary['user_id'] == user_id]
    user_data = user_data[user_data['direction'] == page_number]
    plt.plot('cord_x', 'cord_y', data = user_data)
    plt.xlim(0, 1366)
    plt.ylim(0, 728)
    plt.title(f'User {user_id} mouse movement for {page_number}: {user_label} ')
    plt.show()
