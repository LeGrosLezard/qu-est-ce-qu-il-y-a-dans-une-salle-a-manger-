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


    #size = [25, 50]
    size = [25, 50]
    h, w, ch = img.shape
    print(w, h)


    print("scanning...")
    save = 0
    for i in size:

        print(i, "iciiiiiiiiiiiiii")
        
        bordL = w%i
        print(bordL)
        bordL = int(bordL / 2)
        print(bordL)


        bordl = h%i
        print(bordl)
        bordl = int(bordl / 2)
        print(bordl)


        copy = img.copy()
        copy = cv2.copyMakeBorder(copy, bordL, bordL, bordl, bordl,
                                 cv2.BORDER_CONSTANT, value=(255, 255, 255))

        for y in range(0, img.shape[0], i):
            for x in range(0, img.shape[1], i):

                if y == img.shape[0] - i:
                    b = y-i
                    d = y
                else:
                    b = y
                    d = y+i



                if x == img.shape[1] - i:
                    a = x-i
                    c = x
                else:
                    a = x
                    c = x+i
 

                cv2.rectangle(copy, (a, b), (c, d), (0, 0, 255), 2)




                #clone_draw = crop.copy()
                #crop_clone = img[y:y+i * ok, x:x+i * ok1]

                

                #show_picture("clone", clone_draw, 1, "")
                show_picture("crop", copy, 0, "")



                save += 1






objects_to_search = ['Cuillere', 'Couteau', 'Fourchette']
for objects in objects_to_search:
    
    liste = os.listdir("../dataset/clean/" + str(objects))

    for picture in liste:
        picture = str("../dataset/clean/") + str(objects) + "/" + str(picture)    
        print(picture)
        main_couse(picture)
























