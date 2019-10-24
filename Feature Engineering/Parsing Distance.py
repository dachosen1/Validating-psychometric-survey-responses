import pandas as pd
import numpy as np
import collections

# initilize path
mouse_flat_path = 'Data/Clean Data/mouse_flat_v2.csv'

# read file
data = pd.read_csv(mouse_flat_path)

coordinates = data[['user_id', 'cord_x', 'cord_y']].to_numpy()


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

    for user in user_id:
        index = coord_data[:, 0] == user
        new_index = coord_data[index]

        id_updated = new_index[1:, 0]

        distance_x = new_index[1:, 1] - new_index[:len(new_index) - 1, 1]
        distance_y = new_index[1:, 2] - new_index[:len(new_index) - 1, 2]

        total_x = np.append([total_x], [distance_x])
        total_y = np.append([total_y], [distance_y])
        user_id_list = np.append([user_id_list], [id_updated])

    return total_x, total_y, user_id_list


def parse_directions(id_list, x_coord, y_coord):
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

        if x == 0 and y == 0:
            directions.append('No Movement')
        elif x > 0 and y == 0:
            directions.append('East East')
        elif x < 0 and y == 0:
            directions.append('West West')
        elif x == 0 and y > 0:
            directions.append('North North')
        elif x == 0 and y < 0:
            directions.append('South South')
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

    return pd.DataFrame({'User Id': id_list,
                         'Distance X': x_coord,
                         'Distance Y': y_coord,
                         'Direction': directions})


# parse distance
coord_x, coord_y, coord_user = parse_distance(coordinates)

# parse direction
direction_data = parse_directions(coord_user, coord_x, coord_y)

direction_data.to_csv(f'Models/Q1_Mouse Activity/Data/direction_data.csv')
