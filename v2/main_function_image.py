import os
import cv2
import time
import numpy as np

def open_picture(image):
    """We open picture"""

    img = cv2.imread(image)
    return img

def show_picture(name, image, mode, destroy):
    """
        Show picture
        mode 0 = entrance key  pass to next
        mode y = destroy windows
    """
    
    cv2.imshow(name, image)
    cv2.waitKey(mode)
    if mode == 1:
        time.sleep(1)
        cv2.destroyAllWindows()
    if destroy == "y":
        cv2.destroyAllWindows()

def save_picture(name, picture):
    cv2.imwrite(name, picture)


def blanck_picture(img):
    """
        Create a black picture
    """

    blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
    blank_image[0:, 0:] = 0, 0, 0

    return blank_image


def to_crop(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,250,255,cv2.THRESH_BINARY_INV)

    contours,h=cv2.findContours(thresh,cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)

    maxi = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > maxi:
            maxi = cv2.contourArea(cnt)

    for cnt in contours:
        if cv2.contourArea(cnt) == maxi:
            maxi = cv2.contourArea(cnt)
            x, y, w, h = cv2.boundingRect(cnt)

    img = img[y:y+h, x:x+w]

    return img, int(x+w/2), y


def write_position(positionx, positiony, name):

    positionx = str(positionx)
    positiony = str(positiony)
    name = str(name)
    
    path = "dataset/information_data/current/position.py"
    with open(path, "a") as file:
        to_write = positionx + "," + positiony + ";" + name + "\n"
        file.write(to_write)


def recup_position(name):

    path = "dataset/information_data/current/position.py"

    
    liste = []
    with open(path, "r") as file:
        for i in file:
            increment = ""
            for j in i:
                if j == ";" or j == "\n":
                    liste.append(increment)
                    increment = ""
                else:
                    increment += j


    coordinate = []
    liste_w = []
    for nb, i in enumerate(liste):
        if nb % 2 == 0:
            coordinate.append(liste_w)
            liste_w = []

        liste_w.append(i)

    coordinate.append(liste_w)

    for i in coordinate:
        if i != []:
            if i[1] == name:
                return i[0]




def draw(detection):

    if detection[0] == "": detection[0] = "In searching"
    name = detection[0]; x = 0; y = 0;
    increment = "";

    for detec in detection[1]:
        for d in detec:
            if d == ",":
                x = int(increment)
                increment = ""
            else:
                increment += d

    y = int(increment)


    path = "dataset/image/current/current.jpg"
    img = open_picture(path)
    img = cv2.resize(img, (200, 200))
    img = cv2.copyMakeBorder(img, 200, 200, 200, 200,
                             cv2.BORDER_CONSTANT, value=(177, 151, 151))



    cv2.circle(img, (x + 200, y + 200), 3, (0,0,255), 3)
    cv2.line(img, (x + 150, y + 100), (x + 200, y + 200), (255,0,0), 3)
    cv2.putText(img, name, (x + 100, y + 95), cv2.FONT_HERSHEY_SIMPLEX,
                1.0, (0, 0, 255), lineType=cv2.LINE_AA) 

    return img

