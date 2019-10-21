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


#-------------------------------- CSV treatment

"""
    ; it changes row
    \n jump lines

"""



def csv_write(csv_name, number_pix):
    """
        Wrtting head of csv
        number of pixels
        label of data
    """

    #open csv
    with open(csv_name, 'w') as file:
        writer = csv.writer(file)

        #first case write label
        file.write("label;")

        #write pixel + number ex: pixel50
        for i in range(0, number_pix):
            file.write("pixel"+str(i)+";")

        file.write("\n")




def to_list(thresh):
    """
        Transform picture to only 0 or 1
        if pix > 120 => 1
        else pix < 120 => 0
    """

    data = []

    #We course the binarized picture right to left, top to bot
    for i in range(thresh.shape[0]):
        for j in range(thresh.shape[1]):

            #if value of pixel > 120 we put 1 else 0
            if thresh[i, j] > 120:
                nb = 1
            else:
                nb = 0

            data.append(nb)

    #our picture
    return data



def write_data_into_csv(csv_name, data, label):
    """
        Fill the csv
            - lign to pixel value (0 or 1)
            - label number (name of label ex: 1->dog 2-> cat)
    """

    #open csv
    with open(csv_name, 'a') as file:
        writer = csv.writer(file)

        #write label scored (0 cat, 1 dog)
        file.write(label+";")

        #for value from picture we write it
        for i in data:
            file.write(str(i)+";")

        file.write("\n")



#-------------------------------- Picture treatment

def open_picture(image):
    """
        Open picture
    """

    img = cv2.imread(image)
    return img

def show_picture(name, image, mode, destroy):
    """
        Show picture
        mode 0 -> input a key
        mode 1 -> it display and unindisplay all 0.1 sec
        destroy = y -> windows destroy
    """

    cv2.imshow(name, image)

    #It wait an entrance for pass to next
    cv2.waitKey(mode)

    #It wait x times to pass to next
    if mode == 1:
        time.sleep(0.1)

    #It destroy the current window
    if destroy == "y":
        cv2.destroyAllWindows()


def blanck_picture(img):
    """
        Create a empty black picture
    """
    #Make a picture: width, height and channel in unint8
    blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
    #Make picture 0 to width 0 to height black
    blank_image[0:img.shape[0], 0:img.shape[1]] = 0, 0, 0
    return blank_image



def make_contours(img):
    """
        Gray one channel
        thresh binarize gray
        find the contour with RETR (for binarized picture)
                              EXTER (all points)
        filled it for a filled contour
    """

    #Create a black picture
    blanck = blanck_picture(img)

    #one channel
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #make threshold filter
    _,thresh = cv2.threshold(gray,245,255,cv2.THRESH_BINARY_INV)

    #Search contours from thresh
    contours,h=cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)

    #Filled contours to white on our black empty picture
    for cnts in contours:
        cv2.fillPoly(blanck, pts=[cnts], color=(255,255,255))

    return blanck


def take_max_contour_to_csv(blanck):
    """
        Recup the max contour (imutil function better)
        and redraw it on a new picture
    """

    #Grayscal picture for one channel
    grayblanck = cv2.cvtColor(blanck, cv2.COLOR_BGR2GRAY)

    #Find contours
    contours,h=cv2.findContours(grayblanck,cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)

    #max cnt; bad picture so pass;
    maxi = 0; non = False;

    #take the max contour
    for cnts in contours:

        #but if area of contour > 11000: bad background !
        if cv2.contourArea(cnts) > 11000:
            non = True

        else:
            if cv2.contourArea(cnts) > maxi:
                maxi = cv2.contourArea(cnts)

    #Not a good picture if True
    if non is False:

        #Draw the max contour on a black picture
        blanck1 = blanck_picture(img)
        for cnts in contours:
            if cv2.contourArea(c) == maxi:
                cv2.fillPoly(blanck1, pts =[cnts], color=(255,255,255))

        blanck1 = cv2.cvtColor(blanck1, cv2.COLOR_BGR2GRAY)


    return blanck1


def picture_treatment(path_picture):
    """
        We open picture,
        resize it
        draw contours from a binarized function
        re draw it for the max contour (only one contour)
        transform it to 0 and 1
        wirte it on csv file
    """

    img = open_picture(path_picture)
    img = cv2.resize(img, (100, 150))
    #show_picture("dza", img, 0, "")

    blanck = make_contours(img)
    blanck1 = take_max_contour(blanck)

    data = to_list(blanck1)
    write_data_into_csv(data, str(label))



#-------------------------------- Model treatment

def csv_to_list(csv_name):
    """
        Recup data from csv
        we only take dataframe[1:]
            because dataframe[1] is the label
        we add data on list
            X for 0 or 1 pix of picture
            Y for label
    """

    file =  open(csv_name, 'r')

    #dataframe[1] == label !
    dataframe = file.readlines()
    dataframe = dataframe[1:]

    X = []; Y = [];

    for i in dataframe:

        #it serve to make a list of list it's a work list
        liste_w = []

        for j in i:
            #if element is a jump add
                #work list to final list and
                #reinitialize it
            if j == "\n":
                X.append(liste_w)
                liste_w = []

            else:
                #pass if it's a delemiter or " "
                if j == ";" or j == " ":
                    pass

                else:
                    #If we put a str(label)
                    try:
                        j = int(j)
                        liste_w.append(int(j))
                    except:
                        liste_w.append(str(j))

    #Here we recup label
    for i in X:
        Y.append(i[0])
        del i[0]

    return X, Y



def training(X, Y, model_name):
    """
        We define train data and test data
        We call SVC who's linear function
        We define model name
        And make the prediction
    """

    #define test and train data
    X_train, Y_train =  X, Y
    X_test,Y_test = X, Y

    #call SVC function
    model = svm.SVC(kernel="linear",C=2)

    #fit method
    model.fit(X_train,Y_train)

    #create model
    joblib.dump(model, model_name)

    #predict it!
    predictions = model.predict(X_test)

    print("Score", metrics.accuracy_score(Y_test, predictions))







def main(csv_name, number_pix, path_picture, model_name):

    #Write header of csv
    csv_write(csv_name, number_pix)

    #Write pixel of picture into csv
    picture_treatment(path_picture)

    #Recup data from csv
    X, Y = csv_to_list(csv_name)

    #And make a model
    training(X, Y, model_name)






