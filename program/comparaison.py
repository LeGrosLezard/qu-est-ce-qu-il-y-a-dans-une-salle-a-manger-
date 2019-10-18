import numpy as np
import cv2
import os
import imutils
import math
from PIL import Image
from skimage import exposure
from skimage import feature

from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
import joblib




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
    

def save_picture(name, image):
    path = "dataset/data_analysing/{}"
    cv2.imwrite(path.format(str(name)), image)


def blanck_picture(img):

    """Create a black background picture same dimension of original picture"""

    blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
    blank_image[0:img.shape[0], 0:img.shape[1]] = 0, 0, 0

    return blank_image









def make_contours(img, blanck):
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,250,255,cv2.THRESH_BINARY_INV)

    contours,h=cv2.findContours(thresh,cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

    for i in contours:
        if cv2.contourArea(i) > 200:
            cv2.fillPoly(blanck, pts =[i], color=(0,255,0))

    #show_picture("blanck", blanck, 0, "y")


    return blanck


def object_contours_size(blanck):

    cnts_points = []
    for i in range(blanck.shape[0]):
        c = 0
        for j in range(blanck.shape[1]):
            if blanck[i, j][0] == 0 and\
               blanck[i, j][1] == 255 and\
               blanck[i, j][2] == 0:
               c += 1

        if c == 0:
            pass
        else:
            cnts_points.append(c)


    mean = sum(cnts_points) / len(cnts_points)

    points = []
    for nb, i in enumerate(cnts_points):
        if i > mean + 6:
            points.append(nb)

    return points




def take_max_size(points, img):

    ok = 0; nan = False;

    for i in range(len(points)):
        try:
            if points[i] + 1 == points[i+1] and nan is False:
                ok = points[i]
                nan = True
            else:
                nan = False
                cv2.rectangle(img, (0, ok),
                              (img.shape[0], points[i]),
                              (0,0,255), 30)
                ok = 0
        except:
            pass

    #show_picture("img", img, 0, "y")
    return img



def draw_part_picture(img, copy):
    
    blanck1 = blanck_picture(img)
    blanck2 = blanck_picture(img)

    maxi = 0
    c = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j][0] == 0 and\
               img[i, j][1] == 0 and\
               img[i, j][2] == 255:
                blanck1[i, j] = copy[i, j]

            else:
                blanck2[i, j] = copy[i, j]

    return blanck1, blanck2




def full_white(img):

    full = img.shape[0] * img.shape[1]

    c = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j][0] == 0 and\
               img[i, j][1] == 255 and\
               img[i, j][2] == 0:
                c+=1


    if c > 8500:
        return False
    else:
        return True
    


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




def final_part(blanck):

    gray = cv2.cvtColor(blanck, cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY)

    contours,h=cv2.findContours(thresh,cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    maxi = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > maxi:
            maxi = cv2.contourArea(cnt)

    for cnt in contours:
        if cv2.contourArea(cnt) != maxi:
            cv2.fillPoly(blanck, pts =[cnt], color=(0,0,0))




    return blanck



def no_black_part(blanck):
    points = []
    for i in range(blanck.shape[0]):
        for j in range(blanck.shape[1]):
            if blanck[i, j][0] != 0 and\
               blanck[i, j][1] != 0 and\
               blanck[i, j][2] != 0:
                points.append(i)

    blanck = blanck[min(points):max(points), 0:]

    return blanck



def main_comparaison(img, csv_name, t):

    img = open_picture(img)
    img = cv2.resize(img, (50, 200))

    #show_picture("img", img, 0, "y")

    copy = img.copy()


    blanck = blanck_picture(img)
    blanck = make_contours(img, blanck)
    ocontinuer = full_white(blanck)

    if ocontinuer is True:

        points = object_contours_size(blanck)

        img = take_max_size(points, img)
        #show_picture("img", img, 0, "y")

        blanck1, blanck2 = draw_part_picture(img, copy)

        blanck1 = final_part(blanck1)
        blanck2 = final_part(blanck2)


        
        try:
            blanck1 = no_black_part(blanck1)
            blanck2 = no_black_part(blanck2)


            blanck1 = cv2.resize(blanck1, (50, 100))
            blanck2 = cv2.resize(blanck2, (50, 100))


            blanck1 = cv2.cvtColor(blanck1, cv2.COLOR_BGR2GRAY)
            H1, hogImage1 = HOG_detection(blanck1)
            #show_picture("hogImage1", hogImage1, 0, "y")

            write_data_into_csv(csv_name, str(1), H1)


            blanck2 = cv2.cvtColor(blanck2, cv2.COLOR_BGR2GRAY)
            H2, hogImage2 = HOG_detection(blanck2)
            #show_picture("hogImage2", hogImage2, 0, "y")

            write_data_into_csv(csv_name, str(2), H2)

        except:
            pass




from training.to_csv import verify_name_csv
from training.to_csv import csv_write
from training.to_model import csv_to_data
from training.to_model import training
from training.to_model import verify_name
from training.course_object import main_couse
from training.to_csv import write_data_into_csv


csv_name = verify_name_csv()
csv_write(csv_name, 5000)
print(csv_name)




liste_n = os.listdir("dataset/N")
for picture_n in liste_n:

    picture_n = str("dataset/N/") + str(picture_n)    
    main_couse(picture_n, csv_name, str(0))



t = 0
objects_to_search = ['Fourchette']
for objects in objects_to_search:

    liste = os.listdir("dataset/clean/" + str(objects))
    for picture in liste:
        picture = str("dataset/clean/") + str(objects) + "/" + str(picture)
        main_comparaison(picture, "_in_training.csv", t)


        t += 1



name = verify_name()
data, label = csv_to_data("_in_training.csv")
training(data, label, name)














