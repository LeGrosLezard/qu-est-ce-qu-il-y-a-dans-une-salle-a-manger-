import cv2
import os
import csv
import numpy as np

from skimage import exposure
from skimage import feature

import time
import joblib
import imutils

import requests
import datetime
import urllib.request
from bs4 import *
import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import json
import urllib
import sys
import time
import urllib.request





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

















    

if __name__ == "__main__":




    def treatment_picture_download():
        #objects_to_search = searching_on_internet(label)
        objects_to_search = ["cuillere", "fourchette", "couteau", "verre"]
        open_download_folder(objects_to_search)















