# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 13:05:24 2019

@author: clair
"""

######### part one -- import ###################
import numpy as np
import pandas as pd
import tensorflow as tf

######### part two -- read data file #################
dataset = pd.read_csv({file_path})
#if concatenate multiple files, need to convert from np arrays to pd.DataFrames
dataset = pd.DataFrame(dataset, columns = colu) # colu stores the original dataset column names

########## part three - drop columns with same value for all rows
drop_cols = []

isUnique = dataset.apply(lambda x:x.nunique())
for i,v in enumerate(dataset.columns):
    if isUnique[i] == 1:
        drop_cols.append(i)

# manually drop some range of columns
i1 = dataset.columns.get_loc("track_id")
i2 = dataset.columns.get_loc("numberofstarts")
drop_cols += [i for i in range(0,i1)] + [i for i in range(i2,0)]
dataset = dataset.drop(dataset.columns[drop_cols], axis = 1, inplace = False)

# manually drop certain column
dataset = dataset.drop('race_date',1)

########## part four --  deal with missing data IMPORTANT! ###################
dataset.dropna(inplace=True)

########## part five -- convert type
dataset['ownernumber'] = dataset['ownernumber'].astype(int)
dataset['win_payoff'] = dataset['win_payoff'].astype(float)

############ part six -- encoding categorical data / dummy vairables ########
for i,v in enumerate(dataset.columns):
    if type(dataset[v][0]) == str:
        dataset = pd.get_dummies(dataset, columns=[v])


######## part seven or eight ???? -- split X and Y and Train and Test ###########
    


########## part seven -- feature standarization ######################
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X = sc.fit_transform(X)
