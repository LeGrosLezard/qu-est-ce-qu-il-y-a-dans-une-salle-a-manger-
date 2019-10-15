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


def main():


path_liste = r"C:\Users\jeanbaptiste\Desktop\assiette\program\test"
path_im = r"C:\Users\jeanbaptiste\Desktop\assiette\program\test/"

liste = os.listdir(path_liste)

for i in liste:
    i = path_im.format(str(i))
    print(i)

    img, copy = early_picture(i)
    copy = first_contour(img, copy)
    Xy_min, X_min, Xy_max, X_max = delimited_by_points(copy)

def early_picture(img):


    img = open_picture(i)
    img = cv2.resize(img, (200, 200))
    img = cv2.copyMakeBorder(img, 50, 50, 50, 50,
                             cv2.BORDER_CONSTANT, value=(255, 255, 255))

    copy = img.copy()


    return img, copy


def first_contour(img, copy):


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


    return copy


def delimited_by_points(copy):

    listex = []
    listey = []

    for y in range(copy.shape[1]):
        for x in range(copy.shape[0]):
            if copy[y, x][0] == 0 and\
               copy[y, x][1] == 0 and\
               copy[y, x][2] == 255: 
                listex.append(x)
                listey.append(y)



    Xy_min = min(listex)
    index_min = listex.index(min(listex))
    X_min = listey[index_min]

    Xy_max = max(listex)
    index_max = listex.index(max(listex))
    X_max = listey[index_max]

    print(Xy_min, X_min)
    print(Xy_max, X_max)


    return Xy_min, X_min, Xy_max, X_max


def normal_angle():
    print("noramle")

def 90_degrees(copy, Xy_min, X_min, Xy_max, X_max, img):

    print("90000")
    cv2.circle(copy, (Xy_min, X_min), 6, (0, 255, 0), 6)
    cv2.circle(copy, (Xy_max, X_max), 6, (255, 255, 0), 6)


    show_picture("copy", copy, 0, "y")


    rows = img.shape[0]
    cols = img.shape[1]
    img_center = (cols / 2, rows / 2)


    M = cv2.getRotationMatrix2D(img_center, -90, 1)
    rotated = cv2.warpAffine(copy, M, (cols, rows), borderValue=(255,255,255))

    show_picture("rotated", rotated, 0, "y")


def top_bot_first(Xy_min,X_min, Xy_max, X_max):

    print("yooo")
    c = math.atan(X_min/Xy_min)
    c = math.degrees(c)


    d = math.atan(X_max/Xy_max)
    d = math.degrees(d)
    print(d)

    
    c =  45- c - math.degrees(math.atan(X_max/Xy_max))
    print(c, "ANGLE")
    angle = c

    return angle


def top_bot_second(Xy_min,X_min, Xy_max, X_max):

    print("ici")
    copy = cv2.copyMakeBorder(copy, 50, 50, 50, 50,
                              cv2.BORDER_CONSTANT, value=(255, 255, 255))


    listex = []
    listey = []

    for y in range(copy.shape[1]):
        for x in range(copy.shape[0]):
            if copy[y, x][0] == 0 and\
               copy[y, x][1] == 0 and\
               copy[y, x][2] == 255: 
                listex.append(x)
                listey.append(y)



    Xy_min = min(listex)

    index_min = listex.index(min(listex))
    X_min = listey[index_min]

    Xy_max = max(listex)
    index_max = listex.index(max(listex))
    X_max = listey[index_max]


    show_picture("copy", copy, 0, "y")

    c = math.atan(X_min/Xy_min)
    c = math.degrees(c)


    d = math.atan(X_max/Xy_max)
    d = math.degrees(d)
    print(d)

    
    c =  45- c - math.degrees(math.atan(X_max/Xy_max))
    print(c, "ANGLE")
    angle = c

    return angle


