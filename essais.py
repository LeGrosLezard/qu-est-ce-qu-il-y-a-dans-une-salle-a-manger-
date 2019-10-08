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
    img = img[30:height, 0:width]

    return img


def parcours_image(img, model):

    clone = img.copy()
    size = 25

    for y in range(0, img.shape[0], size):
        for x in range(0, img.shape[1], size):


            crop = img[y:y+size*5, x:x+size*5]
            crop = cv2.resize(crop, (50, 50))
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

            #show_picture("crop", crop, 0, "y")

            try:
                (H, hogImage) = feature.hog(gray, orientations=9, pixels_per_cell=(10, 10),
                                            cells_per_block=(2, 2), transform_sqrt=True,
                                            block_norm="L1", visualize=True)

                pred = model.predict(H.reshape(1, -1))[0]
                if pred == 1:
                    cv2.rectangle(clone, (x, y), (x + size*5, y + size*5), (0, 0, 255), 2)
                else:
                    cv2.rectangle(clone, (x, y), (x + size, y + size), (0, 255, 0), 2)

                hogImage = exposure.rescale_intensity(hogImage, out_range=(0, 255))
                hogImage = hogImage.astype("uint8")
                #show_picture("crop", hogImage, 0, "y")

            except:
                pass

            

            show_picture("clone", clone, 1, "")
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






















