import os
import cv2
from skimage import feature
from skimage import exposure


liste = os.listdir()
register = 0

for i in liste:
    if i == "recup_data.py" or i == "register":
        pass
    else:
        print(i)
        img = cv2.imread(i)
        #img = cv2.resize(img, (100, 100))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 100, 200)


        #on récupérer les contours
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)

        #on recupere le plus grand
        max_cnt = 0
        for i in contours:
            if cv2.contourArea(i) >= max_cnt:
                max_cnt = cv2.contourArea(i)


        #on fait match le plus grand contour avec la liste puis corp gray
        for i in contours:
            if cv2.contourArea(i) != max_cnt:
                cv2.drawContours(edged, i, -1, (0))

        for y in range(0, img.shape[0], 50):
            for x in range(0, img.shape[1], 50):
                crop = edged[y:y+50, x:x+50]
                crop_g = gray[y:y+50, x:x+50]

                if crop.shape[0] != 50 or crop.shape[1] != 50:
                    pass
                else:

                    c = 0
                    b = 0
                    for cropx in range(crop.shape[0]):
                        for cropy in range(crop.shape[1]):
                            if crop[cropx, cropy] == 0:
                                b += 1
                            c += 1

                    if c == b:
                        pass
                    else:

                        (H, hogImage) = feature.hog(crop_g, orientations=9, pixels_per_cell=(10, 10),
                                cells_per_block=(2, 2), transform_sqrt=True, block_norm="L1", visualize=True)

                        hogImage = exposure.rescale_intensity(hogImage, out_range=(0, 255))
                        hogImage = hogImage.astype("uint8")

##                        cv2.imshow("daz", crop)
##                        cv2.imshow("hogImage", hogImage)
##                        cv2.waitKey(0)

                        cv2.imwrite("register2/" + str(register) + "crop1.jpg", crop_g)

                        register += 1
                















