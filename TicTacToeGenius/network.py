
# 3. Import libraries and modules
import numpy as np
from collections import deque

np.random.seed(123)  # for reproducibility

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils

class Network():

    #sizes is list of integers stating the size of each neuron layer
    def __init__(self):
        self.memory = deque(maxlen=2000)
        self.batchSize = 32
        self.model = self.makeModel()

    def makeModel(self):
        model = Sequential()
        model.add(Dense(64, activation='relu'), input_shape=(18,))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(9, activation='softmax'))

        model.compile(loss='categorical_crossentropy',
                      optimizer=keras.optimizers.Adam())

        return model

    def remember(self, state, action, reward, nextState, isEnd):
        self.memory.append((state, action, reward, nextState, isEnd))








