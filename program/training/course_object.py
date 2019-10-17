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
        time.sleep(0.2)
    if destroy == "y":
        cv2.destroyAllWindows()
    


def blanck_picture(img):

    """Create a black background picture same dimension of original picture"""

    blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
    blank_image[0:img.shape[0], 0:img.shape[1]] = 0, 0, 0

    return blank_image


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







from training.to_csv import write_data_into_csv
def main_couse(img, csv_name, label):

    print(label)

    img = open_picture(img)
    img = cv2.resize(img, (50, 200))

    size = 50
    
    print("scanning...")

    copy = img.copy()

    for y in range(0, img.shape[0], size):
        for x in range(0, img.shape[1], size):


            crop_clone = img[y:y+size, x:x+size]
            H, hogImage = HOG_detection(crop_clone)
            #show_picture("dzad", hogImage, 0, "")
                
            c = 0
            for i in range(hogImage.shape[0]):
                for j in range(hogImage.shape[1]):
                    if hogImage[i, j] == 0:
                        c+=1

            if hogImage.shape[0] * hogImage.shape[1] == c:
                pass
            else:
                write_data_into_csv(csv_name, label, H)




##
##objects_to_search = ["Fourchette", 'Cuillere', 'Couteau', 'Fourchette']
##for objects in objects_to_search:
##    
##    liste = os.listdir("../dataset/clean/" + str(objects))
##
##    for picture in liste[1:]:
##        picture = str("../dataset/clean/") + str(objects) + "/" + str(picture)    
##        print(picture)
##        main_couse(picture, "_in_training.csv", 0)





