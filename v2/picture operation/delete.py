"""Here we delete bad picture"""

import os
import cv2
import math
import time
import imutils
import numpy as np
from PIL import Image
from time import time


def open_picture(image):
    """open picture"""

    img = cv2.imread(image)
    return img



def show_picture(name, image, mode, destroy):
    """
        Show picture
        mode 0 = entrance key  pass to next
        mode y = destroy windows
    """

    cv2.imshow(name, image)
    cv2.waitKey(mode)

    if mode == 1:
        time.sleep(0.1)
    if destroy == "y":
        cv2.destroyAllWindows()


def recup_contour(img):
    """
        Recup max contour
        if contour < 1400 so it's a residues
        else background remove has failed
    """

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,250,255,cv2.THRESH_BINARY_INV)

    contours,h=cv2.findContours(thresh,cv2.RETR_TREE,
                                cv2.CHAIN_APPROX_NONE)

    maxi = 0; delete = False;
    for cnts in contours:
        if cv2.contourArea(cnts) > maxi:
            maxi = cv2.contourArea(cnts)

    if maxi < 1400 or maxi > 12000:
        delete = True

    return delete


def timmer():
    start = time()
    while True:
        if time() - start >= 60:
            return "stop"


def main_deleting(img):
    """
        We deleting on contour
    """
    timmer()
    if timer == "stop":
        return "stop"
    img = open_picture(img)
    delete = recup_contour(img)

    return delete
