import os
import cv2
import math
import time
import imutils
import numpy as np
from PIL import Image



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
    if destroy == "y":
        cv2.destroyAllWindows()

def blanck_picture(img):
    """
        Create a black empty picture
    """

    blank_image = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    blank_image[0:, 0:] = 0, 0, 0

    return blank_image




def rotation(img, degrees):
    """
        Rotation of the picture via his center
    """
    
    rows = img.shape[0]
    cols = img.shape[1]

    img_center = (cols / 2, rows / 2)
    M = cv2.getRotationMatrix2D(img_center, degrees, 1)

    #Rotate picture with white border
    rotated = cv2.warpAffine(img, M, (cols, rows), borderValue=(255,255,255))
    #show_picture("rotated", rotated, 0, "y")

    return rotated



def run_a_picture(img, color, mode):

    """
        Course a picture and try to detect
        a kind of pixel.

        Two mods:
            - List for recup all points
            - Points for recup last points
    """

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
                    pts1 = x; pts2 = y;
                    return pts1, pts2



def find_points(listex, listey):
    """
        Recup points from list
        for have the max y and min y of
        our object.
    """

    
    #min coordinates x, y
    Xy_min = min(listex)
    X_min = listey[listex.index(min(listex))]

    #max coordinates x, y
    Xy_max = max(listex)
    X_max = listey[listex.index(max(listex))]

    print(Xy_min, X_min)
    print(Xy_max, X_max)

    return X_min, Xy_min, X_max, Xy_max



def angle_function(X_min, Xy_min, X_max, Xy_max):
    """
        We need to define angle of the object
        for re calculate his rotation.
    """

    #Try to search arctangeante.
    angle = math.degrees(math.atan(X_min/Xy_min))
    #Try to search arctangeante of the second.
    second_angle = math.degrees(math.atan(X_max/Xy_max))
    #half frame - current angle - second why don't remember
    #but wasn't oups
    angle =  45 - angle - second_angle

    return angle




def parameters_rotation(y1, y2, last, ok, angle, go,
                        cnter, number1, number2):

    """
        We have rotate our object,
        now we want a perfect position
        and ask programm to rotate agin
        object. If Max and min points are align
        stop.
        It'll try on a direction if absolute
        max points - min points
        become taller to taller stop and
        try on the opposite sens
    """

    if abs(y1 - y2) > last:
        if ok == 0:
            angle = number1
            ok +=1
        else:
            angle = number2

    if abs(y1 - y2) == last:
        cnter += 1
    else:
        cnter = 0

    if cnter == 3:
        go = False
    elif cnter != 3:
        go = True

    return angle, ok, cnter, go







def early_picture(img):
    """
        Make the basics operations for next
    """

    #open picture and resize it
    img = cv2.resize(open_picture, (200, 200))
    #add white border
    img = cv2.copyMakeBorder(img, 50, 50, 50, 50,
                             cv2.BORDER_CONSTANT, value=(255, 255, 255))
    #make a copy for work on it
    copy = img.copy()
    #make a copy for final
    img_final = img.copy()

    return img, copy, img_final



def first_contour(img, copy):
    """
        Search the max contour
    """

    #one channel
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #binarized it
    _,thresh = cv2.threshold(gray,250,255,cv2.THRESH_BINARY_INV)
    #show_picture("thresh", thresh, 0, "y")

    #All contours + all points
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
    """
        Define max and min points of object
        like the head and the foot
    """

    #recuperate list of points corresponding to green pixel (our contours)
    listex, listey = run_a_picture(copy, (0, 0, 255), "liste")
    #Find max and min points of object
    X_min, Xy_min, X_max, Xy_max = find_points(listex, listey)

    return X_min, Xy_min, X_max, Xy_max



def normal_angle(img):
    """
        No treatment of this picture,
        it has a normal positionning top to bot
    """

    #print("noramle")
    #show_picture("img", img, 0, "y")
    return img



def nine_degrees(copy, X_min, Xy_min, X_max, Xy_max, img,
                 img_final):
    """
        Picture is leaning horizontally.
        We make a rotation of 90 degrees
    """

    cv2.circle(copy, (Xy_min, X_min), 6, (0, 255, 0), 6)
    cv2.circle(copy, (Xy_max, X_max), 6, (255, 255, 0), 6)
    #show_picture("copy", copy, 0, "y")

    rotated = rotation(img, -90)
    img_final = rotation(img_final, -90)
    #show_picture("img_final", img_final, 0, "y")

    return img_final


