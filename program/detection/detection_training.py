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



def detection_training(img, model_name, model_name1, model_name2, model_name3):

    model = joblib.load(model_name)
##    model1 = joblib.load(model_name1)
##    model2 = joblib.load(model_name2)
    #model3 = joblib.load(model_name3)

    img = open_picture(img)
    img = cv2.resize(img, (50, 200))
    size = 50



    for y in range(0, img.shape[0], size):
        for x in range(0, img.shape[1], size):

            copy = img.copy()
            cv2.rectangle(copy, (x, y), (x+size, y + size), (0,0,255) ,3)
            crop_clone = img[y:y+size, x:x+size]
            H, hogImage = HOG_detection(crop_clone)

            pred = model.predict(H.reshape(1, -1))[0]
##            pred1 = model1.predict(H.reshape(1, -1))[0]
##            pred2 = model2.predict(H.reshape(1, -1))[0]
            #pred3 = model3.predict(H.reshape(1, -1))[0]


            pred1 = ""; pred2="";pred3="";
            pred3="";
            
            print("cuillere", pred, "couteau", pred1,
                  "fourchette", pred2, "final", pred3)


            show_picture("copy", copy, 0, "")
            show_picture("dzad", hogImage, 0, "")
            
            

            







objects_to_search = ["Cuillere", 'Cuillere', 'Couteau', 'Fourchette']


model_name = "../models/_in_training"
##model_name1 = "../models/_in_training0"
##model_name2 = "../models/_in_training01"
##model_name3 = "../models/knn_les_trois"

for objects in objects_to_search:
    
    liste = os.listdir("../dataset/clean/" + str(objects))

    for picture in liste:
        picture = str("../dataset/clean/") + str(objects) + "/" + str(picture)
        detection_training(picture, model_name,
                           "", "", "")























