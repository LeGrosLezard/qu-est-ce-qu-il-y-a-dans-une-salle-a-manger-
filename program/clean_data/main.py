import numpy as np
import cv2
import os
import imutils
import math
from PIL import Image


def take_features(liste_obj, category):

    path = "dataset1/{}/{}"
    path_clean = "dataset1/clean/{}/{}"
    for i in liste_obj:

        print("picture: ", i, "\n")
        img = open_picture(path.format(category, i))
        

        height, width, channel = img.shape
        if height > 200 and width > 200:
            img = cv2.resize(img, (200, 200))

        blanck = blanck_picture(img)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(img, 100, 200)

        contours, _ = cv2.findContours(edged, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)

        treatment_background(img, path_clean, category)  #background
        multiple_objects(contours, blanck, img, path_clean, category)
        position_rotation(contours, blanck, img, path_clean, category) #rotation
        
        break

def open_download_folder(objects_to_search):

    for i in objects_to_search:

        liste_obj = os.listdir("dataset1/" + i)
        contours_obj, blanck = take_features(liste_obj, i)  #take_features


def treatment_background(img, path_clean, category):
    name = str(img)
    img = cv2.resize(img, (200, 200))
    color = main_color_background(img)

    #if background black
    if color[0] < 200 and color[1] < 200 and color[2] < 200:

        #make a blanck, a copy and make contour
        blanck, copy_img, copy_img1 = make_cnts(img)

        #We take contours of object and delete the background for a white bg
        img = find_contour_else_white(img, blanck, copy_img)

        #we delete the rest of bg
        color = finish_to_clean_background(img)

        #it'so ok now
        img = masking_to_black(img, color)



def position_rotation(contours, blanck, img, path_clean, category):


    position_circleX, position_circleY = draw_contours(contours, blanck)

    listex, listey, listex2, listey2 = recup_red_points(blanck)

    X_min, Xy_min, X_max, Xy_max,\
    X_min2, Xy_min2, X_max2, Xy_max2, blanck\
    = points_for_define_inclinaison(listex, listey, listex2, listey2, blanck)

    position = treatment_inclinaison(X_min, Xy_min, X_max, Xy_max,
                                     X_min2, Xy_min2, X_max2, Xy_max2)

    precise_angle(img, X_min, Xy_min, X_max, Xy_max,
                  X_min2, Xy_min2, X_max2, Xy_max2,
                  position, blanck, path_clean, category)

    

if __name__ == "__main__":


    objects_to_search = ["cuillere", "fourchette", "couteau", "verre"]
    open_download_folder(objects_to_search)
