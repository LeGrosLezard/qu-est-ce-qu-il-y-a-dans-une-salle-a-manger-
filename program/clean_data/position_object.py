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


def draw_contours(contours, blanck):

    #recup center of detection and draw it in red
    position_circleX = []
    position_circleY = []

    for cnts in contours:
        if cv2.contourArea(cnts):
            
            cv2.drawContours(blanck, cnts, -1, (255, 255, 255), 1)
            
            M = cv2.moments(cnts)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            position_circleX.append(cX)
            position_circleY.append(cY)

            cv2.circle(blanck, (cX, cY), 6, (0, 0, 255), 6)


    return position_circleX, position_circleY



def recup_red_points(blanck):

    #recup red picture
    listex = []
    listey = []
    listex2 = []
    listey2 = []

    for y in range(blanck.shape[1]):
        for x in range(blanck.shape[0]):
            if blanck[y, x][0] == 0 and\
               blanck[y, x][1] == 0 and\
               blanck[y, x][2] == 255: 
                listex.append(x)
                listey.append(y)

            if blanck[x, y][0] == 0 and\
               blanck[x, y][1] == 0 and\
               blanck[x, y][2] == 255: 
                listex2.append(x)
                listey2.append(y)

    return listex, listey, listex2, listey2




def points_for_define_inclinaison(listex, listey, listex2, listey2, blanck):


    #take max (x, y) and min (x, y) on l and L
    X_min = min(listex)
    index_min = listex.index(min(listex))
    Xy_min = listey[index_min]

    X_max = max(listex)
    index_max = listex.index(max(listex))
    Xy_max = listey[index_max]

    X_min2 = min(listex2)
    index_min2 = listex2.index(min(listex2))
    Xy_min2 = listey2[index_min2]

    X_max2 = max(listex2)
    index_max2 = listex2.index(max(listex2))
    Xy_max2 = listey2[index_max2]


    #width
    cv2.circle(blanck, (X_min, Xy_min), 6, (0, 255, 0), 6)
    cv2.circle(blanck, (X_max, Xy_max), 6, (50, 255, 50), 6)

    #height
    cv2.circle(blanck, (Xy_min2, X_min2), 6, (255, 0, 255), 6)
    cv2.circle(blanck, (Xy_max2, X_max2), 6, (255, 255, 0), 6)


    #show_picture("blanck", blanck, 0, "")



    return X_min, Xy_min, X_max, Xy_max,\
           X_min2, Xy_min2, X_max2, Xy_max2, blanck




def treatment_inclinaison(X_min, Xy_min, X_max, Xy_max,
                          X_min2, Xy_min2, X_max2,
                          Xy_max2):

    out = 0

    #0)ok 1)horrizontal 2)bot/top 3)top/bot 

    if abs(Xy_min - Xy_max) < 5 and\
       abs(Xy_min2 - Xy_max2) < 15:
        out = 0

    elif abs(Xy_min - Xy_max) <= 5 and abs(Xy_min2 - Xy_max2) > 15:
        out = 1
    
    elif abs(X_min - X_max) > 80 and Xy_min > Xy_max:
        out = 2

    elif abs(X_min - X_max) > 80 and Xy_min < Xy_max:
        out = 3
        
    elif abs(Xy_min2 - Xy_max2) < 15:
        out = 0

    return out




def precise_angle(img, X_min, Xy_min, X_max, Xy_max,
                  X_min2, Xy_min2, X_max2, Xy_max2,
                  position, blanck,
                  path_clean, category, image):

    if position == 2:
        print("Search coordinates")

        b = 200 - X_min2
        a = math.atan(b/200)
        c = math.degrees(a)
        d = 90 - c

        rotated = imutils.rotate_bound(img, -d, borderValue=(255,255,255))
        #show_picture("img", rotated, 0, "y")
        cv2.imwrite(path_clean.format(category, image), rotated)

    if position == 3:
        print("Search coordinates")

        b = 200 - X_min2
        a = math.atan(b/200)
        c = math.degrees(a)
        d = 90 - c

        rotated = imutils.rotate_bound(img, d, borderValue=(255,255,255))
        #show_picture("img", rotated, 0, "y")
        cv2.imwrite(path_clean.format(category, image), rotated)

    if position == 1:
        print("seaching coordinates")
        rotated = imutils.rotate_bound(img, 90, borderValue=(255,255,255))
        #show_picture("img", rotated, 0, "y")
        cv2.imwrite(path_clean.format(category, image), rotated)




def position_rotation(contours, blanck, img,
                      path_clean, category, image):


    position_circleX, position_circleY = draw_contours(contours, blanck)

    listex, listey, listex2, listey2 = recup_red_points(blanck)

    X_min, Xy_min, X_max, Xy_max,\
    X_min2, Xy_min2, X_max2, Xy_max2, blanck\
    = points_for_define_inclinaison(listex, listey, listex2, listey2, blanck)

    position = treatment_inclinaison(X_min, Xy_min, X_max, Xy_max,
                                     X_min2, Xy_min2, X_max2, Xy_max2)

    precise_angle(img, X_min, Xy_min, X_max, Xy_max,
                  X_min2, Xy_min2, X_max2, Xy_max2,
                  position, blanck, path_clean,
                  category, image)



def transform_i(objects):
    out_objects = ""
    for i in objects:
        for j in i:
            if j in ("é", "è"):
               out_objects += "e"
            else:
                out_objects += j
      
    return out_objects



def pre_treatment(path_picture, objects, image):
    img = open_picture(path_picture.format(objects, image))

    height, width, channel = img.shape
    if height > 200 and width > 200:
        img = cv2.resize(img, (200, 200))

    blanck = blanck_picture(img)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(img, 100, 200)

    contours, _ = cv2.findContours(edged, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)



    return img, objects, contours, blanck




def take_features_position(objects_to_search):


    folder_clean = "dataset/clean/{}"
    path_clean = "dataset/clean/{}/{}"

    for objects in objects_to_search:

        objects = transform_i(objects)

        liste_obj = os.listdir(folder_clean.format(objects))

        for image in liste_obj:
            print(image)

            try:
                img, objects, contours, blanck =\
                pre_treatment(path_clean, objects, image)

                position_rotation(contours, blanck, img,
                                  path_clean, objects, image)
    
            except:
                pass

