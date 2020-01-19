import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# call in data
mt = pd.read_csv('../Data/Clean Data/mouse_flat_V3.csv')
v = pd.read_csv('../Data/Raw/votes.csv')

# Create two new features to capture x,y coordinates but improved, to account for variability in window size

# ratio of cord_x / window_x * 100 - % of width
mt['percent_cord_x'] = (mt['cord_x'] / mt['window_x']) * 100

# ratio of cord_y / window_y * 100 - % of length
mt['percent_cord_y'] = (mt['cord_y'] / mt['window_y']) * 100


def overall_heatmap(userid):
    user_cords = mt[mt.user_id == userid]
    cords = user_cords[['cord_x', 'cord_y', 'window_x', 'window_y']]

    x = user_cords['percent_cord_x'].to_numpy()
    y = user_cords['percent_cord_y'].to_numpy()

    heatmap, xedges, yedges = np.histogram2d(x, y, bins = 100)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    print(userid)
    plt.clf()
    plt.imshow(heatmap.T, extent = extent, origin = 'lower')
    plt.show()


for userid in mt.user_id.unique():
    overall_heatmap(userid)


    def clicks_heatmap(userid):
        user_cords = mt[mt.user_id == userid]


    cords = user_cords[['cord_x', 'cord_y', 'window_x', 'window_y']]
    user_clicks = user_cords[user_cords.action == 'c']

    x = user_clicks['percent_cord_x'].to_numpy()
    y = user_clicks['percent_cord_y'].to_numpy()

    heatmap, xedges, yedges = np.histogram2d(x, y, bins = 100)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    print(userid)
    plt.clf()
    plt.imshow(heatmap.T, extent = extent, origin = 'lower')
    plt.show()


def movements_heatmap(userid):
    user_cords = mt[mt.user_id == userid]
    cords = user_cords[['cord_x', 'cord_y', 'window_x', 'window_y']]
    user_movements = user_cords[user_cords.action == 'm']

    x = user_movements['percent_cord_x'].to_numpy()
    y = user_movements['percent_cord_y'].to_numpy()

    heatmap, xedges, yedges = np.histogram2d(x, y, bins = 100)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    print(userid)
    plt.clf()
    plt.imshow(heatmap.T, extent = extent, origin = 'lower')
    plt.show()


def action_type_scatter(userid):
    user_cords = mt[mt.user_id == userid]
    cords = user_cords[['cord_x', 'cord_y', 'window_x', 'window_y']]

    sns.lmplot(x = "percent_cord_x", y = "percent_cord_y", data = user_cords, fit_reg = False, hue = 'action',
               legend = False, palette = dict(c = "#CD5C5C", m = "#E9967A", s = "#FFA07A"))

    plt.legend(loc = 'lower right')
    print(userid)
    plt.show()


for userid in mt.user_id.unique():
    action_type_scatter(userid)
