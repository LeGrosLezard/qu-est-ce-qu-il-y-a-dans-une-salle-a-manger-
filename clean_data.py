import numpy as np
import cv2
import os


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
def treatment_background(img):


    img = cv2.imread("163.jpg")
    img = cv2.resize(img, (200, 200))

    copy_img = img.copy()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blanck = blanck_picture(img)

    th3 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                cv2.THRESH_BINARY,11,10)

    #show_picture("thresh", th3, 0, "y")


    contours, _ = cv2.findContours(th3, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)
    
    for cnts in contours:
        if 50 < cv2.contourArea(cnts) < 30000:
            print(cv2.contourArea(cnts))
            
            cv2.drawContours(blanck, cnts, -1, (255, 255, 255), 1)



    gray_blanck = cv2.cvtColor(blanck, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(gray_blanck, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)


    cv2.drawContours(copy_img, contours, -1, (0, 255, 0), 21)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if copy_img[i, j][0] != 0 and\
               copy_img[i, j][1] != 255 and\
               copy_img[i, j][2] != 0:
                img[i, j] = 255, 255, 255


    #show_picture("blanck", blanck, 0, "")
    show_picture("img", img, 0, "")
    


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
    cv2.circle(blanck, (X_min, Xy_min), 6, (255, 255, 255), 6)
    cv2.circle(blanck, (X_max, Xy_max), 6, (255, 255, 255), 6)

    cv2.circle(blanck, (Xy_min2, X_min2), 6, (255, 255, 0), 6)
    cv2.circle(blanck, (Xy_max2, X_max2), 6, (255, 255, 0), 6)

    show_picture("blanck", blanck, 0, "")

##    print(X_min, Xy_min)
##    print(X_max, Xy_max)
##    print(X_min2, Xy_min2)
##    print(X_max2, Xy_max2)




    return X_min, Xy_min, X_max, Xy_max,\
           X_min2, Xy_min2, X_max2, Xy_max2




def treatment_inclinaison(X_min, Xy_min, X_max, Xy_max,
                          X_min2, Xy_min2, X_max2,
                          Xy_max2):

    out = 0

    #0) ok 1) horrizontal 2)bot/top 3)top/bot 
    #if there are length min or max it give the sens
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



def rotation_on_current_picture(position, img):
    #0) ok 1) horrizontal 2)bot/top 3)top/bot

    show_picture("image", img, 0, "")
    print(position)

    """ROTATION"""



def position_rotation(contours, blanck, img):


    position_circleX, position_circleY = draw_contours(contours, blanck)

    listex, listey, listex2, listey2 = recup_red_points(blanck)

    X_min, Xy_min, X_max, Xy_max,\
    X_min2, Xy_min2, X_max2, Xy_max2\
    = points_for_define_inclinaison(listex, listey, listex2, listey2, blanck)

    position = treatment_inclinaison(X_min, Xy_min, X_max, Xy_max,
                                     X_min2, Xy_min2, X_max2, Xy_max2)

    rotation_on_current_picture(position, img)



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


        #position_rotation(contours, blanck, img) #rotation
        treatment_background("163.jpg")                 #background


        break

def open_download_folder(objects_to_search):

    for i in objects_to_search:

        liste_obj = os.listdir("dataset1/" + i)
        contours_obj, blanck = take_features(liste_obj, i)  #take_features
        

        break




if __name__ == "__main__":

    
    objects_to_search = ["cuillere", "fourchette", "couteau", "verre"]
    open_download_folder(objects_to_search)




































