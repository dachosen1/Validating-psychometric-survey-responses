import os
from pathlib import Path

import pandas as pd

path = Path("./data")  # CHANGE THIS TO YOUR WORKING DIRECTORY
os.listdir(path)

mouse = pd.read_csv(path / "mouse-flat.csv")  # note: we are loading the flat file
votes = pd.read_csv(path / "votes.csv")

votes_grouped = votes.groupby("user_id")
user_id, validation = [], []
for user, df in votes_grouped:
    # according to data description, users must pass atleast 4 of the six validaiton questions
    passes = 0
    # check 1
    if int(df[df.value == "bf_validation_1"].score) == int(df[df.value == "bf_1"].score): passes += 1
    # check 2
    if int(df[df.value == "bf_validation_2"].score) == int(df[df.value == "bf_21"].score): passes += 1
    # check 3
    if int(df[df.value == "miq_validation_3"].score) in [2, 4]: passes += 1
    # check 4
    if int(df[df.value == "miq_validation_4"].score) in [2, 4]: passes += 1
    # check 5
    if int(df[df.value == "pgi_validation_5_Liking"].score) == 6 or int(
            df[df.value == "pgi_validation_5_Competence"].score) == 6: passes += 1
    # check 6
    if int(df[df.value == "pgi_validation_6_Liking"].score) == 4 or int(
            df[df.value == "pgi_validation_6_Competence"].score) == 4: passes += 1

    # appending to lists
    user_id.append(user)
    if passes >= 4:
        validation.append(True)
    else:
        validation.append(False)

validations = pd.DataFrame({"user_id": user_id, "validation": validation})

validations.to_csv(path / "validations.csv", index = False)

# ignore this cell
for i in votes.value:
    if "validation_5" in i:
        print(i)

mouse_val = pd.merge(mouse, validations, on = "user_id", how = "left")
