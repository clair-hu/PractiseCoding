# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 06:34:13 2019

@author: clair
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#%matplotlib inline
#
#from subprocess import check_output
#print(check_output(["ls","../Data"]).decode("utf8"))

train = pd.read_csv("../Data/train.csv")
print(train.shape)
train.head()

test = pd.read_csv("../Data/test.csv")
print(test.shape)
test.head()

X_train = (train.iloc[:,1:].values).astype('float32')
y_train = train.iloc[:,0].values.astype('int32')
X_test = test.values.astype('float32')


############ Data visualization ####################

# Feature standarization #
from sklearn import preprocessing
X_train = preprocessing.scale(X_train)
#mean_px = X_train.mean().astype(np.float32)
#std_px = X_train.std().astype(np.float32)
#def standardize(x):
#    return (x-mean_px)/std_px

#convert to 28*28 matrix
X_train = X_train.reshape(X_train.shape[0], 28,28)
for i in range(0,5):
    plt.subplot(190+(i+1))
    plt.imshow(X_train[i], cmap=plt.get_cmap('gray'))
    plt.title(y_train[i])
    
#add one dimension for color channel gray
X_train = X_train.reshape(X_train.shape[0], 28, 28, 1)
X_train.shape

X_test = X_test.reshape(X_test.shape[0], 28, 28, 1)
X_test.shape


# One hot encoding #
# Can only be executed once
from keras.utils.np_utils import to_categorical
y_train = to_categorical(y_train)
num_classes = y_train.shape[1]

plt.title(y_train[7])
plt.plot(y_train[7])
plt.xticks(range(10))

np.random.seed(1241)

############## Linear model ########################
from keras.models import Sequential
from keras.layers.core import Lambda, Dense, Flatten, Dropout
from keras.callbacks import EarlyStopping
from keras.layers import BatchNormalization, Convolution2D, MaxPooling2D

model = Sequential()
model.add(Lambda(standardize, input_shape=(28,28,1)))
model.add(Flatten())
model.add(Dense(10, activation="softmax"))
print("input shape is ", model.input_shape)
print("output shape is ", model.output_shape)

# Compile model #
from keras.optimizers import RMSprop
model.compile(optimizer=RMSprop(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

from keras.preprocessing import image
gen = image.ImageDataGenerator()

# Apply model to training dataset #
from sklearn.model_selection import train_test_split
X = X_train
y = y_train
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size = 0.2, random_state=3487)
batches = gen.flow(X_train, y_train, batch_size=128)
val_batches = gen.flow(X_val, y_val, batch_size=128)

history = model.fit_generator(generator=batches, steps_per_epoch=batches.n, epochs=100, 
                              validation_data=val_batches, validation_steps=val_batches.n)
#history = model.fit_generator(generator=batches, steps_per_epoch=batches.n, epochs=3, 
#                              validation_data=val_batches, validation_steps=val_batches.n)



###################### Linear model finished val_acc 85.78% TOOOOOOOO LOW ###########################



# TODO train CNN








