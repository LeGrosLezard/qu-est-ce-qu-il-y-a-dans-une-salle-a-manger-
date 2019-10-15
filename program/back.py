import numpy as np
import cv2
import os
import imutils
import math
from PIL import Image





def main_color_background(img):

    dico = {}

    im = Image.fromarray(img)
    for value in im.getdata():
        if value in dico.keys():
            dico[value] += 1
        else:
            dico[value] = 1

    max_value = 0
    color = []
    for key, value in dico.items():
        if value > max_value:
            if key != (0, 255, 0):
                max_value = value
                color = key

    return color



def open_picture(image):

    """We open picture"""

    img = cv2.imread(image)
    return img



def show_picture(name, image, mode, destroy):
    cv2.imshow(name, image)
    cv2.waitKey(mode)
    if destroy == "y":
        cv2.destroyAllWindows()



def blanck_picture(img):

    """Create a black background picture same dimension of original picture"""

    blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
    blank_image[0:img.shape[0], 0:img.shape[1]] = 0, 0, 0

    return blank_image




    





def pre_treatment(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th3 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                cv2.THRESH_BINARY,11,10)

    show_picture("th3", th3, 0, "y")

    blanck0 = blanck_picture(img)
    copy5 = img.copy()

    return th3, blanck0, copy5


def make_first_treatment(th3, copy5):

    cont,h=cv2.findContours(th3,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    for cn in cont:
        if cv2.contourArea(cn) < 10000:
            cv2.drawContours(copy5,[cn],-1,(0,255,0),3)
            cv2.fillPoly(copy5, pts =[cn], color=(0,255,0))

    show_picture("copy5", copy5, 0, "y")

    for i in range(copy5.shape[0]):
        for j in range(copy5.shape[1]):
            if copy5[i, j][0] == 0 and\
               copy5[i, j][1] == 255 and\
               copy5[i, j][2] == 0:
                pass
            else:
                copy5[i, j] = 255, 255, 255
                

    show_picture("copy5", copy5, 0, "y")

    return copy5


def second_treatment(copy5):

    gray = cv2.cvtColor(copy5, cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,250,255,cv2.THRESH_BINARY_INV)
    cont,h=cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    show_picture("thresh", thresh, 0, "y")

    blanck10 = blanck_picture(img)
    for cn in cont:
        print(cv2.contourArea(cn))
        if cv2.contourArea(cn) < 10000:
            cv2.drawContours(blanck10,[cn],-1,(255,255,255),1)
            cv2.fillPoly(blanck10, pts =[cn], color=(255,255,255))

    show_picture("blanck10", blanck10, 0, "y")

    return blanck10

def third_treatment(blanck10, img):


    for i in range(blanck10.shape[0]):
        for j in range(blanck10.shape[1]):
            if blanck10[i, j][0] == 255 and\
               blanck10[i, j][1] == 255 and\
               blanck10[i, j][2] == 255:
                pass
            else:
                img[i, j] = 255, 255, 255



    show_picture("img", img, 0, "y")

    return img


def contours_square(img, name):


    show_picture("img", img, 0, "y")
    th3, blanck0, copy5 = pre_treatment(img)

    copy5 = make_first_treatment(th3, copy5)
    blanck10 = second_treatment(copy5)
    img = third_treatment(blanck10, img)


    show_picture("img", img, 0, "y")
    






liste = os.listdir("test/")
for i in liste:
    i = str("test/") + str(i)

    img = open_picture(i)
    img = cv2.resize(img, (200, 200))
    color = main_color_background(img)

    print(color)

    show_picture("img", img, 0, "y")
    contours_square(img, i)
























