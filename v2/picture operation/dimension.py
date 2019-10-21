import numpy as np
import cv2
import os
import imutils
import math
from PIL import Image
import time



def open_picture(image):

    """We open picture"""

    img = cv2.imread(image)
    return img



def show_picture(name, image, mode, destroy):
    cv2.imshow(name, image)
    cv2.waitKey(mode)
    if mode == 1:
        time.sleep(0.1)
    if destroy == "y":
        cv2.destroyAllWindows()



def blanck_picture(img):

    """Create a black background picture same dimension of original picture"""

    blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
    blank_image[0:img.shape[0], 0:img.shape[1]] = 0, 0, 0

    return blank_image





liste = os.listdir(r"C:\Users\jeanbaptiste\Desktop\assiette\program\dataset\clean\Cuillere")
path=r"C:\Users\jeanbaptiste\Desktop\assiette\program\dataset\clean\Cuillere\{}"


def recup_contour(img, blanck):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,250,255,cv2.THRESH_BINARY_INV)
    

    contours,h=cv2.findContours(thresh,cv2.RETR_TREE,
                                cv2.CHAIN_APPROX_NONE)

    maxi = 0
    for cnts in contours:
        if cv2.contourArea(cnts) > maxi:
            maxi = cv2.contourArea(cnts)

    for cnts in contours:
        if cv2.contourArea(cnts) == maxi:
            cv2.drawContours(blanck, cnts, -1, (0, 0, 255), 1)

    return blanck

def recup_points(blanck):
    
    listex = []
    listey = []

    for i in range(blanck.shape[0]):
        for j in range(blanck.shape[1]):
            if blanck[i, j][0] == 0 and\
               blanck[i, j][1] == 0 and\
               blanck[i, j][2] == 255:
                listex.append(i)
                listey.append(j)

    return listex, listey


def recup_size(listex, listey):

    Xy_min = min(listex)
    Xy_max = max(listex)

    L = abs(Xy_min - Xy_max)
    Lcm = L / 37.79527559055
    print("longueur:", Lcm)

    a = min(listey)
    c = max(listey)

    l = abs(a - c)
    lcm = l / 37.79527559055
    print("largeur max:", lcm)


    return Lcm, lcm

def main(img):

    img = path.format(i)
    img = open_picture(img)

    blanck = blanck_picture(img)

    blanck = recup_contour(img, blanck)
    listex, listey = recup_points(blanck)
    Lcm, lcm = recup_size(listex, listey)

    show_picture(";p^", blanck, 0, "")





for i in liste:
    main(path.format(i))



























