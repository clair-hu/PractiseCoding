# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 12:33:32 2019

@author: clair
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_train = pd.read_csv('data/train.csv')
data_train.Cabin = data_train.Cabin.fillna('N')
def simplify_ages(df):
    df.Age = df.Age.fillna(-0.5)
    bins = (-1,0,5,12,18,25,35,60,120)
    group_names = ['Unknown', 'Baby', 'Child', 'Teenager', 'Student', 'Young Adult', 'Adult', 'Senior']
    df.Age = pd.cut(df.Age, bins, labels=group_names)

def simplify_cabins(df):
    df.Cabin = df.Cabin.fillna('N')
    df.Cabin = df.Cabin.apply(lambda x: x[0])
    return df

def simplify_fares(df):
    df.Fare = df.Fare.fillna(-0.5)
    bins = (-1, 0, 8, 15, 31, 1000)
    group_names = ['Unknown', '1_quartile', '2_quartile', '3_quartile', '4_quartile']
    categories = pd.cut(df.Fare, bins, labels=group_names)
    df.Fare = categories
    return df

def format_name(df):
    df['Lname'] = df.Name.apply(lambda x: x.split(' ')[0])
    df['NamePrefix'] = df.Name.apply(lambda x: x.split(' ')[1])
    return df    
    
def drop_features(df):
    return df.drop(['Ticket', 'Name', 'Embarked'], axis=1)

def transform_features(df):
    df = simplify_ages(df)
#    df = simplify_cabins(df)
    df = simplify_fares(df)
    df = format_name(df)
    df = drop_features(df)
    return df

data_train = transform_features(data_train)
#data_test = transform_features(data_test)
data_train.head()


#drop_cols = []
#drop_cols.append(dataset.columns.get_loc('PassengerId'))
#drop_cols.append(dataset.columns.get_loc('Name'))
#drop_cols.append(dataset.columns.get_loc('Ticket'))
#
#dataset1 = dataset.drop(dataset.columns[drop_cols],axis = 1)
#
#for i,v in enumerate(dataset1.columns):
#    if type(dataset1[v][1]) == str:
#        dataset1 = pd.get_dummies(dataset1, columns=[v])
#        
#
##missing value
##from sklearn.preprocessing import Imputer
##imputer = Imputer(missing_values='NaN',strategy='mean', axis = 0)
##imputer = imputer.fit(dataset['Age'])
##dataset['Age'] = imputer.transform(dataset['Age'])
#
#i = dataset1.columns.get_loc('Survived')
#y = dataset1.iloc[:,i].values
#dataset1 = dataset1.drop('Survived',axis = 1)
#X = dataset1.iloc[:,:].values
#
##missing value
#from sklearn.preprocessing import Imputer
#imputer = Imputer(missing_values='nan',strategy='mean', axis = 0)
#imputer = imputer.fit(X[:,1])
#X[:,1] = imputer.transform(X[:,1])