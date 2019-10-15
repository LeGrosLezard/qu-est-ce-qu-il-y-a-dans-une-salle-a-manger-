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












liste = os.listdir(r"C:\Users\jeanbaptiste\Desktop\assiette\program\test")
for i in liste:
    i = str(r"C:\Users\jeanbaptiste\Desktop\assiette\program\test/") + str(i)
    print(i)


    img = open_picture(i)
    img = cv2.resize(img, (500, 500))

    copy = img.copy()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,250,255,cv2.THRESH_BINARY_INV)

    show_picture("thresh", thresh, 0, "y")

    contours,h=cv2.findContours(thresh,cv2.RETR_TREE,
                                cv2.CHAIN_APPROX_NONE)

    maxi = 0
    for cnts in contours:
        if cv2.contourArea(cnts) > maxi:
            maxi = cv2.contourArea(cnts)



    for cnts in contours:
        if cv2.contourArea(cnts) == maxi:
            cv2.drawContours(copy, cnts, -1, (0, 0, 255), 2)




    listex = []
    listey = []

    for y in range(copy.shape[1]):
        for x in range(copy.shape[0]):
            if copy[y, x][0] == 0 and\
               copy[y, x][1] == 0 and\
               copy[y, x][2] == 255: 
                listex.append(x)
                listey.append(y)



    #take max (x, y) and min (x, y) on l and L
    X_min = min(listex)
    index_min = listex.index(min(listex))
    Xy_min = listey[index_min]

    X_max = max(listex)
    index_max = listex.index(max(listex))
    Xy_max = listey[index_max]

    print(X_min, Xy_min)
    print(X_max, Xy_max)


    #402 - 98 456 - 21/ 484-8 451-64 -> mettre a 90 -< puis 90





    
    #width
    cv2.circle(copy, (X_max, Xy_max), 6, (0, 255, 0), 6)
    cv2.circle(copy, (X_min, Xy_min), 6, (255, 255, 0), 6)



    show_picture("copy", copy, 0, "y")

    b = 500 - X_min
    a = math.atan(b/500 - Xy_min)
    c = math.degrees(a)
    c = c + 45

    rows = img.shape[0]
    cols = img.shape[1]
    img_center = (cols / 2, rows / 2)
    M = cv2.getRotationMatrix2D(img_center, - c, 1)
    rotated = cv2.warpAffine(copy, M, (cols, rows), borderValue=(255,255,255))

    c+=1

    show_picture("rotated", rotated, 0, "y")

























