import cv2
import os

import numpy as np
import imutils



def open_picture(image):
    """We open picture"""

    img = cv2.imread(image)
    return img



def show_picture(name, image, mode, destroy):
    cv2.imshow(name, image)
    cv2.waitKey(mode)
    if mode == 1:
        time.sleep(0.2)
    if destroy == "y":
        cv2.destroyAllWindows()
    

def save_picture(name, image):
    path = "dataset/data_analysing/{}"
    cv2.imwrite(path.format(str(name)), image)


def blanck_picture(img):

    """Create a black background picture same dimension of original picture"""

    blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
    blank_image[0:img.shape[0], 0:img.shape[1]] = 0, 0, 0

    return blank_image



def find_object(img):

    """
        We binarising picture
        for only have a form of our object.
        We search contours now
    """

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray,250,255,cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)
    return contours


def recup_object(contours, img):

    """
        We search the max contours.
        Sometimes there are noise of litle
        area of the rest of the background
        of pixels (5x5) of background.
        We don't want it !

        After we make a crop of that.
    """

    maxi = 0
    for cnts in contours:
        if cv2.contourArea(cnts) > maxi:
            maxi = cv2.contourArea(cnts)


    for cnts in contours:
        if cv2.contourArea(cnts) == maxi:
 
            x, y, w, h = cv2.boundingRect(cnts)
            crop = img[y:y+h, x:x+w]

            return crop


def main_croping(picture):

    img = open_picture(picture)
    
    contours = find_object(img)
    crop = recup_object(contours, img)

    return crop