def top_bot_third(angle, copy, Xy_min,X_min, Xy_max, X_max):

    #width
    cv2.circle(copy, (Xy_min, X_min), 6, (0, 255, 0), 6)
    cv2.circle(copy, (Xy_max, X_max), 6, (255, 255, 0), 6)

    print(X_min, Xy_min)
    print(X_max, Xy_max)

    show_picture("copy", copy, 0, "y")


    rows = img.shape[0]
    cols = img.shape[1]
    img_center = (cols / 2, rows / 2)

    M = cv2.getRotationMatrix2D(img_center, abs(c), 1)
    rotated = cv2.warpAffine(copy, M, (cols, rows), borderValue=(255,255,255))

    show_picture("rotated", rotated, 0, "y")

    print(angle)
    print("annnnnnnnnnnnnnnnnnnnnnnnnnnnnngle")
    if abs(angle) < 35 or abs(angle) > 45:

        c = 0
        go = True
        while go:

            listex = []
            listey = []

            for x in range(rotated.shape[0]):
                for y in range(rotated.shape[1]):
                    if rotated[x, y][0] == 0 and\
                       rotated[x, y][1] == 255 and\
                       rotated[x, y][2] == 0: 
                        x1 = x
                        y1 = y
                        break

                    if rotated[x, y][0] == 255 and\
                       rotated[x, y][1] == 255 and\
                       rotated[x, y][2] == 0:
                        x2 = x
                        y2 = y
                        break

            print("current data")
            print(x1, y1)
            print(x2, y2)
            print(abs(angle), "annnnnnngle°")
      
            print("oui")
            if abs(angle) < 35:
                M = cv2.getRotationMatrix2D(img_center, -c, 1)
                rotated = cv2.warpAffine(rotated, M, (cols, rows), borderValue=(255,255,255))

                if abs(y1 - y2) < 10:
                    go = False

            elif abs(angle) > 45:
                M = cv2.getRotationMatrix2D(img_center, c, 1)
                rotated = cv2.warpAffine(rotated, M, (cols, rows), borderValue=(255,255,255))

                if abs(y1 - y2) < 30:
                    go = False

            show_picture("rotated", rotated, 0, "y")
            print(c)
            c+=1

        show_picture("rotated", rotated, 0, "y")


def bot_top(angle, copy, Xy_min,X_min, Xy_max, X_max):


    print("laaaaaaaaaaaaa")
    c = math.atan(X_min/Xy_min)
    c = math.degrees(c)

    d = math.atan(X_max/Xy_max)
    d = math.degrees(d)
    print(d)

    c =  45- c - d
    print(c)
    angle = c
    


    #width
    cv2.circle(copy, (Xy_min, X_min), 6, (0, 255, 0), 6)
    cv2.circle(copy, (Xy_max, X_max), 6, (255, 255, 0), 6)

    print(X_min, Xy_min)
    print(X_max, Xy_max)

    show_picture("copy", copy, 0, "y")


    rows = img.shape[0]
    cols = img.shape[1]
    img_center = (cols / 2, rows / 2)


    M = cv2.getRotationMatrix2D(img_center, c, 1)
    rotated = cv2.warpAffine(copy, M, (cols, rows), borderValue=(255,255,255))

    show_picture("rotated", rotated, 0, "y")

    c = 0
    go = True
    while go:


        listex = []
        listey = []

        for x in range(rotated.shape[0]):
            for y in range(rotated.shape[1]):
                if rotated[x, y][0] == 0 and\
                   rotated[x, y][1] == 255 and\
                   rotated[x, y][2] == 0: 
                    x1 = x
                    y1 = y
                    #cv2.circle(rotated, (y, x), 6, (0, 0, 0), 6)

                    break


                if rotated[x, y][0] == 255 and\
                   rotated[x, y][1] == 255 and\
                   rotated[x, y][2] == 0:
                    #cv2.circle(rotated, (y, x), 6, (0, 0, 0), 6)
                    x2 = x
                    y2 = y
                    
                    break

        print("current data")
        print(x1, y1)
        print(x2, y2)

        if angle > - 45:
            M = cv2.getRotationMatrix2D(img_center, c, 1)
            rotated = cv2.warpAffine(rotated, M, (cols, rows), borderValue=(255,255,255))
        else:
           M = cv2.getRotationMatrix2D(img_center, -c, 1)
           rotated = cv2.warpAffine(rotated, M, (cols, rows), borderValue=(255,255,255)) 

        
    
        c+=1

        if abs(y1 - y2) < 10:
            go = False

    show_picture("rotated", rotated, 0, "y")



def define_rotation():

    if abs(X_min - X_max) < 10 and abs(Xy_min - Xy_max) < 100:
        normal_angle()

    elif abs(X_min - X_max) < 15:
        90_degrees(copy, Xy_min, X_min, Xy_max, X_max, img)

    elif Xy_min + 50 < Xy_max and abs(Xy_min - Xy_max) > 50 and X_min > X_max:
        
        print("unnnnnnnnnnnnnn")

        if Xy_min > 0 and X_min > 0:
            angle = top_bot_first(Xy_min,X_min, Xy_max, X_max)
            
        else:
            angle = top_bot_second(Xy_min,X_min, Xy_max, X_max)

        top_bot_third(angle, copy, Xy_min,X_min, Xy_max, X_max)
    

    elif abs(Xy_min - Xy_max) > 80 and X_min < X_max:
        bot_top(angle, copy, Xy_min,X_min, Xy_max, X_max)

    else:
        normal_angle()


