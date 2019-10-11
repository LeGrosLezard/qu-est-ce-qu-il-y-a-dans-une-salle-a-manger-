import numpy as np
import cv2
import os
import imutils
import math



def open_picture(image):

    """We open picture"""

    img = cv2.imread(image)

    return img


def blanck_picture(img):

    """Create a black background picture same dimension of original picture"""

    blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
    blank_image[0:img.shape[0], 0:img.shape[1]] = 0, 0, 0

    return blank_image


def show_picture(name, image, mode, destroy):
    cv2.imshow(name, image)
    cv2.waitKey(mode)
    if destroy == "y":
        cv2.destroyAllWindows()


from PIL import Image
#------------------------------------------------------------------------------------ backa

def main_color_background(img):

    """
        We verify white is the current background
        Indeed, we recup the main color of picture.
    """
    
    dico = {}

    im = Image.fromarray(img)
    for value in im.getdata():
        if value in dico.keys():
            dico[value] += 1
        else:
            dico[value] = 1

    max_value = 0
    color = []
    for key, value in dico.items():
        if value > max_value:
            max_value = value
            color = key

    return color


def make_cnts(img):

    """
        We copy the picture,
        apply adaptativ threshold,
        make contour,
        and draw it into white image
    """

    copy_img = img.copy()
    copy_img1 = img.copy()

    #show_picture("copy_img1", copy_img1, 0, "y")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blanck = blanck_picture(img)

    th3 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                cv2.THRESH_BINARY,11,10)

    #show_picture("thresh", th3, 0, "y")


    contours, _ = cv2.findContours(th3, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)
    
    for cnts in contours:
        if 50 < cv2.contourArea(cnts) < 30000:
            cv2.drawContours(blanck, cnts, -1, (255, 255, 255), 1)

    #show_picture("blanck", blanck, 0, "y")

    return blanck, copy_img, copy_img1


def find_contour_else_white(img, blanck, copy_img):

    """
        We drawing a big contour on the copy of image.
        On the picture we detect contour from copy
        It give us the object in a big area of the picture
        Indeed if on the copy != green we put only white
    """

    gray_blanck = cv2.cvtColor(blanck, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(gray_blanck, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(copy_img, contours, -1, (0, 255, 0), 26)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if copy_img[i, j][0] != 0 and\
               copy_img[i, j][1] != 255 and\
               copy_img[i, j][2] != 0:
                img[i, j] = 255, 255, 255

    return img


def finish_to_clean_background(img):

    """
        We recup the main color now
        because we have object + background
    """
    
    dico = {}

    im = Image.fromarray(img)
    for value in im.getdata():
        if value in dico.keys():
            dico[value] += 1
        else:
            dico[value] = 1

    max_value = 0
    color = []
    for key, value in dico.items():
        if value > max_value and key != (255, 255, 255):
            max_value = value
            color = key

    return color


def masking_to_black(img, color):

    """We delete the rest of bakcground"""
    
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j][0] > color[0] - 70 and img[i, j][0] < color[0] + 70 and\
               img[i, j][1] > color[1] - 70 and img[i, j][1] < color[1] + 70 and\
               img[i, j][2] > color[1] - 70 and img[i, j][2] < color[2] + 70:
                img[i, j] = 255, 255, 255


    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j][0] < 50 and\
               img[i, j][1] < 50 and\
               img[i, j][2] < 50:
                img[i, j] = 255
               

    show_picture("img", img, 0, "")


    return img


def treatment_background(img):

    img = cv2.resize(img, (200, 200))
    color = main_color_background(img)

    #if background black
    if color[0] < 200 and color[1] < 200 and color[2] < 200:
        #make a blanck, a copy and make contour
        blanck, copy_img, copy_img1 = make_cnts(img)
        #We take contours of object and delete the background for a white bg
        img = find_contour_else_white(img, blanck, copy_img)
        #we delete the rest of bg
        color = finish_to_clean_background(img)
        #it'so ok now
        img = masking_to_black(img, color)


#------------------------------------------------------------------------------------ backa





