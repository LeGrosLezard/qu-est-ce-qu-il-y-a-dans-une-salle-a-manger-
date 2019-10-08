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
    img = cv2.imread(image)
    height, width, channel = img.shape

    return img


def reverse_img_by_pos(img, x, y, size):

    height, width, channel = img.shape

    reverse_x = False
    reverse_y = False
    
    if x >= width - size:
        reverse_x = True

    if y >= height/2:
        reverse_y = True


    if reverse_x is True:
        crop = img[y:y+size*5, x-size*5:x]

    if reverse_y is True:
        crop = img[y-size*5:y, x:x+size*5]

    if reverse_x is False and reverse_y is False:
        crop = img[y:y+size*5, x:x+size*5]

    return crop



def HOG_detection(gray):

    (H, hogImage) = feature.hog(gray, orientations=9, pixels_per_cell=(10, 10),
                                cells_per_block=(2, 2), transform_sqrt=True,
                                block_norm="L1", visualize=True)

    hogImage = exposure.rescale_intensity(hogImage, out_range=(0, 255))
    hogImage = hogImage.astype("uint8")

    return H, hogImage


def parcours_image(img, model):

    size = 25
    list_intersection = []
    img_detection = img.copy()

    for y in range(0, img.shape[0], size):
        for x in range(0, img.shape[1], size):

            clone = img.copy()

            crop = reverse_img_by_pos(img, x, y, size)

            crop = cv2.resize(crop, (50, 50))
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)


            try:

                H, hogImage = HOG_detection(gray)
                pred = model.predict(H.reshape(1, -1))[0]

                if pred == 1:

                    cv2.rectangle(img_detection, (x, y), (x + size*5, y + size*5), (0, 0, 255), 2)
                    list_intersection.append([x, y, x+w, y+h])
            except:
                pass

            cv2.rectangle(clone, (x, y), (x + size, y + size), (0, 255, 0), 2)
            show_picture("clone", clone, 1, "")
            show_picture("img_detection", img_detection, 1, "")
            time.sleep(0.3)




def show_picture(name, image, mode, destroy):
    cv2.imshow(name, image)
    cv2.waitKey(mode)
    if destroy == "y":
        cv2.destroyAllWindows()





if __name__ == "__main__":

    model = joblib.load("model/miammiamsvmImage")

    img = open_picture("assiette1.jpg")
    parcours_image(img, model)

