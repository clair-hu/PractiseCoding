# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 14:01:21 2019

@author: clair
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data_train = pd.read_csv('data/train.csv')

#t = pd.read_csv('data/test.csv')
#cols = t.columns
#data_train = np.vstack((data_train, t))
#data_train = pd.DataFrame(data_train, columns = cols)

data_train.info()
data_train.describe()

sns.barplot(x= "Embarked", y="Survived", hue = "Sex", data=data_train)

sns.pointplot(x="Pclass", y= "Survived", hue = "Sex", data = data_train)

# missing values
data_train.Age = data_train.Age.fillna(-1)
data_train.Cabin = data_train.Cabin.fillna('N')
data_train.Cabin = [i[0] for i in data_train.Cabin]

data_train['Title'] = [i.split(',')[1].split()[0] for i in data_train.Name]

drop_cols = []
drop_cols.append(data_train.columns.get_loc('Name'))
drop_cols.append(data_train.columns.get_loc('Ticket'))

data_train = data_train.drop(data_train.columns[drop_cols],axis = 1)

data_train.info()

for v in data_train.columns:
    if type(data_train[v][0]) == str:
        data_train = pd.get_dummies(data_train, columns=[v])

y = data_train['Survived']
X = data_train.drop('Survived', axis = 1)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.9, random_state = 606)

from sklearn.linear_model import LogisticRegression
logisticRegrassion = LogisticRegression()
logisticRegrassion.fit(X_train,y_train)
Y_pred = logisticRegrassion.predict(X_test)
acc_log = round(logisticRegrassion.score(X_train,y_train)*100,2)


from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

import keras
from keras.models import Sequential
from keras.layers import Dense
from keras import regularizers, optimizers

classifier = Sequential()
classifier.add(Dense(units = 128, kernel_initializer="uniform", activation="relu", input_dim = X_train.shape[1]))
classifier.add(Dense(units = 64, kernel_initializer="uniform", activation="relu"))
classifier.add(Dense(units = 32, kernel_initializer="uniform", activation="relu"))
classifier.add(Dense(units = 1, kernel_initializer = 'uniform', activation = 'sigmoid'))
RMSprop = optimizers.RMSprop()

from datetime import datetime
start = datetime.now()
classifier.compile(optimizer=RMSprop, loss='mean_squared_error', metrics = ['accuracy'])

from keras.callbacks import EarlyStopping, TensorBoard
early_stopping = EarlyStopping(monitor='val_loss', patience=100)
tensorBoard = TensorBoard(log_dir='../logs', histogram_freq=0, batch_size=64)

hist = classifier.fit(X_train, y_train, batch_size = 64, epochs = 100, validation_split=0.2)
end = datetime.now()

score = classifier.evaluate(X_test, y_test, batch_size=64)


y_pred = classifier.predict(X_test)
y_pred = [1 if i > 0.5 else 0 for i in y_pred]