def rectangle_more_one_object(contours):
    """Here we want separate in case multiple objects by area detection"""

    positionX = []; positionY = []; positionW = []; positionH = [];
    for cnts in contours:
        if cv2.contourArea(cnts) == maxi1 or\
           cv2.contourArea(cnts) == maxi2 or\
           cv2.contourArea(cnts) == maxi3:
            x, y, w, h = cv2.boundingRect(cnts)

            positionX.append(x); positionY.append(y);
            positionW.append(x+w); positionH.append(y+h);

            x, y, w, h = cv2.boundingRect(cnts)
            cv2.drawContours(blanck, cnts, -1, (255, 255, 255), 1)
            cv2.rectangle(blanck, (x, y), (x+w, y+h), (0, 0, 255), 3)
            

    for i in range(len(positionX)):
        print(positionX[i], positionY[i], positionW[i], positionH[i])

















 
#----------------------------------------------------------------------------------- rotation
"""
    1 - contour to red
    2 - recup red points
    3 - take min max contour width and height
    4 - define position inclinaison
"""

def draw_contours(contours, blanck):

    #recup center of detection and draw it in red
    position_circleX = []
    position_circleY = []



    for cnts in contours:
        if cv2.contourArea(cnts):
            
            cv2.drawContours(blanck, cnts, -1, (255, 255, 255), 1)
            
            M = cv2.moments(cnts)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            position_circleX.append(cX)
            position_circleY.append(cY)

            cv2.circle(blanck, (cX, cY), 6, (0, 0, 255), 6)


    return position_circleX, position_circleY



def recup_red_points(blanck):

    #recup red picture
    listex = []
    listey = []
    listex2 = []
    listey2 = []

    for y in range(blanck.shape[1]):
        for x in range(blanck.shape[0]):
            if blanck[y, x][0] == 0 and\
               blanck[y, x][1] == 0 and\
               blanck[y, x][2] == 255: 
                listex.append(x)
                listey.append(y)

            if blanck[x, y][0] == 0 and\
               blanck[x, y][1] == 0 and\
               blanck[x, y][2] == 255: 
                listex2.append(x)
                listey2.append(y)

    return listex, listey, listex2, listey2




def points_for_define_inclinaison(listex, listey, listex2, listey2, blanck):


    #take max (x, y) and min (x, y) on l and L
    X_min = min(listex)
    index_min = listex.index(min(listex))
    Xy_min = listey[index_min]

    X_max = max(listex)
    index_max = listex.index(max(listex))
    Xy_max = listey[index_max]

    X_min2 = min(listex2)
    index_min2 = listex2.index(min(listex2))
    Xy_min2 = listey2[index_min2]

    X_max2 = max(listex2)
    index_max2 = listex2.index(max(listex2))
    Xy_max2 = listey2[index_max2]


    #draw circle
    #width
    cv2.circle(blanck, (X_min, Xy_min), 6, (0, 255, 0), 6)
    cv2.circle(blanck, (X_max, Xy_max), 6, (50, 255, 50), 6)

    #height
    cv2.circle(blanck, (Xy_min2, X_min2), 6, (255, 0, 255), 6)
    cv2.circle(blanck, (Xy_max2, X_max2), 6, (255, 255, 0), 6)

    #show_picture("blanck", blanck, 0, "")

##    print(X_min, Xy_min)
##    print(X_max, Xy_max)
##    print(X_min2, Xy_min2)
##    print(X_max2, Xy_max2)




    return X_min, Xy_min, X_max, Xy_max,\
           X_min2, Xy_min2, X_max2, Xy_max2, blanck




def treatment_inclinaison(X_min, Xy_min, X_max, Xy_max,
                          X_min2, Xy_min2, X_max2,
                          Xy_max2):

    out = 0

    #0)ok 1)horrizontal 2)bot/top 3)top/bot 

    if abs(Xy_min - Xy_max) < 5 and\
       abs(Xy_min2 - Xy_max2) < 15:
        out = 0

    elif abs(Xy_min - Xy_max) < 5:
        out = 1
        
    
    elif abs(X_min - X_max) > 80 and Xy_min > Xy_max:
        out = 2

    elif abs(X_min - X_max) > 80 and Xy_min < Xy_max:
        out = 3
        
    elif abs(Xy_min2 - Xy_max2) < 15:
        out = 0

    return out


