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
    img = cv2.imread(image)
    height, width, channel = img.shape

    return img


def parcours_image(img):

    clone = img.copy()
    size = 25

    for y in range(0, img.shape[0], size):
        for x in range(0, img.shape[1], size):


            def into_picture(img, x_picture, y_picture):
                crop = img[y:y+size*y_picture, x:x+size*x_picture]
                show_picture("crop", crop, 0, "y")

            for nb in range(1, 4):
                into_picture(img, nb, 1)
                into_picture(img, 1, nb)
                into_picture(img, nb, nb)


            cv2.rectangle(clone, (x, y), (x + size, y + size), (0, 255, 0), 2)

            show_picture("clone", clone, 1, "")
            time.sleep(0.3)




def show_picture(name, image, mode, destroy):
    cv2.imshow(name, image)
    cv2.waitKey(mode)
    if destroy == "y":
        cv2.destroyAllWindows()



if __name__ == "__main__":

    img = open_picture("assiette1.jpg")
    parcours_image(img)


