import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from math import sqrt

#Pre-proccesing, loading the data
path = './Data/Clean Data/mouse_flat_v2.csv'

data = pd.read_csv(path)

#EDA Process of index per ratio (window x and window y)

def index_per_ratio(data,ratio_x,ratio_y):
    l=[]
    clients = data['user_id'].unique()
    c=0
    for i in range(len(clients)):
        x = data[data.user_id == clients[i]]
        per_id = x.id.unique()
        for j in range(len(per_id)):
            donde = np.where( (x.action == "c") & (x.id == per_id[j]) &
                             (x.window_x == ratio_x) & (x.window_y == ratio_y))
            print([clients[i],per_id[j],ratio_x,ratio_y])
            try:
                h = donde[0][-1]
                l.append(x.Index.iloc[h])
            except IndexError or KeyError:
                pass
    return l

data.iloc[3244067,]

#List of all Unique combinations of window x,window y
ins = data[['window_x',"window_y"]].drop_duplicates().sort_values(by="window_x")

#Key creation of each combination of window_x and window_y
str_windows = [str(ins.window_x.iloc[i])+"x"+str(ins.window_y.iloc[i]) for i in range(len(ins))]

#creating the dictionary where the index of the last click per each aspect ratio combination is stored.
myDict = dict.fromkeys(str_windows)
for k in range(len(ins)):
    myDict[str_windows[k]]= index_per_ratio(data,ins.window_x.iloc[k],ins.window_y.iloc[k])

data.loc[myDict['1440'],['user_id','id','radio','cord_x','cord_y']]#tests


#Converting Numpy Int to Int
od = myDict
m=0
for m in range(len(str_windows)):
    od[str_windows[m]]= list(map(int, od[str_windows[m]]))

#Saving for later Use
with open('last_c.json','w') as fp:
    json.dump(od, fp,indent=4)


#Creating a box to estimate where the next page button is located based on the last click per ratio and an expansion
# of the error rate by 5%

max_min_df = pd.DataFrame(index=od.keys(),columns=['count','max_x','max_y',"min_x","min_y",'range_x','range_y','window_x','window_y'])
for w in od:
    max_min_df.loc[w, 'count'] = len(od[w])
    #Min Max *1.05
    ux = data.loc[od[w], 'cord_x'].describe()['max']
    uy = data.loc[od[w], 'cord_y'].describe()['max']
    mx = data.loc[od[w], 'cord_x'].describe()['min']
    my = data.loc[od[w], 'cord_y'].describe()['min']
    max_min_df.loc[w, 'max_x'] = ux *1.05
    max_min_df.loc[w, 'max_y'] = uy *1.05
    max_min_df.loc[w, 'min_x'] = mx *.95
    max_min_df.loc[w, 'min_y'] = my *.95

    #Range
    tx = data.loc[od[w],'cord_x'].describe()['max']-data.loc[od[w],'cord_x'].describe()['min']
    ty = data.loc[od[w],'cord_y'].describe()['max']-data.loc[od[w],'cord_y'].describe()['min']
    max_min_df.loc[w,'range_x'] = tx
    max_min_df.loc[w, 'range_y'] = ty

    #Window
    max_min_df.loc[w, 'window_x'] = data.loc[od[w],'window_x'].describe()['mean']
    max_min_df.loc[w, 'window_y'] = data.loc[od[w],'window_y'].describe()['mean']

df = data

df.action = np.where((data.window_x == 1600) & (data.window_y == 860) &
         (data.cord_x <= max_min_df.loc["1600x860","max_x"]) &
         (data.cord_x >= max_min_df.loc["1600x860","min_x"]) &
         (data.cord_y <= max_min_df.loc["1600x860","max_y"]) &
         (data.cord_y >= max_min_df.loc["1600x860","min_y"]) &
         (data.action == "c"),
          "np",df.action)

to_ins = df[df.action != "m"][df.user_id == 365]

jj = []
for r in range(len(max_min_df)):
    if max_min_df.cord_x[r] <150 and max_min_df.cord_y[r] <150:
        jj.append(list(max_min_df.index)[r])

#Creating the Distance Variable
def distance(data):
    pl=[]
    clients = data['user_id'].unique()
    for i in range(len(clients)):
        x = data[data.user_id == clients[i]]
        per_id = x.id.unique()
        for j in range(len(per_id)):
            y = x[x.id == per_id[j]]
            pl.append(0)
            m=1
            while m < len(y):
                dist = sqrt((y.cord_x.iloc[m]-y.cord_x.iloc[m-1])**2 + (y.cord_y.iloc[m]-y.cord_y.iloc[m-1])**2) #distance formula between two points.
                pl.append(dist)
                m += 1
    return pl


dist = distance(data)
data.insert(loc=data.columns.get_loc('cord_y')+1,column='distance',value=dist)


#Detect Mobile Devices using a csv of scrapped ratio aspects of known mobile devices

path2 = './Data/Extra/Mobile Aspect Ratio.csv'
mobile_detect = pd.read_csv(path2)

data['system'] = ""
for sys in range(len(mobile_detect)):
    data.system = np.where((data.window_x == mobile_detect.window_x[sys]) & (data.window_y == mobile_detect.window_y[sys]),
             mobile_detect.OS[sys],data.system)
data.system = np.where(data.system == "",
         "pc", data.system)

data['system'].value_counts(dropna=False)

#Create a csv of all ids and their respective system
subset =data[['user_id','id','system']].drop_duplicates().reset_index(drop=True)
subset.to_csv(r"./Data/Extra/uid_system.csv",index=False)
