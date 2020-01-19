import os

import numpy as np
import pandas as pd

os.chdir("Data/Clean Data")
df = pd.read_csv("Data/Clean Data/mouse_flat_v3.csv", index_col = 0)

# filter dataset by action = "c" only
df_clicks = df[df['action'] == 'c']

df_clicks_grouped = df_clicks.groupby('user_id')['time_since'].apply(list).reset_index(name = 'time_since')


def calc_avg_delay_btwn_clicks(df):
    # calc difference of time in clicks
    diff = abs(np.diff(df['time_since']))

    # calculate average delay of clicks per user based on difference above
    avg_calc = sum(diff) / len(diff)
    return avg_calc


df_clicks_grouped['average_click_delay'] = df_clicks_grouped.apply(lambda x: calc_avg_delay_btwn_clicks(x), axis = 1)
# Load new file and concat:
data = pd.read_csv("Data/Clean Data/merged_data_user_level.csv", index_col = 0)
data.insert(loc = data.columns.get_loc('click count') + 1, column = "average_click_delay",
            value = df_clicks_grouped.average_click_delay)

data.to_csv(r"merged_data_user_level_V2.csv")
