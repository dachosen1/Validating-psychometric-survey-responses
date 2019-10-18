import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from math import sqrt, nan,isnan
import re

#Pre-proccesing, loading the data
path = './Data/Clean Data/mouse_flat_V3.csv'
path_dup = './Data/Raw/mouse_paths.csv'
data = pd.read_csv(path,index_col=0)
data.replace(np.nan, 'NoValue', regex=True,inplace=True)
len(data)

#Duplicate ids
for_dup = pd.read_csv(path_dup)
dup_ids = list(for_dup.user_id.value_counts()[for_dup.user_id.value_counts()>1].index)

inn = [np.where(data.user_id == dup_ids[i]) for i in range(len(dup_ids))]
inn_2 = [list(item) for sublist in inn for item in sublist]
inn_3 = [item for sublist in inn_2 for item in sublist]
data.iloc[inn_3,:].user_id.unique()

data.drop(inn_3,inplace=True)
data.user_id.unique()
data.reset_index(drop=True,inplace=True)


#Distance of Clicks not 0, same as previous movement
l = np.array(np.where(((data.action == "c") | (data.action == "np")) & (data.radio != "NoValue"))).tolist()
i_list = [item for sublist in l for item in sublist]
index_list = [ind-1 for ind in i_list]

radio_DF = data.iloc[i_list,].reset_index()

#Create Aspect Ratio column
radio_DF['aspect_ratio'] = [str(radio_DF['window_x'][i])+"x"+str(radio_DF['window_y'][i]) for i in range(len(radio_DF))]

def distance(df):
    pl=[]
    clients = df['user_id'].unique()
    for i in range(len(clients)):
        x = df[df.user_id == clients[i]]
        per_id = x.id.unique()
        for j in range(len(per_id)):
            y = x[x.id == per_id[j]]
            pl.append(0)
            m=1
            while m < len(y):
                dist = round(sqrt((y.cord_x.iloc[m]-y.cord_x.iloc[m-1])**2 + (y.cord_y.iloc[m]-y.cord_y.iloc[m-1])**2),0)#distance formula between two points.
                pl.append(dist)
                m += 1
    return pl

radio_DF.distance = distance(radio_DF)

def scale_distance(df):
    sx = []
    first = []
    aspect_r = df['aspect_ratio'].unique()
    for i in range(len(aspect_r)):
        x = df[df.aspect_ratio == aspect_r[i]]
        ind = df[df.aspect_ratio == aspect_r[i]].index
        as_dis = np.round(np.interp(x.distance, (x.distance.min(), x.distance.max()), (0, 100)),0)
        sx.append(as_dis)
        first.append(ind)
    ll = [sx,first]
    pp = pd.DataFrame({"scaled_distance":[item for sublist in ll[0] for item in sublist]},
             index=[item for sublist in ll[1] for item in sublist])
    return pp

scaled_cords = scale_distance(radio_DF)
rr_df = radio_DF.join(scaled_cords)

#Scaling Distance and Coordinates

# Radio click is in list name it page change, 0 Means Start Page and If Cord Y is Above 300
rr_df.insert(loc=rr_df.columns.get_loc('distance')+1,column='direction',value=["Nada" for val in rr_df.distance])
page_change_list = ['_bf_9_score_','_bf_18_score_','_bf_28_score_','_bf_37_score_',
'_miq_2.1_score_','_miq_3.3_score_','_miq_4.4_score_','_miq_5.6_score_','_miq_6.7_score_',
'_miq_8.1_score_','_pgi_1_Liking_score_','_pgi_9_Liking_score_','_pgi_18_Liking_score_',
'_pgi_validation_6_Liking_score_','_pgi_37_Liking_score_']

pat = re.compile("(_\w+_?[\w+]?_[\d\.]+_?[\w+]*_score_)\d*")
question_change = rr_df.radio.apply(lambda x: True if re.findall(pat, x)[0] in page_change_list else False)

for i in range(len(rr_df)):
    if question_change[i] == True and list(rr_df.index) !=0 and (abs(rr_df.cord_y[i]-rr_df.cord_y[i-1])>50):
        rr_df.loc[i,'direction'] = 'PageChange'

x=[]
non_complete=[]
weirdinstance = []
tofix = []
for id in np.array(rr_df.user_id.unique()).tolist():
    print(id)
    one_user = rr_df[rr_df.user_id == id]
    if len(one_user) >= 187:
        vc = pd.DataFrame(one_user.direction.value_counts())
        try:
            if vc.direction[1] >= 15:
                #print(id)
                x.append(id)
        except IndexError:
            weirdinstance.append(id)
    else:
        non_complete.append(id)


#one_user = rr_df[rr_df.user_id == 1528].reset_index(drop=True)
ii = [np.where(rr_df.user_id == x[i]) for i in range(len(x))]
ii_2 = [list(item) for sublist in ii for item in sublist]
ii_3 = [item for sublist in ii_2 for item in sublist]

good_user = rr_df.iloc[ii_3,:].reset_index(drop=True)

def add_direction(dd):
    for i in range(len(dd)):
        if dd.direction[i] != "PageChange" and dd.distance[i] != 0:
            xx = dd.cord_x[i] - dd.cord_x[i-1]
            yy = dd.cord_y[i] - dd.cord_y[i-1]
            if xx>0 and yy>0:
                dd.loc[i,'direction'] = 'SE' +" "+str(dd.scaled_distance[i]) + " ,"
            elif xx<0 and yy>0:
                dd.loc[i,'direction'] = 'SW' +" "+str(dd.scaled_distance[i]) + " ,"
            elif xx<0 and yy<0:
                dd.loc[i,'direction'] = 'NW' +" "+str(dd.scaled_distance[i]) + " ,"
            elif xx>0 and yy<0:
                dd.loc[i,'direction'] = 'NE' +" "+str(dd.scaled_distance[i]) + " ,"
            elif xx== 0 and yy>0:
                dd.loc[i,'direction'] = 'SS'+" "+str(dd.scaled_distance[i]) + " ,"
            elif xx == 0 and yy < 0:
                dd.loc[i,'direction'] = 'NN'+" "+str(dd.scaled_distance[i]) + " ,"
            elif xx > 0 and yy == 0:
                dd.loc[i,'direction'] = 'EE'+" "+str(dd.scaled_distance[i]) + " ,"
            elif xx < 0 and yy == 0:
                dd.loc[i,'direction'] = 'WW'+" "+str(dd.scaled_distance[i]) + " ,"
    return dd

final_df = add_direction(rr_df)

ff = final_df.user_id.unique().tolist()
ff.sort()
print(ff)
len(ff)
non_complete.sort()
print(non_complete)

direction_df = pd.DataFrame(columns=['user_id','direction_list'])
list_of_ids = np.array(final_df.user_id.unique()).tolist()
for id in range(len(list_of_ids)):
    list_of_direction = final_df[final_df.user_id == list_of_ids[id]].direction.reset_index(drop=True)
    del list_of_direction[0]
    direction_df.loc[id, 'user_id'] = list_of_ids[id]
    direction_df.loc[id,'direction_list'] = [' '.join(list_of_direction)]

direction_df.to_csv('./Data/Extra/id_direction_list.csv')





