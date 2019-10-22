import os
import cv2
import joblib
import numpy as np
from skimage import feature
from sklearn import metrics
from skimage import exposure


def open_picture(image):

    img = cv2.imread(image)
    return img

def show_picture(name, image, mode, destroy):

    cv2.imshow(name, image)
    cv2.waitKey(mode)
    if mode == 1:
        time.sleep(0.1)
    if destroy == "y":
        cv2.destroyAllWindows()


def blanck_picture(img):
    blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
    blank_image[0:img.shape[0], 0:img.shape[1]] = 0, 0, 0
    return blank_image



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




def detection(model, w, h, img):

    model = joblib.load(model)

    img = cv2.resize(img, (w, h))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,245,255,cv2.THRESH_BINARY_INV)

    contours,h=cv2.findContours(thresh,cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)

    blanck = blanck_picture(img)


    for cnts in contours:
        cv2.fillPoly(blanck, pts =[cnts], color=(255,255,255))
    show_picture("blanck", blanck, 0, "")

    grayblanck = cv2.cvtColor(blanck, cv2.COLOR_BGR2GRAY)

    contours,h=cv2.findContours(grayblanck,cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)


    maxi = 0
    non = False
    for c in contours:
        if cv2.contourArea(c) > 11000:
            non = True
        else:
            if cv2.contourArea(c) > maxi:
                maxi = cv2.contourArea(c)

    if non is False:
        blanck1 = blanck_picture(img)
        for c in contours:
            if cv2.contourArea(c) == maxi:
                cv2.fillPoly(blanck1, pts =[c], color=(255,255,255))

    blanck1 = cv2.cvtColor(blanck1, cv2.COLOR_BGR2GRAY)

    data = to_list(blanck1)
    predictions = model.predict([data])

    print(predictions[0])
    return predictions[0]

































