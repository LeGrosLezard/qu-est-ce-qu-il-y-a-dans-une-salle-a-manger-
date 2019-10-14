import numpy as np
import cv2
import os
import imutils
import math
from PIL import Image


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



def main_color_background(img):

    """
        We verify white is the current background
        Indeed, we recup the main color of picture.
    """
    
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
            max_value = value
            color = key

    return color



def make_cnts(img):

    """
        We copy the picture,
        apply adaptativ threshold,
        make contour,
        and draw it into white image
    """

    copy_img = img.copy()
    copy_img1 = img.copy()

    #show_picture("copy_img1", copy_img1, 0, "y")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blanck = blanck_picture(img)

    th3 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                cv2.THRESH_BINARY,11,10)

    #show_picture("thresh", th3, 0, "y")


    contours, _ = cv2.findContours(th3, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)
    
    for cnts in contours:
        if 50 < cv2.contourArea(cnts) < 30000:
            cv2.drawContours(blanck, cnts, -1, (255, 255, 255), 1)

    #show_picture("blanck", blanck, 0, "y")

    return blanck, copy_img, copy_img1




def find_contour_else_white(img, blanck, copy_img):

    """
        We drawing a big contour on the copy of image.
        On the picture we detect contour from copy
        It give us the object in a big area of the picture
        Indeed if on the copy != green we put only white
    """

    gray_blanck = cv2.cvtColor(blanck, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(gray_blanck, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(copy_img, contours, -1, (0, 255, 0), 26)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if copy_img[i, j][0] != 0 and\
               copy_img[i, j][1] != 255 and\
               copy_img[i, j][2] != 0:
                img[i, j] = 255, 255, 255

    return img



def finish_to_clean_background(img):

    """
        We recup the main color now
        because we have object + background
    """
    
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
        if value > max_value and key != (255, 255, 255):
            max_value = value
            color = key

    return color



def masking_to_black(img, color):

    """We delete the rest of bakcground"""
    
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j][0] > color[0] - 70 and\
               img[i, j][0] < color[0] + 70 and\
               img[i, j][1] > color[1] - 70 and\
               img[i, j][1] < color[1] + 70 and\
               img[i, j][2] > color[1] - 70 and\
               img[i, j][2] < color[2] + 70:
                img[i, j] = 255, 255, 255


    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j][0] < 50 and\
               img[i, j][1] < 50 and\
               img[i, j][2] < 50:
                img[i, j] = 255
               

    #show_picture("img", img, 0, "")
    

    return img





def treatment_background(img, category):
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

    else:
        pass

    return img



def transform_i(objects):
    out_objects = ""
    for i in objects:
        for j in i:
            if j in ("é", "è"):
               out_objects += "e"
            else:
                out_objects += j
      
    return out_objects



def pre_treatment(path_picture, objects, image):
    img = open_picture(path_picture.format(objects, image))

    height, width, channel = img.shape
    if height > 200 and width > 200:
        img = cv2.resize(img, (200, 200))

    blanck = blanck_picture(img)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(img, 100, 200)

    contours, _ = cv2.findContours(edged, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)



    return img, objects, contours, blanck




def take_features_background(objects_to_search):


    path_folder = "dataset/{}"
    path_picture = "dataset/{}/{}"
    path_clean = "dataset/clean/{}/{}"


    for objects in objects_to_search:

        objects = transform_i(objects)
        os.makedirs(path_picture.format("clean", objects))

        liste_obj = os.listdir(path_folder.format(objects))

        for image in liste_obj:

            print("picture: ", image)

            try:
                #contours, blanck
                img, objects, contours, blanck =\
                pre_treatment(path_picture, objects, image)

                #background
                img = treatment_background(img, objects)
                cv2.imwrite(path_clean.format(objects, image), img)

            except:
                pass
