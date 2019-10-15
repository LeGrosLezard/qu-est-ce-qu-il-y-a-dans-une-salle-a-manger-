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






def find_contour(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,250,255,cv2.THRESH_BINARY_INV)

    #show_picture("thresh", thresh, 0, "y")

    contours,h=cv2.findContours(thresh,cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)

    blanck1 = blanck_picture(img)

    return blanck1, contours


def recup_object(img, blanck1, contours,
                 name):
    c = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > 500:

            blanck1 = blanck_picture(img)
            copy = img.copy()

            cv2.drawContours(blanck1,[cnt],-1,(0,255,0),1)
            cv2.fillPoly(blanck1, pts =[cnt], color=(0,255,0))

            for i in range(blanck1.shape[0]):
                for j in range(blanck1.shape[1]):
                    if blanck1[i, j][0] == 0 and\
                       blanck1[i, j][1] == 255 and\
                       blanck1[i, j][2] == 0:
                        pass
                    else:
                        copy[i, j] = 255, 255, 255

            save_or_delete(copy, name, c)

            c+=1

    return copy



def save_or_delete(copy, name, counter):

    gray = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,250,255,cv2.THRESH_BINARY_INV)

    #show_picture("thresh", thresh, 0, "y")

    contours,h=cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


    for cnts in contours:
        if cv2.contourArea(cnts) > 9000:
            #os.remove(name)
            pass
        else:
            #show_picture("copy", copy, 0, "y")
            return copy





def take_features_multi_obj(img):


    try:
        name = str(img)

        img = open_picture(img)
        img = cv2.resize(img, (200, 200))

        show_picture("img", img, 0, "y")

        blanck1, contours = find_contour(img)
        copy = recup_object(img, blanck1, contours,
                            name)

        #show_picture("copy", copy, 0, "y")
        cv2.imwrite(name, copy)
    except:
        pass

