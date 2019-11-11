import os
import pandas as pd
import numpy as np
import collections

# set working directory (Change for youe)
os.chdir('C:/Users/ander/Google Drive/Columbia/Fall 2019/Capstone/Dotin-Columbia-Castone-Team-Alpha-')

# initilize path
mouse_flat_path = 'Data/Clean Data/mouse_flat_v4.csv'

# read file
data = pd.read_csv(mouse_flat_path)

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
subset_radio = data.loc[:,['user_id', 'radio']]
subset_radio = subset_radio.dropna(subset = ['radio'])
user_completion = subset_radio.groupby('user_id').count() >= 196
user_completion = user_completion[user_completion['radio'] == True].reset_index()
user_id_who_completed_survey = pd.DataFrame(user_completion['user_id'])
completed_survey_data = data[data.user_id.isin(user_id_who_completed_survey.user_id)].reset_index()
completed_survey_data = completed_survey_data.drop(columns = ['Index','index'])

coordinates =  completed_survey_data[['user_id','cord_x', 'cord_y','action']].to_numpy()


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

    for user in user_id:
        index = coord_data[:, 0] == user
        new_index = coord_data[index]

        id_updated = new_index[1:, 0]
        action_updated = new_index[1:, 3]

        distance_x = new_index[1:, 1] - new_index[:len(new_index) - 1, 1]
        distance_y = new_index[1:, 2] - new_index[:len(new_index) - 1, 2]

        total_x = np.append([total_x], [distance_x])
        total_y = np.append([total_y], [distance_y])

        user_id_list = np.append([user_id_list], [id_updated])
        action_list = np.append([action_list], [action_updated])

    return total_x, total_y, user_id_list, action_list


def parse_directions(id_list, x_coord, y_coord, action):
    """
    Converts coordinate changes into Cardinal direction.

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



