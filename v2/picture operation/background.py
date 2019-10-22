"""Here we place a white background"""

import os
import cv2
import math
import time
import imutils
import numpy as np
from PIL import Image
from time import time

def open_picture(image):
    """We open picture"""

    img = cv2.imread(image)
    return img

def show_picture(name, image, mode, destroy):
    """
        Show picture
        mode 0 = entrance key  pass to next
        mode y = destroy windows
    """
    
    cv2.imshow(name, image)
    if mode == 0:
        cv2.waitKey(mode)
    if mode == 1:
        time.sleep(1)
        cv2.destroyAllWindows()
    if destroy == "y":
        cv2.destroyAllWindows()

def blanck_picture(img):
    """
        Create a black empty picture
    """

    blank_image = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    blank_image[0:, 0:] = 0, 0, 0

    return blank_image


def main_color_background(img):
    """
        Here we recup the main color
        by the recurrent pixel
    """

    dico = {}; max_value = 0; color = []

    #Convert picture to array
    im = Image.fromarray(img)
    #data from array recup value pixels 
    for value in im.getdata():
        if value in dico.keys():
            dico[value] += 1
        else:
            dico[value] = 1

    #recup main pixel presence
        #except for green pixels (use for our contours)
    for key, value in dico.items():
        if value > max_value and key != (0, 255, 0):
            max_value = value; color = key;

    return color




def pre_treatment(img):

    """
        Gray,
        ADAPTIVE_THRESH_GAUSSIAN_C,
        Make copy, and white picture.
    """

    #One channel.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Binarized with gaussian by sum of neighboors.
    th3 = cv2.adaptiveThreshold(gray, 255,
                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY,11,5)

    copy = img.copy()

    return th3, copy



def make_first_treatment(th3, copy):

    """
        contours (filled),
        only keep contours,
        other white.
    """

    #Complete Contours + all points.
    cont,h=cv2.findContours(th3,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    #Recup max contour.
    maxi = 0
    for cnt in cont:
        if cv2.contourArea(cnt) > maxi:
            maxi = cv2.contourArea(cnt)

    #Draw contour exept the bigger (border of image).
    for cnt in cont:
        if cv2.contourArea(cnt) != maxi:
            #Add + 2 to the borders (no holes).
            cv2.drawContours(copy,[cnt], -1, (0,255,0), 3)
            #Filled contours.
            cv2.fillPoly(copy, pts =[cnt], color=(0, 255, 0))

    #Delete all picture execpt greens statements.
    for i in range(copy.shape[0]):
        for j in range(copy.shape[1]):
            if copy[i, j][0] == 0 and\
               copy[i, j][1] == 255 and\
               copy[i, j][2] == 0:
                pass
            else:
                copy[i, j] = 255, 255, 255

    return copy



def second_treatment(copy, img):
    """
        Gray,
        Thresh,
        Contours filled.
    """

    #Gray, Binzarized, Contours.
    gray = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    #Create empty black picture
    blanck = blanck_picture(img)

    #For all contours except if < 100 (littles contours)
    #Reredraw it.
    for cnt in contours:

        if cv2.contourArea(cnt) > 100:
            cv2.drawContours(blanck,[cnt],-1,(255,255,255), 3)
            cv2.fillPoly(blanck, pts =[cnt], color=(255,255,255))

    return blanck



def third_treatment(blanck, img):
    """
        Raise all execpt object on current picture
        from blanck picture who's in black and white.
    """

    for i in range(blanck.shape[0]):
        for j in range(blanck.shape[1]):
            if blanck[i, j][0] == 255 and\
               blanck[i, j][1] == 255 and\
               blanck[i, j][2] == 255:
                pass
            else:
                img[i, j] = 255, 255, 255
    return img


def timmer():
    start = time()
    while True:
        if time() - start >= 60:
            return "stop"

def main_background(img):

    #keep name for saving.
    name = img
    timmer()
    if timer == "stop":
        return "stop"

    img = open_picture(img)
    x, w, ch = img.shape
    if x > 5000:
        img = cv2.resize(open_picture(img), (200, 200))

    #show_picture("dzad", img, 0, "")

    color = main_color_background(img)

    if color != (255, 255, 255):
        #Threshold + copy current picture.
        th3, copy = pre_treatment(img)

        #First treatment contour on green.
        copy = make_first_treatment(th3, copy)

        #Second treatment on blanck.
        blanck = second_treatment(copy, img)

        #Finish it on copy picture.
        img = third_treatment(blanck, img)

        return img

    else:
        return img

#main(r"C:\Users\jeanbaptiste\Desktop\assiette\program\dataset\aa\images.jpg")
