import pandas as pd
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")


def parse_distance(coord_data):
    """
    Calculate the incremental coordinate for each mouse movement
    :param coord_data:
    :return: A seperate numpy array for the x, y, user id list.
    """
    user_id = np.unique(coord_data[:, 0])[1:]
    total_x = []
    total_y = []
    user_id_list = []
    action_list = []
    page_list = []

    for user in user_id:
        index = coord_data[:, 0] == user
        new_index = coord_data[index]

        id_updated = new_index[1:, 0]
        action_updated = new_index[1:, 3]
        page_updated = new_index[1:, 4]

        distance_x = new_index[1:, 1] - new_index[:len(new_index) - 1, 1]
        distance_y = new_index[1:, 2] - new_index[:len(new_index) - 1, 2]

        total_x = np.append([total_x], [distance_x])
        total_y = np.append([total_y], [distance_y])

        user_id_list = np.append([user_id_list], [id_updated])
        action_list = np.append([action_list], [action_updated])
        page_list = np.append([page_list], [page_updated])

    return total_x, total_y, user_id_list, action_list, page_list


def parse_directions(id_list, x_coord, y_coord, action):
    """
    Converts coordinate changes all mouse movements into Cardinal direction. Ignores scrolls and clicks

    :param id_list: Unique list of user ids
    :param x_coord: List of the changes in the x coordinate
    :param y_coord: List of the changes in the y coordinates
    :return: A data frame that contains the user id list, x directional changes, and y directional changes,
    calculated cardinal direction
    """

    directions = collections.deque()  # optimized for append operations

    for value in range(0, len(id_list)):

        x = x_coord[value]
        y = y_coord[value]

        action_value = action[value]

        if action_value == 'm':
            if x == 0 and y == 0:
                directions.append('No Movement')
            elif x > 0 and y == 0:
                directions.append('East')
            elif x < 0 and y == 0:
                directions.append('West')
            elif x == 0 and y > 0:
                directions.append('North')
            elif x == 0 and y < 0:
                directions.append('South')
            elif x > 0 and y > 0:
                directions.append('North East')
            elif x > 0 and y < 0:
                directions.append('North West')
            elif x < 0 and y < 0:
                directions.append('South West')
            elif x < 0 and y > 0:
                directions.append('South East')
            else:
                directions.append('TBD')
        else:
            directions.append(action_value)

    return pd.DataFrame({'User Id': id_list,
                         'Distance X': x_coord,
                         'Distance Y': y_coord,
                         'Direction': directions})


class page_description:
    """
    Class to analyze direction data. Purpose is to determine the movement count thresholdhold for hmm model.
    """

    def __init__(self, data, page_number):
        self.page_number = page_number
        self.page = direction_data[direction_data['Page count'] == f'page {self.page_number}']
        self.data = data

    def page_segment(self):
        """
        Desplays the user id belong to a that segment
        """
        page = self.data[self.data['Page count'] == f'page {self.page_number}']
        page = page.groupby('User Id').count()[['Page count']]
        return page

    def page_description(self):
        """
        Provide summary statistics on a page
        """

        return self.page_segment().describe()

    def percentage(self):
        """
        prints the percentage of the total number of counts recorded on this page
        """

        value = f' {round((len(self.page) / len(self.data)) * 100, 2)}% of all the mouse movemens are recorded in page {self.page_number}'

        return value


# initilize path
mouse_flat_path = 'Data/Clean Data/mouse_flat_v4.csv'

# read file
data = pd.read_csv(mouse_flat_path)

# remove duplicates
user_id_seqence = []

for i in range(1, len(data)):
    if data.iloc[i, 2] == data.iloc[i - 1, 2]:
        continue
    else:
        user_id_seqence.append(data.iloc[i, 2])

user_id_seq = pd.DataFrame({'user_id': user_id_seqence})
user_id_seq = user_id_seq['user_id'].value_counts()
multiple_survey = user_id_seq[user_id_seq > 1]
duplicate_ = multiple_survey.index
data = data[~data['user_id'].isin(duplicate_)]

# add page numbers
direction = data[['user_id', 'direction']].values
user_list = set(data.user_id)
page_movement = collections.deque()
for user in user_list:
    user_segment = direction[direction[:, 0] == user]
    count = 1
    for user, action in user_segment:
        if action == 'PageChange ,':
            count += 1
            user_movement = f'page {count}'
            page_movement.append(user_movement)
        else:
            user_movement = f'page {count}'
            page_movement.append(user_movement)

data.direction = page_movement

# filter users with less than 196 radio count, which is the number of questions in the data
subset_radio = data.loc[:, ['user_id', 'radio']]
subset_radio = subset_radio.dropna(subset = ['radio'])
user_completion = subset_radio.groupby('user_id').count() >= 196
user_completion = user_completion[user_completion['radio'] == True].reset_index()
user_id_who_completed_survey = pd.DataFrame(user_completion['user_id'])
completed_survey_data = data[data.user_id.isin(user_id_who_completed_survey.user_id)].reset_index()
completed_survey_data = completed_survey_data.drop(columns = ['Index', 'index'])

coordinates = data[['user_id', 'cord_x', 'cord_y', 'action', 'direction']].to_numpy()
# parse distance
coord_x, coord_y, coord_user, action_type, page_list = parse_distance(coordinates)

user_direction_summary = data[['user_id', 'action', 'cord_x', 'cord_y', 'window_x', 'window_y', 'direction']]
user_direction_summary.to_csv('Models/Q1_Mouse Activity/Data/user_direction_summary.csv', )

user_sytem = data[['user_id', 'system']].drop_duplicates()

# parse direction
direction_data = parse_directions(coord_user, coord_x, coord_y, action_type)
direction_data['Page count'] = page_list

# remove all clicks, scrolls, and np
direction_data = direction_data[-direction_data.Direction.isin(['c', 's', 'np'])]

page_number_list = []
for value in range(1, 16):
    page_ = f'page {value}'
    page_number_list.append(page_)

page_count = [1]
count = 1

for row in range(1, len(direction_data)):
    if direction_data.iloc[row, 4] == direction_data.iloc[row - 1, 4]:
        count += 1
        page_count.append(count)
    else:
        count = 1
        page_count.append(count)

# add observation
direction_data['observation'] = page_count

# remove all pages greater than 15
direction_data = direction_data[direction_data['Page count'].isin(page_number_list)]

direction_data.to_csv(f'Models/Q1_Mouse Activity/Data/direction_data.csv')
