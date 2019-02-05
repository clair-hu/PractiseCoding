# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 13:05:24 2019

@author: clair
"""

######### part one -- import library for preprocessing part ###################
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

############ part seven -- split X and Y and Train and Test ###########
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.2, reandom_state = 304)

########### part eight -- feature standarization -- only to training set ######################
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)

############### part nine -- import library for training model part ###############################
import keras
from keras.model import Sequential
from keras.layers import Dense
from keras import regularizers, optimizers
from datetime import datetime

# keep track of starting time
start = datetime.now()

###################### part ten -- set up model ###########################
classifier = Sequential()

"""
kernel_initializer: difference between 'uniform' and others
activation: difference between 'relu' and 'linear'
"""
classifier.add( Dense( units=128, kernel_initializer = 'uniform', activation = 'relu', input_dim = X_train.shape[1])) # first layer need to assign 'input_dim'
classifier.add( Dense( units=128, kernel_initializer = 'uniform', activation = 'relu'))
classifier.add( Dense( units=128, kernel_initializer = 'uniform', activation = 'relu'))
classifier.add( Dense( units=64, kernel_initializer = 'uniform', activation = 'relu'))
classifier.add( Dense( units=64, kernel_initializer = 'uniform', activation = 'relu'))
classifier.add( Dense( units=64, kernel_initializer = 'uniform', activation = 'relu'))
classifier.add( Dense( units=32, kernel_initializer = 'uniform', activation = 'relu'))
classifier.add( Dense( units=32, kernel_initializer = 'uniform', activation = 'relu'))
classifier.add( Dense( units=32, kernel_initializer = 'uniform', activation = 'relu'))
classifier.add( Dense( units=1, kernel_initializer = 'uniform', activation = 'linear'))

################### part eleven -- define optimizer ###############################
RMSprop = optimizers.RMSprop(lr=0.001) # can tune learning rate here

################## part twelve -- compile model #################################
classifier.compile(optimizer = RMSprop, loss = 'mean_squared_error', metrics = ['accuracy']) # can add more metrics, can change loss based on purpose

################# part thirteen -- set up early stoppping and prepare for history recording ##################################
from keras.callbacks import EarlyStopping, TensorBoard
early_stopping = EarlyStopping(monitor='val_loss', patience = 100)
tensorBoard = TensorBoard(log_dir={path to store log file}, histogram_freq=0, batch_size=128)
'''
Do we need to keep the batch_size of tensorBoard and the training classifier part SAME?
'''

#################### part fourteen -- fitting the model to training data set ################################################
hist = classifier.fit(X_train, y_train, batch_size=512, epochs=5000, validation_split=0.05)

# keep track of ending time
end = datetime.now()

################## part fifteen -- evaluation ###########################################
y_pred = classifier.predict(X_test)
y_pred_df = pd.DataFrame(y_pred)

################## part sixteen -- editing history file ############################
text_file = open({path of txt file you want to store}, 'w')
text_file.write("Processing time is " + str(end-start) + "\n")
text_file.write(str(hist.history))
text_file.close()

################## part seventeen -- store weight/output to a .h5 file ####################
classifier.save({path to store model output .h5 file})









