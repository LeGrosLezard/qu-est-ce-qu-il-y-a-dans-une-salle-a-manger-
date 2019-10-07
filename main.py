import os
import cv2
import joblib

import time
from skimage import exposure
from skimage import feature





liste = os.listdir(r"C:\Users\jeanbaptiste\Desktop\assiette\image\assiette_couvert")
path  = "image/assiette_couvert/{}"
model = joblib.load("model/miammiam_model")

for i in liste:
    print(path.format(i))

    img = cv2.imread(path.format(i))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edged = cv2.Canny(gray, 100, 200)

    for y in range(0, img.shape[0], 50):
        for x in range(0, img.shape[1], 50):
            
            clone = img.copy()
            crop = edged[y:y+50, x:x+50]


            #on récupérer les contours
            contours, _ = cv2.findContours(crop, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)

            #on recupere le plus grand
            max_cnt = 0
            for i in contours:
                if cv2.contourArea(i) >= max_cnt:
                    max_cnt = cv2.contourArea(i)


            #on fait match le plus grand contour avec la liste puis corp gray
            for i in contours:
                if cv2.contourArea(i) != max_cnt:
                    cv2.drawContours(crop, i, -1, (0))
                     
                
            try:

                (H, hogImage) = feature.hog(crop, orientations=9, pixels_per_cell=(10, 10),
                        cells_per_block=(2, 2), transform_sqrt=True, block_norm="L1", visualize=True)


                hogImage = exposure.rescale_intensity(hogImage, out_range=(0, 255))
                hogImage = hogImage.astype("uint8")

                pred = model.predict(H.reshape(1, -1))[0]

                if pred == 1:
                    cv2.rectangle(img, (x, y), (x + 50, y + 50), (0, 0, 255), 2)

                
            except:
                pass


                     
            cv2.rectangle(clone, (x, y), (x + 50, y + 50), (0, 255, 0), 2)


            cv2.imshow("Window", clone)
            cv2.imshow("img", crop)
            cv2.waitKey(1)
            time.sleep(0.5)


    cv2.imshow("imgage", img)
    cv2.waitKey(0)