import math
def precise_angle(img, X_min, Xy_min, X_max, Xy_max,
                  X_min2, Xy_min2, X_max2, Xy_max2,
                  position, blanck):

    #0)ok 1)horrizontal 2)bot/top 3)top/bot 




    
    if position == 2:


        show_picture("img", img, 0, "")

        angle = 0
        continuer = True
        while continuer:

            
            rotated = imutils.rotate_bound(blanck, angle)
            copy = img.copy()
            copy = imutils.rotate_bound(copy, angle)
            

            aX = 0; aY = 0;
            bX = 0; bY = 0;

            for x in range(rotated.shape[0]):
                for y in range(rotated.shape[1]):
                    if rotated[x, y][0] == 50 and\
                       rotated[x, y][1] == 255 and\
                       rotated[x, y][2] == 50:
                       aX = x; aY = y

                    if rotated[x, y][0] == 0 and\
                       rotated[x, y][1] == 255 and\
                       rotated[x, y][2] == 0:
                       bX = x; bY = y
     
##
##            cv2.circle(copy, (aY, aX), 3, (0, 0, 255), 3)
##            cv2.circle(copy, (bY, bX), 3, (0, 0, 255), 3)
##            show_picture("copy", copy, 0, "")
##            show_picture("blanck", rotated, 0, "")

            #print(aX, aY, bX, bY)

            if aY - bY < 8:
                continuer = False
                print(aX, aY, bX, bY)
            angle -= 2



        print(angle)
        show_picture("copy", copy, 0, "")
        show_picture("blanck", rotated, 0, "y")

            





##    elif position == 3:
##        print("3")
##
##
##        show_picture("rotated", rotated, 0, "y")
##
##    elif position == 1:
##        print("1")
##
##        show_picture("rotated", rotated, 0, "y")
##
##    else:
##        show_picture("image", img, 0, "y")





def rotation_on_current_picture(position, img):
    #0) ok 1) horrizontal 2)bot/top 3)top/bot


    if position == 2:
        print("2")
        rotated = imutils.rotate(img, 55)
        show_picture("rotated", rotated, 0, "y")


    elif position == 3:
        print("3")
        rotated = imutils.rotate(img, -45)
        show_picture("rotated", rotated, 0, "y")

    elif position == 1:
        print("1")
        rotated = imutils.rotate(img, -90)
        show_picture("rotated", rotated, 0, "y")

    else:
        show_picture("image", img, 0, "y")







def position_rotation(contours, blanck, img):


    position_circleX, position_circleY = draw_contours(contours, blanck)

    listex, listey, listex2, listey2 = recup_red_points(blanck)

    X_min, Xy_min, X_max, Xy_max,\
    X_min2, Xy_min2, X_max2, Xy_max2, blanck\
    = points_for_define_inclinaison(listex, listey, listex2, listey2, blanck)

    position = treatment_inclinaison(X_min, Xy_min, X_max, Xy_max,
                                     X_min2, Xy_min2, X_max2, Xy_max2)

    precise_angle(img, X_min, Xy_min, X_max, Xy_max,
                  X_min2, Xy_min2, X_max2, Xy_max2,
                  position, blanck)

    #rotation_on_current_picture(position, img)



#----------------------------------------------------------------------------------- rotation






def take_features(liste_obj, category):

    path = "dataset1/{}/{}"
    
    for i in liste_obj:

        print("picture: ", i, "\n")
        img = open_picture(path.format(category, i))
        

        height, width, channel = img.shape
        if height > 200 and width > 200:
            img = cv2.resize(img, (200, 200))

        blanck = blanck_picture(img)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(img, 100, 200)

        contours, _ = cv2.findContours(edged, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)

        #treatment_background(img)                 #background
        position_rotation(contours, blanck, img) #rotation
        




def open_download_folder(objects_to_search):

    for i in objects_to_search:

        liste_obj = os.listdir("dataset1/" + i)
        contours_obj, blanck = take_features(liste_obj, i)  #take_features
        






if __name__ == "__main__":

    
    objects_to_search = ["cuillere", "fourchette", "couteau", "verre"]
    open_download_folder(objects_to_search)




































