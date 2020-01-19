import os

import numpy as np
import pandas as pd

os.chdir("../../Data/Clean Data")
df = pd.read_csv("votes_v2.csv")


# boolean if user clicked on option 1 in the question
def get_response_1(df):
    """Create new column to capture absolute response=1 as 1=yes, 0=no"""
    if df['score'] == 1:
        return 1
    else:
        return 0


df['response_1'] = df.apply(lambda x: get_response_1(x), axis = 1)


# boolean if user clicked on option 2 in the question
def get_response_2(df):
    """Create new column to capture absolute response=2 as 1=yes, 0=no"""
    if df['score'] == 2:
        return 1
    else:
        return 0


df['response_2'] = df.apply(lambda x: get_response_2(x), axis = 1)


# boolean if user clicked on option 3 in the question
def get_response_3(df):
    """Create new column to capture absolute response=3 as 1=yes, 0=no"""
    if df['score'] == 3:
        return 1
    else:
        return 0


df['response_3'] = df.apply(lambda x: get_response_3(x), axis = 1)


# boolean if user clicked on option 4 in the question
def get_response_4(df):
    """Create new column to capture absolute response=4 as 1=yes, 0=no"""
    if df['score'] == 4:
        return 1
    else:
        return 0


df['response_4'] = df.apply(lambda x: get_response_4(x), axis = 1)


# boolean if user clicked on option 5 in the question
def get_response_5(df):
    """Create new column to capture absolute response=5 as 1=yes, 0=no"""
    if df['score'] == 5:
        return 1
    else:
        return 0


df['response_5'] = df.apply(lambda x: get_response_5(x), axis = 1)


# boolean if user clicked on option 6 in the question
def get_response_6(df):
    """Create new column to capture absolute response=6 as 1=yes, 0=no"""
    if df['score'] == 6:
        return 1
    else:
        return 0


df['response_6'] = df.apply(lambda x: get_response_6(x), axis = 1)


# boolean if user clicked on option 7 in the question
def get_response_7(df):
    """Create new column to capture absolute response=7 as 1=yes, 0=no"""
    if df['score'] == 7:
        return 1
    else:
        return 0


df['response_7'] = df.apply(lambda x: get_response_7(x), axis = 1)


