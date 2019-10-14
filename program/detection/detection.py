import cv2
import os
import csv
import numpy as np

from skimage import exposure
from skimage import feature

import time
import joblib
import imutils



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
    
def reverse_img_by_pos(img, x, y, size):

    """ 
    We loop the picture x and y range.
    We ask a crop of the picture x to x + 25 * 3, same for y
    
    If we are at border of picture x - 25 * 3 to x
    """

    height, width, channel = img.shape
    reverse_x = False; reverse_y = False

    if x >= width/2:
        reverse_x = True

    if y >= height/2:
        reverse_y = True

    if reverse_x is True:
        crop = img[y:y+size*5, x-size*5:x]
        pts = (y, y+size*5, x-size*5, x)

    if reverse_y is True:
        crop = img[y-size*5:y, x:x+size*5]
        pts = (y-size*5, y, x, x+size*5)

    if reverse_x is False and reverse_y is False:
        crop = img[y:y+size*5, x:x+size*5]
        pts = (y, y+size*5, x, x+size*5)

    return crop, pts



def HOG_detection(gray):

    """We detect contour orientation gradient
    from color"""

    (H, hogImage) = feature.hog(gray, orientations=9,
                                pixels_per_cell=(10, 10),
                                cells_per_block=(2, 2),
                                transform_sqrt=True,
                                block_norm="L1", visualize=True)

    hogImage = exposure.rescale_intensity(hogImage, out_range=(0, 255))
    hogImage = hogImage.astype("uint8")

    return H, hogImage

def rotation_crop(crop):

    """
        Make a rotation of the
        current crop
    """
    
    for i in range(0, 360, 10):
        rotated = imutils.rotate_bound(crop, i)

                        
def parcours_image(img, model):

    """
        On veut juste les parties pour detecter ex un manche
        le crop pour vrai apprentissage => recup_data.py 
    """

    size = 15; list_intersection = [];prediction = [];
    img_detection = img.copy()

    for y in range(0, img.shape[0], size):
        for x in range(0, img.shape[1], size):

            clone = img.copy()

            try:

                crop, pts = reverse_img_by_pos(img, x, y, size)
                crop = cv2.resize(crop, (50, 50))
                gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

                #show_picture("gray", gray, 1, "")

                H, hogImage = HOG_detection(gray)
                #show_picture("hogImage", hogImage, 1, "")

                rotation_crop(hogImage)

                pred = model.predict(H.reshape(1, -1))[0]

                if pred == 1:
                    cv2.rectangle(img_detection, (pts[2], pts[0]),
                                  (pts[3], pts[1]), (0, 0, 255), 2)
                    prediction.append(pred)
                    list_intersection.append([pts[2], pts[0],
                                              pts[3], pts[1]])
            except:
                pass


##            cv2.rectangle(clone, (x, y), (x + size, y + size), (0, 255, 0), 2)
##            show_picture("clone", clone, 1, "")
##            show_picture("img_detection", img_detection, 1, "")


    return list_intersection, prediction



def reconstruction(image, liste, prediction, number_label, label):

    """We can have multiple detection so
    We make an average of this and recup the final detection
    We return this points"""

    a = 0; b = 0; c = 0; d = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    image_copy = image.copy()

    print(liste, prediction, number_label, label)

    if liste == []:
        return None
    else:

        #on regarde le label
        predicted = ""
        for i in range(len(number_label)):
            if number_label[i] == prediction[0]:
                predicted = label[i]

        #on fait un "include" de detection
        for i in liste:
            a += i[0]; b += i[1]
            c += i[2]; d += i[3]

        e = len(liste)

        #on dessine le "include"
        cv2.rectangle(image, (int(a/e), int(b/e)),
                      (int(c/e), int(d/e)),
                      (0, 0, 255), 1)

        show_picture("image", image, 0, "")

        image_copy = cv2.copyMakeBorder(image_copy, 50, 50, 50, 50,
                                  cv2.BORDER_CONSTANT, value=(255, 255, 255))


        cv2.putText(image_copy ,str(predicted), (int(a/e), int(b/e)),
                    font, 1, (200,0,0), 1, cv2.LINE_AA)

        show_picture("image_copy", image_copy, 0, "y")

        return str(predicted)



def detection_picture_hog(number_label, label, model, image):

    #load model
    model = joblib.load(model)

    #open img and copy it
    img = open_picture(image)
    img_copy = img.copy()
    

    list_intersection, prediction = parcours_image(img, model)

    detection = reconstruction(img, list_intersection,
                               prediction, number_label,
                               label)

    print(detection)
    return detection






