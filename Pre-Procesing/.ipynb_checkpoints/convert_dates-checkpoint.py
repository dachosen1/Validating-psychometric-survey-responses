import pandas as pd

# import data
votes = pd.read_csv('Data/Raw/votes.csv')


def convert_date(df):
    """
    Function to convert a date pandas series into into date, time, and weekday name
    """

    date_time = pd.to_datetime(df)
    date = date_time.dt.date
    time = date_time.dt.time
    weekday_name = date_time.dt.day_name()

    return date, time, weekday_name


# apply function
votes['created_date'], votes['created_time'], votes['created_weekday'] = convert_date(votes['created_at'])

# drop unused columns
votes = votes.drop(columns = ['created_at', 'updated_at'])

votes.to_csv("Data/votes_modified.csv")
