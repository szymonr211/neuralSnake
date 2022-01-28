import pygame, sys, random


class Manual_controller:
    def __init__(self):
        self.output = -1

    def get_output(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.output = 0
                if event.key == pygame.K_DOWN:
                    self.output = 1
                if event.key == pygame.K_LEFT:
                    self.output = 2
                if event.key == pygame.K_RIGHT:
                    self.output = 3

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        return self.output

    def reset(self):
        self.output = -1

class Random_controller:
    def __init__(self):
        self.output = -1

    def get_output(self):
        self.output = random.randint(0,3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        return self.output

    def reset(self):
        self.output = -1


import keras
from keras import backend as K
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class Neural_controller:
    def __init__(self):
        self.output = -1
        self.prediction = [1,0,0,0]
        self.rst = False

    def my_model(self):
        model = keras.models.Sequential()
        model.add(keras.layers.Dense(6,activation='relu',input_shape=(6,)))
        model.add(keras.layers.Dense(8, activation='relu'))
        model.add(keras.layers.Dense(4, activation='sigmoid'))
        return model

    def set_weights(self,weights):
        K.clear_session()
        self.model = self.my_model()
        self.model.set_weights(weights)

    def predict(self,input):
        input = np.asarray(input).astype('float32')/100
        prediction = self.model.predict([[input]])
        self.prediction = list(prediction[0])

    def get_output(self):
        if not self.rst:
            if self.prediction.index(max(self.prediction)) == 0:
                self.output = 0
            if self.prediction.index(max(self.prediction)) == 1:
                self.output = 1
            if self.prediction.index(max(self.prediction)) == 2:
                self.output = 2
            if self.prediction.index(max(self.prediction)) == 3:
                self.output = 3
        self.rst = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        return self.output

    def reset(self):
        self.output = -1
        self.rst = True
