import numpy as np
import cv2
import os
import imutils
import math
from PIL import Image
from skimage import exposure
from skimage import feature




def open_picture(image):
    """We open picture"""

    img = cv2.imread(image)
    return img



def show_picture(name, image, mode, destroy):
    cv2.imshow(name, image)
    cv2.waitKey(mode)
    if mode == 1:
        time.sleep(0.2)
    if destroy == "y":
        cv2.destroyAllWindows()
    

def save_picture(name, image):
    path = "dataset/data_analysing/{}"
    cv2.imwrite(path.format(str(name)), image)


def blanck_picture(img):

    """Create a black background picture same dimension of original picture"""

    blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
    blank_image[0:img.shape[0], 0:img.shape[1]] = 0, 0, 0

    return blank_image









def make_contours(img, blanck):
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,250,255,cv2.THRESH_BINARY_INV)

    contours,h=cv2.findContours(thresh,cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

    for i in contours:
        if cv2.contourArea(i) > 200:
            cv2.fillPoly(blanck, pts =[i], color=(0,255,0))

    show_picture("blanck", blanck, 0, "y")


    return blanck


def object_contours_size(blanck):

    cnts_points = []
    for i in range(blanck.shape[0]):
        c = 0
        for j in range(blanck.shape[1]):
            if blanck[i, j][0] == 0 and\
               blanck[i, j][1] == 255 and\
               blanck[i, j][2] == 0:
               c += 1

        if c == 0:
            pass
        else:
            cnts_points.append(c)


    mean = sum(cnts_points) / len(cnts_points)

    points = []
    for nb, i in enumerate(cnts_points):
        if i > mean + 6:
            points.append(nb)

    return points




def take_max_size(points, img):

    ok = 0; nan = False;

    for i in range(len(points)):
        try:
            if points[i] + 1 == points[i+1] and nan is False:
                ok = points[i]
                nan = True
            else:
                nan = False
                cv2.rectangle(img, (0, ok),
                              (img.shape[0], points[i]),
                              (0,0,255), 30)
                ok = 0
        except:
            pass

 
    show_picture("img", img, 0, "y")
    return img




def draw_part_picture(img, copy):
    
    blanck1 = blanck_picture(img)
    blanck2 = blanck_picture(img)

    maxi = 0
    c = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j][0] == 0 and\
               img[i, j][1] == 0 and\
               img[i, j][2] == 255:
                blanck1[i, j] = copy[i, j]

            else:
                blanck2[i, j] = copy[i, j]

    show_picture("blanck1", blanck1, 0, "y")
    show_picture("blanck2", blanck2, 0, "y")

    return blanck1, blanck2


def full_white(img):

    full = img.shape[0] * img.shape[1]

    c = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j][0] == 0 and\
               img[i, j][1] == 255 and\
               img[i, j][2] == 0:
                c+=1

    print(c, full)
    if c > 8500:
        return False
    else:
        return True
    

def final_part(blanck):

    gray = cv2.cvtColor(blanck, cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY)

    contours,h=cv2.findContours(thresh,cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    maxi = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > maxi:
            maxi = cv2.contourArea(cnt)

    for cnt in contours:
        if cv2.contourArea(cnt) != maxi:
            cv2.fillPoly(blanck, pts =[cnt], color=(0,0,0))

    return blanck




def main_comparaison(img):

    img = open_picture(img)
    img = cv2.resize(img, (50, 200))

    copy = img.copy()

    blanck = blanck_picture(img)
    blanck = make_contours(img, blanck)
    ocontinuer = full_white(blanck)

    if ocontinuer is True:

        points = object_contours_size(blanck)

        img = take_max_size(points, img)

        blanck1, blanck2 = draw_part_picture(img, copy)

        blanck1 = final_part(blanck1)
        blanck2 = final_part(blanck2)




objects_to_search = ['Fourchette', 'Couteau', 'Fourchette']
for objects in objects_to_search:

    liste = os.listdir("../dataset/clean/" + str(objects))
    for picture in liste:
        picture = str("../dataset/clean/") + str(objects) + "/" + str(picture)
        main_comparaison(picture)







