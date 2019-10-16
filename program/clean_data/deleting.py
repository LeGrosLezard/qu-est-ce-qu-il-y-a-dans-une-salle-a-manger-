import numpy as np
import cv2
import os
import imutils
import math
from PIL import Image
import time






def open_picture(image):

    """We open picture"""

    img = cv2.imread(image)
    return img



def show_picture(name, image, mode, destroy):
    cv2.imshow(name, image)
    cv2.waitKey(mode)
    if mode == 1:
        time.sleep(0.1)
    if destroy == "y":
        cv2.destroyAllWindows()






def recup_contour(img):
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,250,255,cv2.THRESH_BINARY_INV)

    

    contours,h=cv2.findContours(thresh,cv2.RETR_TREE,
                                cv2.CHAIN_APPROX_NONE)

    maxi = 0
    for cnts in contours:
        if cv2.contourArea(cnts) > maxi:
            maxi = cv2.contourArea(cnts)

    return contours, maxi

def deleting(contours, maxi, img):

    for cnts in contours:
        if cv2.contourArea(cnts) == maxi:

            if 40000 > cv2.contourArea(cnts) < 1400:
                return True

                #show_picture("thresh", thresh, 0, "y")

                #  1400          1800 12000         40049
    return False


def main_deleting(img):

    img = open_picture(img)
    contours, maxi = recup_contour(img)
    delete = deleting(contours, maxi, img)

    return delete







