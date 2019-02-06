# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:47:39 2019

@author: clair
"""
# import libraries for processing
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# import data
dataset = pd.read_csv("Logistic_Regression/Social_Network_Ads.csv")
X = dataset.iloc[:, [2,3]].values
y= dataset.iloc[:,-1].values

# split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 32)

# feature scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# fiting logistic regression to trainig set
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state = 404)
classifier.fit(X_train, y_train)

# predict the testset results
y_pred = classifier.predict(X_test)

# show the confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

## visualizing training set results
#from matplotlib.colors import ListedColormap
#X_set, y_set = X_train, y_train
#X1, X2 = np.meshgrid()
#

