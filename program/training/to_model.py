file =  open('../csv/miammiamsvmImage.csv', 'r')
    
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC


from skimage import exposure
from skimage import feature

import numpy as np

import joblib
import cv2
import csv
import os

import pandas as pd
import matplotlib.pyplot as plt  
from sklearn import metrics
from sklearn.decomposition import PCA
from sklearn.utils import shuffle




def verify_name():

    name = str("_in_training")
    path = "models"

    c = 0

    liste = os.listdir(path)
    no_save = True;
    while no_save:

        same = False
        for url in liste:

            if url == name:
                name = str(name) + str(c)
                same = True
                c+=1

            if same is False:
                no_save = False

    print(name)
    return name



def csv_to_data(name):

    file =  open("csv/" + name, 'r')

    dataframe = file.readlines()
    dataframe = dataframe[1:]

    data = []
    label = []
    increment = ""


    for i in dataframe:
        liste_w = []
        for j in i:
            if j == "\n":
                data.append(liste_w)
                liste_w = []
            else:
                if j == " ":
                    pass
                elif j == ";":
                    liste_w.append(float(increment))
                    increment = ""
                else:
                    increment += str(j)


    for i in data:
        label.append(int(i[0]))
        del i[0]


    return data, label



def training(data, label, name):

    model = LinearSVC()
    model.fit(data, label)
    joblib.dump(model, "models/" + str(name)) 

    predictions = model.predict(data)

    print("Score", metrics.accuracy_score(label, predictions))

