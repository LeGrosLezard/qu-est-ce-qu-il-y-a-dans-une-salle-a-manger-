import os
import cv2
import csv
import joblib
import numpy as np
import pandas as pd
from sklearn import svm
from sklearn import metrics
from skimage import feature
from skimage import exposure
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from sklearn.decomposition import PCA



def open_picture(image):

    img = cv2.imread(image)
    return img

def show_picture(name, image, mode, destroy):

    cv2.imshow(name, image)
    cv2.waitKey(mode)
    if mode == 1:
        time.sleep(0.1)
    if destroy == "y":
        cv2.destroyAllWindows()

def HOG_detection(gray):

    (H, hogImage) = feature.hog(gray, orientations=9,
                                pixels_per_cell=(10, 10),
                                cells_per_block=(2, 2),
                                transform_sqrt=True,
                                block_norm="L1", visualize=True)
    hogImage = exposure.rescale_intensity(hogImage, out_range=(0, 255))
    hogImage = hogImage.astype("uint8")

    return H, hogImage


def blanck_picture(img):
    blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
    blank_image[0:img.shape[0], 0:img.shape[1]] = 0, 0, 0
    return blank_image


def csv_write():
    with open('csv/testtttttttttttttto.csv', 'w') as file:
        writer = csv.writer(file)
        file.write("label;")
        for i in range(0, 15000):
            file.write("pixel"+str(i)+";")

        file.write("\n")



def to_list(thresh):

    data = []
    for i in range(thresh.shape[0]):
        for j in range(thresh.shape[1]):
            if thresh[i, j] > 120:
                nb = 1
            else:
                nb = 0
        
            data.append(nb)

    return data



def write_data_into_csv(data, label):

    with open('csv/testtttttttttttttto.csv', 'a') as file:
        writer = csv.writer(file)
        file.write(label+";")
        for i in data:
            file.write(str(i)+";")

        file.write("\n")
















csv_write()

liste_object = ["Fourchette", "Cuillere", "Couteau"]


label = 0
for objects in liste_object:

    path_pictures = "dataset/clean/{}"
    path_pictures = path_pictures.format(objects)
    objects_picture = os.listdir(path_pictures)
    label += 1

    for picture in objects_picture:
        path_picture = "dataset/clean/{}/{}"
        path_picture = path_picture.format(objects, picture)

        img = open_picture(path_picture)
        img = cv2.resize(img, (100, 150))
        #show_picture("dza", img, 0, "")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #show_picture("gray", gray, 0, "")

        _,thresh = cv2.threshold(gray,245,255,cv2.THRESH_BINARY_INV)
        #show_picture("thresh", thresh, 0, "")

        blanck = blanck_picture(img)

        contours,h=cv2.findContours(thresh,cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            cv2.fillPoly(blanck, pts =[c], color=(255,255,255))
        #show_picture("blanck", blanck, 0, "")


        grayblanck = cv2.cvtColor(blanck, cv2.COLOR_BGR2GRAY)
        contours,h=cv2.findContours(grayblanck,cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

        maxi = 0
        non = False
        for c in contours:
            if cv2.contourArea(c) > 11000:
                non = True
            else:
                if cv2.contourArea(c) > maxi:
                    maxi = cv2.contourArea(c)
        if non is False:
            blanck1 = blanck_picture(img)
            for c in contours:
                if cv2.contourArea(c) == maxi:
                    cv2.fillPoly(blanck1, pts =[c], color=(255,255,255))

            blanck1 = cv2.cvtColor(blanck1, cv2.COLOR_BGR2GRAY)

            data = to_list(blanck1)
            write_data_into_csv(data, str(label))








file =  open('csv/testtttttttttttttto.csv', 'r')
    
dataframe = file.readlines()
dataframe = dataframe[1:]

X = []
Y = []

for i in dataframe:
    liste_w = []
    for j in i:
        if j == "\n":
            X.append(liste_w)
            liste_w = []
        else:
            if j == ";" or j == " ":
                pass
            else:
                try:
                    j = int(j)
                    liste_w.append(int(j))
                except:
                    liste_w.append(str(j))


for i in X:
    Y.append(i[0])
    del i[0]



X_train, Y_train =  X, Y
X_test,Y_test = X, Y


model = svm.SVC(kernel="linear",C=2)
model.fit(X_train,Y_train)
joblib.dump(model, "models/jojo") 
predictions = model.predict(X_test)

print("Score", metrics.accuracy_score(Y_test, predictions))






