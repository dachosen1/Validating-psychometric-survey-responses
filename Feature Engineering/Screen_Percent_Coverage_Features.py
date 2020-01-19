import numpy as np
import pandas as pd

df = pd.read_csv("Data/mouse-flat.csv")

df_u_365 = df[df['user_id'] == 365]
# create separate arrays for x and y cords
cord_x_u365 = np.array(df_u_365['cord_x'])
cord_y_u365 = np.array(df_u_365['cord_y'])

# get absolute diff between adjacent items in array. get two interim distance arrays id_x and id_y
id_x = abs(np.diff(cord_x_u365))
id_y = abs(np.diff(cord_y_u365))


def calc_total_dist_x(idx):
    """Calculate total distance x based on interim distances x """
    # initialize total distance x
    td_x = 0

    # array to store total distance x incrementing
    td_x_array = []

    for i in range(len(idx)):
        td_x = td_x + idx[i]
        td_x_array.append(td_x)
    return td_x_array


td_x = calc_total_dist_x(id_x)


def calc_total_dist_y(idy):
    """Calculate total distance x based on interim distances x """
    # initialize total distance y
    td_y = 0

    # array to store total distance x incrementing
    td_y_array = []

    for j in range(len(idy)):
        td_y = td_y + idy[j]
        td_y_array.append(td_y)
    return td_y_array


td_y = calc_total_dist_y(id_y)

# last value of td_x and td_y is what we care about - that's the total aggregated value td=td+id
td_x[-1]
td_y[-1]

# calculate % width of screen covered for user 365
percent_width_u365 = td_x[-1] / window_u365[0][1]

# calculate % height of screen covered for user 365
percent_height_u365 = td_y[-1] / window_u365[0][0]
