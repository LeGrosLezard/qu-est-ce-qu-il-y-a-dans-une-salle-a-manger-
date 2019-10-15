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












liste = os.listdir(r"C:\Users\jeanbaptiste\Desktop\assiette\program\dataset\cuillere")
for i in liste:
    i = str(r"C:\Users\jeanbaptiste\Desktop\assiette\program\dataset\cuillere/") + str(i)
    print(i)
    img = open_picture(i)
    img = cv2.resize(img, (200, 200))

    copy = img.copy()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,250,255,cv2.THRESH_BINARY_INV)

    show_picture("thresh", thresh, 0, "y")

    contours,h=cv2.findContours(thresh,cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)


    for cnts in contours:
        if cv2.contourArea(cnts) > 5:
            cv2.drawContours(copy, cnts, -1, (0, 0, 255), 2)

            M = cv2.moments(cnts)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])


    cv2.circle(copy, (cX, cY), 3, (0,255,0), 3)
    show_picture("copy", copy, 0, "y")




    listex = []
    listey = []

    listex2 = []
    listey2 = []


    for x in range(thresh.shape[0]):
        for y in range(thresh.shape[1]):
            if thresh[x, y] == 255:
                listex.append(x)
                listey.append(y)
   
            if thresh[y, x] == 255:
                listex2.append(x)
                listey2.append(y)


    bas1 = min(listey)
    bas2 = listex[listey.index(min(listey))]

    haut1 = max(listey)
    haut2 = listex[listey.index(max(listey))]


    print(bas1, bas2)
    print(haut1, haut2)



    cv2.circle(copy, (bas1, bas2), 6, (0, 255, 0), 6)
    cv2.circle(copy, (haut1, haut2), 6, (255, 0, 0), 6)





    show_picture("copy", copy, 0, "y")

    c = 0
    if bas1 + 50 < haut1 and\
       bas2 > haut2 + 25:
        print("un")

        while True:
            print(cX - c)
            cv2.circle(copy, (cX - c, cY), 3, (0,255,0), 3)
            rows = img.shape[0]
            cols = img.shape[1]
            img_center = (cols / 2, rows / 2)
            M = cv2.getRotationMatrix2D(img_center, c, 1)
            rotated = cv2.warpAffine(copy, M, (cols, rows), borderValue=(255,255,255))
            show_picture("img", rotated, 0, "y")


            c+=1




    elif abs(bas2 - haut2) < 25 and\
         bas1 + 100 < haut1:
        print("90")


        rows = img.shape[0]
        cols = img.shape[1]
        img_center = (cols / 2, rows / 2)
        M = cv2.getRotationMatrix2D(img_center, 90, 1)
        rotated = cv2.warpAffine(img, M, (cols, rows), borderValue=(255,255,255))

        show_picture("img", rotated, 0, "y")
        




    elif bas2 + 30 < haut2 and\
       bas1 + 20 < haut1:
        print("deux")


        b = 200 - bas1
        a = math.atan(b/200)
        c = math.degrees(a)
        print(c)

        rows = img.shape[0]
        cols = img.shape[1]
        img_center = (cols / 2, rows / 2)
        M = cv2.getRotationMatrix2D(img_center, -c, 1)
        rotated = cv2.warpAffine(img, M, (cols, rows), borderValue=(255,255,255))
        show_picture("img", rotated, 0, "y")



    else:
        print("normal")
        b = 200 - bas1
        a = math.atan(b/200)
        c = math.degrees(a)
        d = 90 - c
        print(d)



































