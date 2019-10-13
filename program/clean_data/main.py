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


from clean_data.background import main_color_background
from clean_data.background import make_cnts
from clean_data.background import find_contour_else_white
from clean_data.background import finish_to_clean_background
from clean_data.background import masking_to_black
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



def take_features(objects_to_search):


    path_folder = "dataset/{}"
    path_picture = "dataset/{}/{}"
    path_clean = "dataset/clean/{}/{}"


    for objects in objects_to_search:

        def transform_i(objects):
            out_word = ""
            for i in objects:
                for j in i:
                    if j in ("é", "è"):
                       out_word += "e"
                    else:
                        out_word += j
              
            return out_word

        objects = transform_i(objects)
        
        os.makedirs(path_picture.format("clean", objects))




        
        liste_obj = os.listdir(path_folder.format(objects))
        for image in liste_obj:

            print("picture: ", image, "\n")

            img = open_picture(path_picture.format(objects, image))

            height, width, channel = img.shape
            if height > 200 and width > 200:
                img = cv2.resize(img, (200, 200))

            blanck = blanck_picture(img)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edged = cv2.Canny(img, 100, 200)

            contours, _ = cv2.findContours(edged, cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

            img = treatment_background(img, objects)  #background
            print(path_clean.format(objects, image))
            cv2.imwrite(path_clean.format(objects, image), img)


##            multiple_objects(contours, blanck, img, path_clean, category)
##            position_rotation(contours, blanck, img, path_clean, category) #rotation
##            
##            break





