from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier

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



liste = os.listdir(r"C:\Users\jeanbaptiste\Desktop\assiette\image\assiette")
path  = r"C:\Users\jeanbaptiste\Desktop\assiette\image\assiette\{}"


liste1 = os.listdir(r"C:\Users\jeanbaptiste\Desktop\assiette\image\N")
path1  = r"C:\Users\jeanbaptiste\Desktop\assiette\image\N\{}"


def csv_write():
    with open('csv/miammiamCSV.csv', 'w') as file:
        writer = csv.writer(file)
        file.write("label;")
        for i in range(0, 576):
            file.write("histo"+str(i)+";")

        file.write("\n")

def write_data_into_csv(data, label):

    with open('csv/miammiamCSV.csv', 'a') as file:
        writer = csv.writer(file)
        file.write(label+";")
        for i in data:
            file.write(str(i)+";")

        file.write("\n")



data = []
labels = []

def input_csv(liste, path, label):

    for image in liste:

        #on lit l'image, to contours uniquement
        img = cv2.imread(path.format(image))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 100, 200)


        #on récupérer les contours
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

        #on recupere le plus grand
        max_cnt = 0
        for i in contours:
            if cv2.contourArea(i) >= max_cnt:
                max_cnt = cv2.contourArea(i)


        #on fait match le plus grand contour avec la liste puis corp gray
        for i in contours:
            if cv2.contourArea(i) == max_cnt:
                x, y, w, h = cv2.boundingRect(i)
                crop = gray[y:y + h, x:x + w]
                crop = cv2.resize(crop, (50, 50))


        #on prend l'histogram orienté gradient de l'image
            #ICI FAUT LE FAIRE SANS CE MACHIN APRES
        H, hogImage = feature.hog(crop, orientations=9, pixels_per_cell=(10, 10),
                cells_per_block=(2, 2), transform_sqrt=True, block_norm="L1",
                                 visualize=True)


        #on ajoute les info pour le model
        write_data_into_csv(H, label)


        #on affiche les image HOG/gray crop
##        hogImage = exposure.rescale_intensity(hogImage, out_range=(0, 255))
##        hogImage = hogImage.astype("uint8")
##
##        cv2.imshow("HOG Image", hogImage)
##        cv2.imshow("dzq", crop)
##        cv2.waitKey(0)




csv_write()
input_csv(liste1, path1, "0")
input_csv(liste, path, "1")


file =  open('csv/miammiamCSV.csv', 'r')
    
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




model = KNeighborsClassifier(n_neighbors=1)
model.fit(data, label)
joblib.dump(model, "model/miammiam_model") 

predictions = model.predict(data)

print("Score", metrics.accuracy_score(label, predictions))








































































