import os
import cv2
import math
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
    if mode == 1:
        time.sleep(3)
    if destroy == "y":
        cv2.destroyAllWindows()



def blanck_picture(img):
    """
        Create a black picture
    """

    blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
    blank_image[0:, 0:] = 0, 0, 0

    return blank_image


def find_contour(img):
    """
        Find all externals contours in picture
        create black empty picture
    """

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,250,255,cv2.THRESH_BINARY_INV)

    #show_picture("thresh", thresh, 0, "y")

    contours,h=cv2.findContours(thresh,cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    blanck = blanck_picture(img)

    return blanck, contours


def recup_object(img, blanck, contours,
                 name):
    """
        We detect contours
        for each objects in the scene
        we'll draw contour in green.
        We'll course the picture
        and display all object one by one
        unindisplay objects and just keep one
        for save it
    """

    c = 0 #for name save
    for cnt in contours:
        #delete litles contours
        if cv2.contourArea(cnt) > 500:

            #create ephemeral pictures
            blanck = blanck_picture(img)
            copy = img.copy()

            #fill the contour in green
            cv2.drawContours(blanck,[cnt],-1,(0,255,0),1)
            cv2.fillPoly(blanck, pts =[cnt], color=(0,255,0))
            #show_picture("ici", blanck, 0, "y")

            #superpose blanck and original image
            #if blanck is green pass else delete it with white
            for i in range(blanck.shape[0]):
                for j in range(blanck.shape[1]):
                    if blanck[i, j][0] == 0 and\
                       blanck[i, j][1] == 255 and\
                       blanck[i, j][2] == 0:
                        pass
                    else:
                        copy[i, j] = 255, 255, 255

            #decide to save or delete the copy !
            save(copy, name, c)

            c+=1

    return copy




def save(copy, name, counter):

    gray = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)

    #show_picture("thresh", thresh, 0, "y")

    contours,h=cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)

    for cnts in contours:

        new_name = str(name[:-4]) + "v" + str(counter) + ".jpg"
        #show_picture(str(new_name), copy, 1, "y")
        cv2.imwrite(new_name, copy)
        os.remove(name)



def take_features_multi_obj(img):
    """
        We open picture
        We resize picture
        We found the contours
        We try to detect objects by objects
    """


    try:
        name = str(img)

        img = open_picture(img)
        img = cv2.resize(img, (200, 200))

        #show_picture("img", img, 0, "")

        blanck, contours = find_contour(img)
        copy = recup_object(img, blanck, contours,
                            name)
        return copy
    except:
        pass





#take_features_multi_obj(r"C:\Users\jeanbaptiste\Desktop\assiette\program\dataset\assiette_couvert\assiette1.jpg")





