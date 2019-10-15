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




def rotation(img, degrees):

    rows = img.shape[0]
    cols = img.shape[1]

    img_center = (cols / 2, rows / 2)
    M = cv2.getRotationMatrix2D(img_center, degrees, 1) #-90
    rotated = cv2.warpAffine(img, M, (cols, rows), borderValue=(255,255,255))
    show_picture("rotated", rotated, 0, "y")


    return rotated



def run_a_picture(img, color, mode):

    listex = []; listey = []

    if mode is "liste":

        for y in range(img.shape[1]):
            for x in range(img.shape[0]):
                if img[y, x][0] == color[0] and\
                   img[y, x][1] == color[1] and\
                   img[y, x][2] == color[2]: 
                    listex.append(x)
                    listey.append(y)


        return listex, listey

    elif mode is "points":

        pts1 = 0; pts2 = 0;

        for x in range(img.shape[0]):
            for y in range(img.shape[1]):
                if img[x, y][0] == color[0] and\
                   img[x, y][1] == color[1] and\
                   img[x, y][2] == color[2]: 
                    pts1 = x
                    pts2 = y

                    return pts1, pts2



def find_points(listex, listey):

    Xy_min = min(listex)
    X_min = listey[listex.index(min(listex))]

    Xy_max = max(listex)
    X_max = listey[listex.index(max(listex))]

    print(Xy_min, X_min)
    print(Xy_max, X_max)

    return X_min, Xy_min, X_max, Xy_max





def angle_function(X_min, Xy_min, X_max, Xy_max):

    angle = math.degrees(math.atan(X_min/Xy_min))
    second_angle = math.degrees(math.atan(X_max/Xy_max))
    angle =  45 - angle - second_angle

    return angle










def early_picture(img):


    img = open_picture(img)
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

    listex, listey = run_a_picture(copy, (0, 0, 255), "liste")
    X_min, Xy_min, X_max, Xy_max = find_points(listex, listey)

    return X_min, Xy_min, X_max, Xy_max


def normal_angle():
    print("noramle")



def nine_degrees(copy, X_min, Xy_min, X_max, Xy_max, img):

    print("90")
    cv2.circle(copy, (Xy_min, X_min), 6, (0, 255, 0), 6)
    cv2.circle(copy, (Xy_max, X_max), 6, (255, 255, 0), 6)

    show_picture("copy", copy, 0, "y")

    rotated = rotation(img, -90)



def top_bot_first(X_min, Xy_min, X_max, Xy_max, img):

    print("yooo")

    angle = angle_function(X_min, Xy_min, X_max, Xy_max)

    return angle




def top_bot_second(Xy_min,X_min, Xy_max, X_max, img):

    print("ici")
    copy = cv2.copyMakeBorder(copy, 50, 50, 50, 50,
                              cv2.BORDER_CONSTANT, value=(255, 255, 255))

    listex, listey = run_a_picture(copy, (0, 0, 255), "liste")

    X_min, Xy_min, X_max, Xy_max = find_points(listex, listey)

    show_picture("copy", copy, 0, "y")

    angle = angle_function(X_min, Xy_min, X_max, Xy_max)
    print(angle, "ANGLE")


    return angle




def top_bot_third(angle, copy, X_min, Xy_min, X_max, Xy_max, img):

    #width
    cv2.circle(copy, (Xy_min, X_min), 6, (0, 255, 0), 6)
    cv2.circle(copy, (Xy_max, X_max), 6, (255, 255, 0), 6)

    print(X_min, Xy_min)
    print(X_max, Xy_max)

    show_picture("copy", copy, 0, "y")

    rotated = rotation(copy, abs(angle))


    show_picture("rotated", rotated, 0, "y")

    print(angle)
    print("annnnnnnnnnnnnnnnnnnnnnnnnnnnnngle")
    if abs(angle) < 35 or abs(angle) > 45:

        c = 0
        go = True
        while go:


            x1, y1 = run_a_picture(rotated, (0, 255, 0), "points")
            x2, y2 = run_a_picture(rotated, (255, 255, 0), "points")

            print("current data")
            print(x1, y1)
            print(x2, y2)
            print(abs(angle), "annnnnnngle°")
      
            print("oui")
            if abs(angle) < 35:

                rotated = rotation(rotated, -c)
                if abs(y1 - y2) < 10:
                    go = False

            elif abs(angle) > 45:
                rotated = rotation(rotated, c)
                if abs(y1 - y2) < 30:
                    go = False

            print(c)
            c+=1


        show_picture("rotated", rotated, 0, "y")



def bot_top(copy, X_min, Xy_min, X_max, Xy_max, img):


    print("laaaaaaaaaaaaa")
    angle = angle_function(X_min, Xy_min, X_max, Xy_max)


    cv2.circle(copy, (Xy_min, X_min), 6, (0, 255, 0), 6)
    cv2.circle(copy, (Xy_max, X_max), 6, (255, 255, 0), 6)

    print(X_min, Xy_min)
    print(X_max, Xy_max)

    show_picture("copy", copy, 0, "y")

    rotated = rotation(copy, angle)

    c = 0
    go = True
    while go:

        x1, y1 = run_a_picture(rotated, (0, 255, 0), "points")
        x2, y2 = run_a_picture(rotated, (255, 255, 0), "points")

        print("current data")
        print(x1, y1)
        print(x2, y2)

        if angle > - 45:
            rotated = rotation(rotated, c)
        else:
           rotated = rotation(rotated, -c)

        c+=1

        if abs(y1 - y2) < 10:
            go = False

    show_picture("rotated", rotated, 0, "y")


     
def define_rotation(X_min, Xy_min, X_max, Xy_max, copy, img):

    if abs(X_min - X_max) < 10 and abs(Xy_min - Xy_max) < 100:
        normal_angle()

    elif abs(X_min - X_max) < 15:
        nine_degrees(copy, X_min, Xy_min, X_max, Xy_max, img)

    elif Xy_min + 50 < Xy_max and abs(Xy_min - Xy_max) > 50 and X_min > X_max:
        

        if Xy_min > 0 and X_min > 0:
            angle = top_bot_first(X_min, Xy_min, X_max, Xy_max, img)
            
        else:
            angle = top_bot_second(X_min, Xy_min, X_max, Xy_max, img)

        top_bot_third(angle, copy, X_min, Xy_min, X_max, Xy_max, img)
    

    elif abs(Xy_min - Xy_max) > 80 and X_min < X_max:
        bot_top(copy, X_min, Xy_min, X_max, Xy_max, img)

    else:
        normal_angle()



def main():

    path_liste = r"C:\Users\jeanbaptiste\Desktop\assiette\program\test"
    path_im = r"C:\Users\jeanbaptiste\Desktop\assiette\program\test/{}"

    liste = os.listdir(path_liste)

    for i in liste:
        i = path_im.format(str(i))
        print(i)

        img, copy = early_picture(i)
        copy = first_contour(img, copy)
        X_min, Xy_min, X_max, Xy_max = delimited_by_points(copy)
        
        define_rotation(X_min, Xy_min, X_max, Xy_max, copy, img)


main()