def split_by_page(df):
    ###############################################################
    # for bf_questions
    if "bf_" in df['value']:

        # validation questions first
        if df['value'] == 'bf_validation_1':
            return "Page_2"
        if df['value'] == 'bf_validation_2':
            return "Page_4"

        # rest of questions
        # page 1
        pattern = ['_1', '_2', '_3', '_4', '_5', '_6', '_7', '_8']
        if df['value'].endswith(tuple(pattern)):
            return "Page_1"

        # page 2
        pattern2 = ['_9', '_10', '_11', '_12', '_13', '_14', '_15', '_16', '_17']
        if df['value'].endswith(tuple(pattern2)):
            return "Page_2"

        # page 3
        pattern3 = ['_18', '_19', '_20', '_21', '_22', '_23', '_24', '_25', '_26', '_27']
        if df['value'].endswith(tuple(pattern3)):
            return "Page_3"

        # page 4
        pattern4 = ['_28', '_29', '_30', '_31', '_32', '_33', '_34', '_35', '_36']
        if df['value'].endswith(tuple(pattern4)):
            return "Page_4"

        # page 5
        pattern5 = ['_37', '_38', '_39', '_40']
        if df['value'].endswith(tuple(pattern5)):
            return "Page_5"

    ###############################################################
    # for bs questions
    if "bs_" in df['value']:

        pattern_bs_1 = ['_1', '_2', '_3', '_4']
        if df['value'].endswith(tuple(pattern_bs_1)):
            return "Page_6"

    ###############################################################
    # for miq questions
    if "miq_" in df['value']:

        # validation questions first
        if df['value'] == 'miq_validation_3':
            return "Page_9"
        if df['value'] == 'miq_validation_4':
            return "Page_11"

        # rest of questions

        # page 7
        pattern_mq_1 = ['_1.1', '_1.2', '_1.3', '_1.4', '_1.5', '_1.6', '_1.7', '_1.8']
        if df['value'].endswith(tuple(pattern_mq_1)):
            return "Page_7"

        # page 8
        pattern_mq_2 = ['_2.1', '_2.2', '_2.3', '_2.4', '_2.5', '_2.6', '_2.7', '_2.8', '_3.1', '_3.2']
        if df['value'].endswith(tuple(pattern_mq_2)):
            return "Page_8"

        # page 9
        pattern_mq_3 = ['_3.3', '_3.4', '_3.5', '_3.6', '_3.7', '_3.8', '_4.1', '_4.2', '_4.3']
        if df['value'].endswith(tuple(pattern_mq_3)):
            return "Page_9"

        # page 10
        pattern_mq_4 = ['_4.4', '_4.5', '_4.6', '_4.7', '_4.8', '_5.1', '_5.2', '_5.3', '_5.4', '_5.5']
        if df['value'].endswith(tuple(pattern_mq_4)):
            return 'Page_10'

        # page 11
        pattern_mq_5 = ['_5.6', '_5.7', '_5.8', '_6.1', '_6.2', '_6.3', '_6.4', '_6.5', '_6.6']
        if df['value'].endswith(tuple(pattern_mq_5)):
            return "Page_11"

        # page 12
        pattern_mq_6 = ['_6.7', '_6.8', '_7.1', '_7.2', '_7.3', '_7.4', '_7.5', '_7.6', '_7.7', '_7.8']
        if df['value'].endswith(tuple(pattern_mq_6)):
            return "Page_12"

        # page 13
        pattern_mq_7 = ['_8.1', '_8.2', '_8.3', '_8.4', '_8.5', '_8.6', '_8.7', '_8.8']
        if df['value'].endswith(tuple(pattern_mq_7)):
            return "Page_13"

    ###############################################################
    # for pgi Liking questions
    if "_Liking" in df['value']:

        if df['value'] == 'pgi_validation_5_Liking':
            return "Page_15"
        if df['value'] == 'pgi_validation_6_Liking':
            return "Page_17"

        # rest of questions
        # page 14
        pattern_lik_1 = ['_1_', '_2_', '_3_', '_4_', '_5_', '_6_', '_7_', '_8_']
        for i in pattern_lik_1:
            if i in df['value']:
                return "Page_14"

        # page 15
        pattern_lik_2 = ['_9_', '_10_', '_11_', '_12_', '_13_', '_14_', '_15_', '_16_', '_17_']
        for i in pattern_lik_2:
            if i in df['value']:
                return "Page_15"

        # page 16
        pattern_lik_3 = ['_18_', '_19_', '_20_', '_21_', '_22_', '_23_', '_24_', '_25_', '_26_', '_27_']
        for i in pattern_lik_3:
            if i in df['value']:
                return "Page_16"

        # page 17
        pattern_lik_4 = ['_28_', '_29_', '_30_', '_31_', '_32', '_33_', '_34_', '_35_', '_36_']
        for i in pattern_lik_4:
            if i in df['value']:
                return "Page_17"

        # page 18
        pattern_lik_5 = ['_37_', '_38_', '_39_', '_40_']
        for i in pattern_lik_5:
            if i in df['value']:
                return "Page_18"

    ###############################################################
    # for pgi Competence questions
    if "_Competence" in df['value']:

        # validation questions first
        if df['value'] == 'pgi_validation_5_Competence':
            return "Page_15"
        if df['value'] == 'pgi_validation_6_Competence':
            return "Page_17"

        # rest of questions
        # page 14
        pattern_comp_1 = ['_1_', '_2_', '_3_', '_4_', '_5_', '_6_', '_7_', '_8_']
        for i in pattern_comp_1:
            if i in df['value']:
                return "Page_14"

        # page 15
        pattern_comp_2 = ['_9_', '_10_', '_11_', '_12_', '_13_', '_14_', '_15_', '_16_', '_17_']
        for i in pattern_comp_2:
            if i in df['value']:
                return "Page_15"

        # page 16
        pattern_comp_3 = ['_18_', '_19_', '_20_', '_21_', '_22_', '_23_', '_24_', '_25_', '_26_', '_27_']
        for i in pattern_comp_3:
            if i in df['value']:
                return "Page_16"

        # page 17
        pattern_comp_4 = ['_28_', '_29_', '_30_', '_31_', '_32', '_33_', '_34_', '_35_', '_36_']
        for i in pattern_comp_4:
            if i in df['value']:
                return "Page_17"

        # page 18
        pattern_comp_5 = ['_37_', '_38_', '_39_', '_40_']
        for i in pattern_comp_5:
            if i in df['value']:
                return "Page_18"


df['page_number'] = df.apply(lambda x: split_by_page(x), axis = 1)

# Save new votes dataset that includes: Page Number - Page Question Count - and more...
df.to_csv("votes_V3.csv")

# calculate nr of questions per page
df['page_quest_count'] = df.groupby(['page_number', 'user_id'])['page_number'].transform('count')

df_pivot = pd.pivot_table(df, index = ['page_number', 'user_id', 'page_quest_count'],
                          values = ['response_1', 'response_2', 'response_3', 'response_4',
                                    'response_5', 'response_6', 'response_7'],
                          aggfunc = [np.sum])

# turn pivot to dataframe
df_pivot.columns = df_pivot.columns.droplevel(0)
votes_pages = df_pivot.reset_index().rename_axis(None, axis = 1)

# change column names
votes_pages.columns = ['page_number', 'user_id', 'quest_count', 'count_resp_1', 'count_resp_2',
                       'count_resp_3', 'count_resp_4', 'count_resp_5', 'count_resp_6', 'count_resp_7']

# create v2 with subcolumns
v2 = votes_pages[['quest_count', 'count_resp_1', 'count_resp_2',
                  'count_resp_3', 'count_resp_4', 'count_resp_5', 'count_resp_6', 'count_resp_7']]
col = "quest_count"
other_cols = [c for c in v2 if c != col]

# get boolean if quest_count==any of responses
vv = pd.concat([v2[[col]],
                v2[other_cols].apply(lambda series: v2[col].eq(series))], axis = 1)

# create new column that captures if any of count_resp is True
col = "quest_count"
other_cols = [c for c in vv if c != col]
vv["same_answer_across"] = (vv[other_cols] == True).any(axis = "columns")

# concat with page_number and user_id columns
final_df = pd.concat([votes_pages, vv['same_answer_across']], axis = 1)

final_df.to_csv("Data/Extra/outliers.csv")
