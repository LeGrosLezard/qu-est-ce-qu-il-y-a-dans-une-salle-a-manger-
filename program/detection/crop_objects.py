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
    

def save_picture(name, image):

    cv2.imwrite("dataset/data_analysing/" + str(name), image)


def blanck_picture(img):

    """Create a black background picture same dimension of original picture"""

    blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
    blank_image[0:img.shape[0], 0:img.shape[1]] = 0, 0, 0

    return blank_image




def blanck_picture_white(img):

    """Create a black background picture same dimension of original picture"""

    blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
    blank_image[0:img.shape[0], 0:img.shape[1]] = 255, 255, 255

    return blank_image




def get_other_object(img):

    """We detecte contours from the picture
    We try to recup them and to put it into rectangle"""

    blanck = blanck_picture(img)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(img, 0, 160)
    th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)

    contours, _ = cv2.findContours(th3, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)

    liste = []
    for cnts in contours:
        pts = [x, y, w, h] = cv2.boundingRect(cnts); liste.append(pts)
        cv2.drawContours(blanck, cnts, -1, (255, 255, 255), 1)

    #show_picture("blanck", blanck, 0, "y")

    return liste



def croping_it_from_original(img, liste):

    """Now we must fusion the multiples detections from
    a single object.
    We must crop it now for an other matching with current model"""

    liste_area = []
    for i in liste:
        if i[2] > 10 and i[3] > 10 and\
           i[2] < img.shape[0] and i[3] < img.shape[1]:
            liste_area += [i]

    copy2, liste_area = one_detection_for_one_picture(liste_area, img)
    objects_to_picture(copy2, liste_area, img)




def one_detection_for_one_picture(liste_area, img):
    """ on supprimre les detections dans les detections"""


    for _ in range(2):
        for i in liste_area:
            copy = img.copy()
            for j in liste_area:
                if j[0] > i[0] + 2 and j[0] + j[2] < i[0] + i[2] or\
                   j[0] + j[2] - 2 > i[0] and j[0] + j[2] < i[0] + i[2]:

                    cv2.rectangle(copy, (i[0], i[1]), (i[0] + i[2], i[1] + i[3]),
                                  (0, 0, 255), 2)

                    cv2.rectangle(copy, (j[0], j[1]), (j[0] + j[2], j[1] + j[3]),
                                  (255, 0, 0), 1)

                    liste_area.remove(j)


    copy2 = img.copy()
    for i in liste_area:
        cv2.rectangle(copy2, (i[0], i[1]), (i[0] + i[2], i[1] + i[3]),
                      (0, 0, 255), 1)

    #show_picture("copy2", copy2, 1, "")

    return copy2, liste_area




def part_of_object(crop):

    size = [25, 50]

    print("scanning...")

    save = 0
    for i in size:
        for y in range(0, crop.shape[0], i):
            for x in range(0, crop.shape[1], i):

                clone_draw = crop.copy()
                crop_clone = crop[y:y+i, x:x+i]

                cv2.rectangle(clone_draw, (x, y), (x+i, y+i), (0, 0, 255), 2)

                #show_picture("clone", clone_draw, 1, "")
                #show_picture("crop", crop_clone, 0, "")

                #save_picture("crop_learning/" + str(i) + str(save) + ".jpg", crop_clone)
                
                save += 1


def objects_to_picture(copy2, liste_area, img):

    for i in liste_area:
        crop = img[i[1]:i[1] + i[3], i[0]:i[0]+i[2]]
        save_picture(str(i) + ".jpg", crop)


        copy_crop = crop.copy()

        crop = cv2.copyMakeBorder(crop, 50, 50, 50, 50,
                                  cv2.BORDER_CONSTANT, value=(255, 255, 255))

        part_of_object(crop)


    #save_picture(str("analysing") + ".jpg", img)


def detection_picture(model, image):

    #load model
    model = joblib.load("models/miammiamsvmImage")

    #open img and copy it
    img = open_picture("dataset/assiette_couvert/assiette1.jpg")
    img_copy = img.copy()


    #get other items on picture
    liste = get_other_object(img)

    """     IN COURSE    """    
    croping_it_from_original(img_copy, liste)