def top_bot_first(X_min, Xy_min, X_max, Xy_max, img):
    """
        Picture is oritente top to bot,
        lifted to the right side
        leaning to the left side.
    """

    #calcul how many do we rotate picture from his
    #current angle
    angle = angle_function(X_min, Xy_min, X_max, Xy_max)

    return angle



def top_bot_second(Xy_min,X_min, Xy_max, X_max, img):
    """
        Picture is oritente top to bot,
        lifted to the right side
        leaning to the left side.
        But border of object are glue to the borders.
    """

    #make white border before rotation
    #because picture can cut part of object
    copy = cv2.copyMakeBorder(copy, 50, 50, 50, 50,
                              cv2.BORDER_CONSTANT, value=(255, 255, 255))

    #recup all greens points 
    listex, listey = run_a_picture(copy, (0, 0, 255), "liste")
    #recup this points
    X_min, Xy_min, X_max, Xy_max = find_points(listex, listey)
    #show_picture("copy", copy, 0, "y")

    #
    angle = angle_function(X_min, Xy_min, X_max, Xy_max)



    return angle





def top_bot_third(angle, copy, X_min, Xy_min, X_max, Xy_max,
                  img, img_final):

    """
        Draw points for visual,
        Make rotation,
    """

    cv2.circle(copy, (Xy_min, X_min), 6, (0, 255, 0), 6)
    cv2.circle(copy, (Xy_max, X_max), 6, (255, 255, 0), 6)
    #show_picture("copy", copy, 0, "y")

    rotated = rotation(copy, abs(angle))
    img_final = rotation(img_final, abs(angle))
    #show_picture("rotated", rotated, 0, "y")

    last = 0 ;c = 0;go = True;cnter = 0;ok = 0;

    #While max and min points aren't aligned do it
    while go:

        try:
            #search last points of the object
            x1, y1 = run_a_picture(rotated, (0, 255, 0), "points")
            x2, y2 = run_a_picture(rotated, (255, 255, 0), "points")
        except:
            go = False

        #We try in a sens to decrease distance
        #beetween head and foot of object.
        #It increases ? try in the other sens.
        angle, ok, cnter, go = \
        parameters_rotation(y1, y2, last, ok, angle,
                            go, cnter, 46, 0)

        if abs(angle) > 45:
            rotated = rotation(rotated, -c)
            img_final = rotation(img_final, -c)

            if abs(y1 - y2) < 10:
                go = False

        elif abs(angle) < 35:
            rotated = rotation(rotated, c)
            img_final = rotation(img_final, c)

            if abs(y1 - y2) < 30:
                go = False

        last = abs(y1 - y2)

        c+=1

    #show_picture("rotated", rotated, 0, "y")
    #show_picture("img_final", img_final, 0, "y")
    return img_final




def define_rotation(X_min, Xy_min, X_max, Xy_max,
                    copy, img, img_final, picture):

    """
        All conditions.
        1) normal position
        5) normal position
        2) leaning horizontally
        3) right lifted left down
        4) left lifted right down
    """

    #1
    if abs(X_min - X_max) <= 15 and abs(Xy_min - Xy_max) < 100:
        img_final = normal_angle(img)

    #2
    elif abs(X_min - X_max) < 15:
        img_final = nine_degrees(copy, X_min, Xy_min, X_max, Xy_max,
                                 img, img_final)

    #3
    elif Xy_min + 50 < Xy_max and abs(Xy_min - Xy_max) > 50 and X_min > X_max:

        if Xy_min > 0 and X_min > 0:
            angle = top_bot_first(X_min, Xy_min, X_max, Xy_max, img)
            
        else:
            angle = top_bot_second(X_min, Xy_min, X_max, Xy_max, img)

        img_final = top_bot_third(angle, copy, X_min, Xy_min, X_max, Xy_max,
                                  img, img_final)
    
    #4
    elif abs(Xy_min - Xy_max) > 80 and X_min < X_max:
        img_final = bot_top(copy, X_min, Xy_min, X_max, Xy_max,
                            img, img_final)
    #5
    else:
        img_final = normal_angle(img)

    #show_picture("img_final", img_final, 0, "y")
    cv2.imwrite(picture, img_final)




def take_features_position(picture):

    print(picture)

    #Make copies and make a border
    img, copy, img_final = early_picture(picture)
    #Find contour
    copy = first_contour(img, copy)
    #Find the header and the footer of the object
    X_min, Xy_min, X_max, Xy_max = delimited_by_points(copy)
    #Find the best, ok rotation !
    define_rotation(X_min, Xy_min, X_max, Xy_max,
                    copy, img, img_final, str(picture))
