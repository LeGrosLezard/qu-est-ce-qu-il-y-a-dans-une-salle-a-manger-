from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier

from skimage import exposure
from skimage import feature

import joblib
import cv2
import os


liste = os.listdir(r"C:\Users\jeanbaptiste\Desktop\assiette\image\assiette")
path  = r"C:\Users\jeanbaptiste\Desktop\assiette\image\assiette\{}"


liste1 = os.listdir(r"C:\Users\jeanbaptiste\Desktop\assiette\image\N")
path1  = r"C:\Users\jeanbaptiste\Desktop\assiette\image\N\{}"

data = []
labels = []


for nb in range(2):

    if nb == 1:
        liste = liste1
        path = path1

    for image in liste:
        #on lit l'image, to contours uniquement
        img = cv2.imread(path.format(image))
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
            if cv2.contourArea(i) == max_cnt:
                x, y, w, h = cv2.boundingRect(i)
                crop = gray[y:y + h, x:x + w]
                crop = cv2.resize(crop, (50, 50))


        #on prend l'histogram orienté gradient de l'image
            #ICI FAUT LE FAIRE SANS CE MACHIN APRES
        H, hogImage = feature.hog(crop, orientations=9, pixels_per_cell=(10, 10),
                cells_per_block=(2, 2), transform_sqrt=True, block_norm="L1",
                                 visualize=True)

        #on ajoute les info pour le model
        data.append(H)
        if nb == 1:
            labels.append("negativ")
        elif nb == 0:
            labels.append("assiette")


        #on affiche les image HOG/gray crop
        hogImage = exposure.rescale_intensity(hogImage, out_range=(0, 255))
        hogImage = hogImage.astype("uint8")

##
##        cv2.imshow("HOG Image", hogImage)
##        cv2.imshow("dzq", crop)
##        cv2.waitKey(0)


print(labels)


model = svm.SVC()
model.fit(data, labels)

joblib.dump(model, "model/miammiam_model") 















































































