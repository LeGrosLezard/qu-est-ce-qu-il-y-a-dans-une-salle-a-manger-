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


#multi
def multiple_objects(contours, blanck, img, path_clean, category):

    show_picture("image", img, 0, "y")
    

    detection = 0
    stop = True

    last_w_object = 0
    
    for cnts in contours:
        if cv2.contourArea(cnts) > 1:
            
            x, y, w, h = cv2.boundingRect(cnts)
            if h > 20 and w > 5:
            
                if last_w_object > x+w and last_w_object != 0:
                    cv2.rectangle(blanck, (x, y), (x+w, y+h), (0, 0, 255), 1)
                    detection += 1

                last_w_object = x+w

    if detection >= 4:
        print("multiple objects")
    else:
        pass
        #cv2.imwrite(path_clean.format(str(category), str(img)), img)
    show_picture("blanck", blanck, 0, "y")



def rectangle_more_one_object(contours):
    """Here we want separate in case multiple objects by area detection"""

    positionX = []; positionY = []; positionW = []; positionH = [];
    for cnts in contours:
        if cv2.contourArea(cnts) == maxi1 or\
           cv2.contourArea(cnts) == maxi2 or\
           cv2.contourArea(cnts) == maxi3:
            x, y, w, h = cv2.boundingRect(cnts)

            positionX.append(x); positionY.append(y);
            positionW.append(x+w); positionH.append(y+h);

            x, y, w, h = cv2.boundingRect(cnts)
            cv2.drawContours(blanck, cnts, -1, (255, 255, 255), 1)
            cv2.rectangle(blanck, (x, y), (x+w, y+h), (0, 0, 255), 3)
            

    for i in range(len(positionX)):
        print(positionX[i], positionY[i], positionW[i], positionH[i])













    
