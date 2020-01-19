from pathlib import Path

import numpy as np
import pandas as pd

# set path directory
path = Path("./Data")
# read in the data
votes = pd.read_csv(path / "votes_modified.csv")


def get_min_response(df):
    """Create new column to capture absolute min response (aka 1) as 1=yes, 0=no"""
    if df['score'] == 1:
        return 1
    else:
        return 0


votes['is_min_response?'] = votes.apply(lambda x: get_min_response(x), axis = 1)


def get_max_response(df):
    """Create new column to capture absolute max response (aka 5 or 7 depending on question) as 1=yes, 0=no"""
    if "pgi_" in df['value']:
        if df['score'] == 7:
            return 1
        else:
            return 0
    else:
        if df['score'] == 5:
            return 1
        else:
            return 0


votes["is_max_response?"] = votes.apply(lambda x: get_max_response(x), axis = 1)


# function to group survey responses by type and see if they have been responded as an absolute min and max
# as an aggregate

def create_question_buckets(df):
    """Create a new column to bucket questions by category"""
    if "bf_" in df['value']:
        return "bf_questions"
    elif "bs_" in df['value']:
        return "bs_questions"
    elif "miq_" in df['value']:
        return "miq_questions"
    elif "_Liking" in df['value']:
        return "pgi_liking_questions"
    else:
        return "pgi_competence_questions"


votes['value_category'] = votes.apply(lambda x: create_question_buckets(x), axis = 1)

# ABSOLUTE MIN/MAX RESPONSE CALCULATIONS#

# create pivot table for absolute min/max answer to aggregate information

abs_minmax_pivot_table = pd.pivot_table(votes, index = ['value_category', 'user_id'], values = ['is_min_response?',
                                                                                                'is_max_response?'],
                                        aggfunc = [np.sum, len])

# turn pivot table to regular dataframe
abs_minmax_pivot_table.columns = abs_minmax_pivot_table.columns.droplevel(0)
abs_minmax_votes = abs_minmax_pivot_table.reset_index().rename_axis(None, axis = 1)

# change column names for is_min_responses
abs_minmax_votes.columns = ['value_category', 'user_id', 'sum_max_resp_occurrence', 'sum_min_resp_occurrence',
                            'total_count_of_cat_questions', 'total_count_of_cat_questions_2']

del abs_minmax_votes['total_count_of_cat_questions_2']


# function to capture users who have selected only absolute min or max per question category

def abs_min_users_per_cat(df):
    """Create new column to capture users who have full absolute min response across categories"""

    if df['sum_min_resp_occurrence'] == df['total_count_of_cat_questions']:
        return 1
    else:
        return 0


abs_minmax_votes['full_abs_min_response'] = abs_minmax_votes.apply(lambda x: abs_min_users_per_cat(x), axis = 1)


def abs_max_users_per_cat(df):
    """Create new column to capture users who have full absolute min response across categories"""

    if df['sum_max_resp_occurrence'] == df['total_count_of_cat_questions']:
        return 1
    else:
        return 0


abs_minmax_votes['full_abs_max_response'] = abs_minmax_votes.apply(lambda x: abs_max_users_per_cat(x), axis = 1)

absolute_response_features = votes.to_csv(path / "absolute_response_features.csv")
users_with_abs_minmax_responses = abs_minmax_votes.to_csv(path / "users_with_absolute_response_features.csv")
