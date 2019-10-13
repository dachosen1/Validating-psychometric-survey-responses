import pandas as pd
import math


# set mouse flat path
mouse_flat_path = './Data/mouse-flat.csv'

# read data
mouse_data = pd.read_csv(mouse_flat_path)
mouse_data = mouse_data.drop(columns='Unnamed: 0')


def mouse_distance(x1, y1, x2, y2):
    """
    Calculates the euclidean distance between two vectors.
    return: Integer class object that represents the euclidean distance.
    """
    x1 = x1.astype(float)
    x2 = x2.astype(float)
    y1 = y1.astype(float)
    y2 = y2.astype(float)

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calc_distance(data):

    """
    Function to apply the mouse coordinate to calculate distance over a data frame
    """
    nrow = data.shape[0]
    distance = []

    if data['user_id'] == data['user_id'].shift(-1):
        for count in range(1, nrow):
            x1 = data['cord_x'][count]
            x2 = data['cord_x'].shift(-1)[count]

            y1 = data['cord_y'][count]
            y2 = data['cord_y'].shift(-1)[count]

            distance.append(mouse_distance(x1, y1, x2, y2))
    else:
        distance.append(0)

    return distance


total_distance = calc_distance(data=mouse_data)

