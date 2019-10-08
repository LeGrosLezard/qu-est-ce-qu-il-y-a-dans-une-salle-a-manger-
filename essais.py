import cv2
import os
import csv
import numpy as np
from skimage import exposure
from skimage import feature

import joblib

import imutils


def to_list(thresh):

    data = []
    for i in range(thresh.shape[0]):
        for j in range(thresh.shape[1]):
            if thresh[i, j] > 120:
                nb = 1
            else:
                nb = 0
        
            data.append(nb)

    return data

##liste = os.listdir(r"C:\Users\jeanbaptiste\Desktop\assiette\image\assiette")
##path  = "image/assiette/{}"

liste = os.listdir(r"C:\Users\jeanbaptiste\Desktop\assiette\image\assiette_couvert")
path  = "image/assiette_couvert/{}"


model = joblib.load("model/miammiam_model")
model1 = joblib.load("model/miammiam_model8")


for image in liste:

    print(image)
    

    img = cv2.imread(path.format(image))


    blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
    blank_image[0:img.shape[0], 0:img.shape[1]] = 0, 0, 0


    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 100, 200)


    for y in range(0, img.shape[0], 50):
        for x in range(0, img.shape[1], 50):

            crop_g = gray[y:y+50, x:x+50]
            crop = edged[y:y+50, x:x+50]

            try:
                (H, hogImage) = feature.hog(crop_g, orientations=9, pixels_per_cell=(10, 10),
                        cells_per_block=(2, 2), transform_sqrt=True, block_norm="L1", visualize=True)

                hogImage = exposure.rescale_intensity(hogImage, out_range=(0, 255))
                hogImage = hogImage.astype("uint8")

                pred = model.predict(H.reshape(1, -1))[0]

                if pred == 1:
                    crop_img_by_HOG = edged[y-50:y+100, x:x+150]
                    crop_img_by_HOG = cv2.resize(crop_img_by_HOG, (50, 50))
   
                    cv2.imshow("crop_img_by_HOG", crop_img_by_HOG)
                    cv2.waitKey(0)

                    data1 = to_list(crop_img_by_HOG)
                    data1 = np.array(data1)

                    pred1 = model1.predict(data1.reshape(1, -1))[0]
                    print(pred1)

           

                    if pred1 == 1:
                        cv2.rectangle(img, (x, y-50), (x+150, y+100), (0,0,255), 1)
                        cv2.imshow("img", img)
                        cv2.waitKey(0)


            except:
                pass



    
































