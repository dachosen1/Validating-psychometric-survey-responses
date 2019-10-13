import json

import numpy as np
import pandas as pd

mouse = pd.read_csv("Data/Raw/mouse_paths.csv")
votes = pd.read_csv("Data/Raw/votes.csv")

# these indices contain incomplete frames data
broken = [393, 409, 416, 428, 582, 613, 687, 809]
broken_uids = [mouse.user_id[i] for i in broken]

# these indices contain incomplete frames data
broken = [393, 409, 416, 428, 582, 613, 687, 809]
broken_uids = [mouse.user_id[i] for i in broken]

# drop the broken indicies
mouse.drop(broken, axis = 0, inplace = True)

# preparing the mouse data for flattening vy first adding the time elapsed, window_x and window_y cols
time_elapsed, window_x, window_y = [], [], []

for index, row in mouse.iterrows():
    d = dict(json.loads(mouse.path[index]))
    time_elapsed.append(d["timeElapsed"])
    window_x.append(dict(d['window'])["width"])
    window_y.append(dict(d['window'])["height"])


# function to create a new row for each frames movement
def flatten_df(df):
    """
    input mouse df with a json column, path, and return df with flattened df cols
    """
    user_id, action, cord_x, cord_y, radio, time_since = [], [], [], [], [], []
    for index, row in df.iterrows():
        f = dict(json.loads(row.path))['frames']
        for i in range(len(f)):
            user_id.append(row.user_id)
            action.append(f[i][0])
            cord_x.append(f[i][1])
            cord_y.append(f[i][2])
            if f[i][0] == "c":
                assert len(f[i]) == 5
                radio.append(f[i][3])
                time_since.append(f[i][4])
            else:
                radio.append(np.nan)
                time_since.append(f[i][3]) if i != 0 else time_since.append(
                    0)  # since len(f[i][0]) = 3 i.e. [s,0,0], indexing at 3 results in an error

    res = pd.DataFrame({"user_id": user_id,
                        "action": action,
                        "cord_x": cord_x,
                        "cord_y": cord_y,
                        "radio": radio,
                        "time_since": time_since})
    res.time_since.replace("None", np.nan, inplace = True)  # replace None string with np.nan for time_since
    df.drop("path", inplace = True, axis = 1)
    return pd.merge(res, df, how = "left", on = "user_id")


mouse_flat = flatten_df(mouse)
mouse_flat.to_csv("Data/mouse-flat.csv")
