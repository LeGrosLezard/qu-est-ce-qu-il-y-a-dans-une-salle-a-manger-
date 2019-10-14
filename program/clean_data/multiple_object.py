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



def multiple_objects(contours, blanck, img,
                     path_clean, category, image):

    #show_picture("image", img, 0, "y")

    detection = 0
    stop = True

    last_w_object = 0
    
    for cnts in contours:
        if cv2.contourArea(cnts) > 1:
            
            x, y, w, h = cv2.boundingRect(cnts)
            if h > 20 and w > 5:
            
                if last_w_object > x+w and last_w_object != 0:
                    cv2.rectangle(blanck, (x, y), (x+w, y+h), (0, 0, 255), 1)
                    detection += 1

                last_w_object = x+w

    if detection >= 4:
        os.remove(path_clean.format(category, image))
    else:
        pass
    #show_picture("blanck", blanck, 0, "y")



def rectangle_more_one_object(contours):
    """Here we want separate in case multiple objects by area detection"""

    positionX = []; positionY = []; positionW = []; positionH = [];
    for cnts in contours:
        if cv2.contourArea(cnts) == maxi1 or\
           cv2.contourArea(cnts) == maxi2 or\
           cv2.contourArea(cnts) == maxi3:
            x, y, w, h = cv2.boundingRect(cnts)

            positionX.append(x); positionY.append(y);
            positionW.append(x+w); positionH.append(y+h);

            x, y, w, h = cv2.boundingRect(cnts)
            cv2.drawContours(blanck, cnts, -1, (255, 255, 255), 1)
            cv2.rectangle(blanck, (x, y), (x+w, y+h), (0, 0, 255), 3)
            

    for i in range(len(positionX)):
        print(positionX[i], positionY[i], positionW[i], positionH[i])





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



def transform_i(objects):
    out_objects = ""
    for i in objects:
        for j in i:
            if j in ("é", "è"):
               out_objects += "e"
            else:
                out_objects += j
      
    return out_objects




def take_features_multi_obj(objects_to_search):

    folder_clean = "dataset/clean/{}"
    path_clean = "dataset/clean/{}/{}"

    for objects in objects_to_search:
        objects = transform_i(objects)
        liste_obj = os.listdir(folder_clean.format(objects))
        before = len(liste_obj)
        for image in liste_obj:
            #print("picture: ", image)

            img, objects, contours, blanck =\
            pre_treatment(path_clean, objects, image)

            multiple_objects(contours, blanck, img,
                             path_clean, objects, image)


  
        liste_obj = os.listdir(folder_clean.format(objects))
        print(before - len(liste_obj))



