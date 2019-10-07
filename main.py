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


    for y in range(0, img.shape[0], 50):
        for x in range(0, img.shape[1], 50):

            clone = img.copy()
            crop = img[y:y+50, x:x+50]
            cv2.rectangle(clone, (x, y), (x + 50, y + 50), (0, 255, 0), 2)

            try:

                (H, hogImage) = feature.hog(crop, orientations=9, pixels_per_cell=(10, 10),
                        cells_per_block=(2, 2), transform_sqrt=True, block_norm="L1", visualize=True)



                hogImage = exposure.rescale_intensity(hogImage, out_range=(0, 255))
                hogImage = hogImage.astype("uint8")

                pred = model.predict(H.reshape(1, -1))[0]
                print(pred)

                
            except:
                pass

            
            #cv2.circle(clone, (int(x+50/2), int(y+50/2)), 3, (0,0,255), 3)


            cv2.imshow("Window", clone)
            cv2.imshow("img", hogImage)
            cv2.waitKey(1)
            time.sleep(0.5)












