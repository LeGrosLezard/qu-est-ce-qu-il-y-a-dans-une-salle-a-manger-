import cv2
import os
import csv
import numpy as np

from skimage import exposure
from skimage import feature

import time
import joblib
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
    


def blanck_picture(img):

    """Create a black background picture same dimension of original picture"""

    blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
    blank_image[0:img.shape[0], 0:img.shape[1]] = 0, 0, 0

    return blank_image





def main_couse(img):



    img = open_picture(img)
    show_picture("dza", img, 0, "")


    size = [25, 50]

    print("scanning...")
    save = 0
    for i in size:
        for y in range(0, img.shape[0], i):
            for x in range(0, img.shape[1], i):
                
                clone_draw = img.copy()
                #crop_clone = img[y:y+i, x:x+i]

                cv2.rectangle(clone_draw, (x, y), (x+i, y+i), (0, 0, 255), 2)

                show_picture("clone", clone_draw, 1, "")
                #show_picture("crop", crop_clone, 0, "")



                save += 1
































