
import numpy as np
import cv2
import os
import imutils
import math
from PIL import Image





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
            if key != (0, 255, 0):
                max_value = value
                color = key

    return color


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



def contours_square(img):


    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _,thresh = cv2.threshold(gray,250,255,cv2.THRESH_BINARY_INV)
    show_picture("thresh", thresh, 0, "y")


    contours,h=cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


    for cnt in contours:
        perimetre=cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,0.01*perimetre,True)

        try:
            M = cv2.moments(cnt)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.drawContours(img,[cnt],-1,(0,255,0),2)
        except:
            pass


    if len(approx)==4:
        (x, y, w, h) = cv2.boundingRect(approx)
        ratio = w / float(h)
        if ratio >= 0.95 and ratio <= 1.05:
            shape = "carre"
        else:
            shape = "rectangle"


        print(shape)

    
        show_picture("img", img, 0, "y")
        
        crop = img[y:y+h, x:x+w]
        show_picture("crop", crop, 0, "y")
        color = main_color_background(crop)

        print(color)
        for i in range(crop.shape[0]):
            for j in range(crop.shape[1]):
                if crop[i, j][0] > color[0] - 40 and\
                   crop[i, j][0] < color[0] + 40 and\
                   crop[i, j][1] > color[1] - 40 and\
                   crop[i, j][1] < color[1] + 40 and\
                   crop[i, j][2] > color[1] - 40 and\
                   crop[i, j][2] < color[2] + 40:
                    crop[i, j] = 255, 255, 255


        show_picture("crop", crop, 0, "y")





liste = os.listdir("test/")
for i in liste:
    i = str("test/") + str(i)

    img = open_picture(i)
    
    color = main_color_background(img)

    print(color)

    show_picture("img", img, 0, "y")
    contours_square(img)
























