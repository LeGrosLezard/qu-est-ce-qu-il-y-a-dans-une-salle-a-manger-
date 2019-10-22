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





def recup_label_position(detection):
    
    if detection[0] == "": detection[0] = "?"
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

    return name, x, y


def picture_treatment(image, nb):
    img1 = open_picture(image)
    img1 = cv2.resize(img1, (50, 100))

    if nb == 0:
        path = "dataset/image/current/current.jpg";
    if nb > 0:
        path = "dataset/image/current/current_copy.jpg";

    img = open_picture(path)


    if nb == 0:
        img = cv2.resize(img, (200, 200))
        img = cv2.copyMakeBorder(img, 200, 200, 200, 200,
                                 cv2.BORDER_CONSTANT, value=(177, 151, 151))




    return img1, img




def draw(detection, nb, image):


    img1, img = picture_treatment(image, nb)
    name, x, y = recup_label_position(detection)
    #We add border to picture
    #We course the picture
    #if coursing == on the picture
    #pass
    #We verify slot.
    #If slot or c == 0:
    #empty slot
    #else
    #picture already on it
    for j in range(0, img.shape[0], img1.shape[0]):
        for i in range(0, img.shape[1], img1.shape[1]):
            if j >= 100 and j <= 380 and i >= 100 and i <= 450:
                pass

            else:
                c = 0
                for jj in range(j, j + img1.shape[0]):
                    for ii in range(i, i + img1.shape[1]): 
                        if img[jj, ii][0] != 177 and\
                           img[jj, ii][1] != 151 and\
                           img[jj, ii][2] != 151:
                            c += 1

                if c == 0:

                    img[j:j + img1.shape[0], i:i + img1.shape[1]] = img1

                    cv2.line(img, (i+ img1.shape[1], j+ img1.shape[0]),
                             (x + 200, y + 200), (0, 0, 0), 2)

                    cv2.putText(img, name, (i,j+img1.shape[0]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255))

                    return img


