import cv2
import os
import csv
import numpy as np

from skimage import exposure
from skimage import feature

import time
import joblib
import imutils

import requests
import datetime
import urllib.request
from bs4 import *
import datetime



#-------------------------------------------------------------------------- Part model learning
def element_to_detection(label, detection):
    with open("label.py", "a") as file:
        row = str(label) + "," + str(detection) + ";\n"
        file.write(str(row))
        
def element_in_label_PY():

    label = []
    number_label = []
    increment = ""
 
    with open("label.py", "r") as file:
        for i in file:
            for j in i:

                if j in (";"):
                    label.append(increment)
                    increment = ""

                if j not in (",", " ", "\n"):
                    try:
                        j = int(j)
                        if j == int(j):
                            number_label.append(j)
   
                    except:
                        increment += j

    return number_label, label     
                

#-------------------------------------------------------------------------- Part model learning


#-------------------------------------------------------------------------- Part picture
def open_picture(image):

    """We open picture"""

    img = cv2.imread(image)

    return img


def blanck_picture(img):

    """Create a black background picture same dimension of original picture"""

    blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
    blank_image[0:img.shape[0], 0:img.shape[1]] = 0, 0, 0

    return blank_image



def reverse_img_by_pos(img, x, y, size):

    """ 
    We loop the picture x and y range.
    We ask a crop of the picture x to x + 25 * 3, same for y
    
    If we are at border of picture x - 25 * 3 to x
    """

    
    height, width, channel = img.shape

    reverse_x = False
    reverse_y = False
    
    if x >= width - size:
        reverse_x = True

    if y >= height/2:
        reverse_y = True


    if reverse_x is True:
        crop = img[y:y+size*5, x-size*5:x]
        pts = (y, y+size*5, x-size*5, x)


    if reverse_y is True:
        crop = img[y-size*5:y, x:x+size*5]
        pts = (y-size*5, y, x, x+size*5)

    if reverse_x is False and reverse_y is False:
        crop = img[y:y+size*5, x:x+size*5]
        pts = (y, y+size*5, x, x+size*5)


    return crop, pts



def HOG_detection(gray):

    """We detect contour orientation gradient
    from color"""

    (H, hogImage) = feature.hog(gray, orientations=9, pixels_per_cell=(10, 10),
                                cells_per_block=(2, 2), transform_sqrt=True,
                                block_norm="L1", visualize=True)

    hogImage = exposure.rescale_intensity(hogImage, out_range=(0, 255))
    hogImage = hogImage.astype("uint8")

    return H, hogImage


def rotation():
    pass

def parcours_image(img, model):

    """We put picture into model. We try to match
    The last crop with picture on model"""

    size = 25
    list_intersection = []
    img_detection = img.copy()

    for y in range(0, img.shape[0], size):
        for x in range(0, img.shape[1], size):

            clone = img.copy()

            try:
                crop, pts = reverse_img_by_pos(img, x, y, size)

                crop = cv2.resize(crop, (50, 50))
                gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

                H, hogImage = HOG_detection(gray)
                pred = model.predict(H.reshape(1, -1))[0]

                if pred == 1:
                    cv2.rectangle(img_detection, (pts[2], pts[0]), (pts[3], pts[1]), (0, 0, 255), 2)
                    list_intersection.append([pts[2], pts[0], pts[3], pts[1]])
            except:
                pass


##            cv2.rectangle(clone, (x, y), (x + size, y + size), (0, 255, 0), 2)
##            show_picture("clone", clone, 1, "")
##            show_picture("img_detection", img_detection, 1, "")
##            time.sleep(0.3)

    return list_intersection





def reconstruction(image, liste):

    """We can have multiple detection so
    We make an average of this and recup the final detection
    We return this points"""

    a = 0
    b = 0
    c = 0
    d = 0

    for i in liste:
        a += i[0]
        b += i[1]
        c += i[2]
        d += i[3]

    e = len(liste)

    cv2.rectangle(image, (int(a/e), int(b/e)), (int(c/e), int(d/e)), (0, 0, 255), 1)
    show_picture("image", image, 0, "y")

    return int(a/e), int(b/e), int(c/e), int(d/e)


def remove_background(img):

    """If background isn't white we delete it"""
    pass


def get_other_object(img):

    """We detecte contours from the picture
    We try to recup them and to put it into rectangle"""

    blanck = blanck_picture(img)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    th3 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                cv2.THRESH_BINARY,11,10)

    contours, _ = cv2.findContours(th3, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)

    liste = []
    for cnts in contours:
        if 30000 > cv2.contourArea(cnts) > 200:
            x, y, w, h = cv2.boundingRect(cnts)
            liste.append([x, y, w, h])
            cv2.drawContours(blanck, cnts, -1, (255, 255, 255), 1)

 
    show_picture("blanck", blanck, 0, "y")
    return liste



def croping_it_from_original(img, liste, x, y, w, h):

    """Now we must fusion the multiples detections from
    a single object.
    We must crop it now for an other matching with current model"""

    print(liste)

    for i in liste:
        print(i)
        cv2.rectangle(img, (i[0], i[1]), (i[0] + i[2], i[1] + i[3]), (0, 0, 255), 1)

    
    show_picture("img", img, 0, "")




def show_picture(name, image, mode, destroy):
    cv2.imshow(name, image)
    cv2.waitKey(mode)
    if destroy == "y":
        cv2.destroyAllWindows()

#-------------------------------------------------------------------------- Part picture







#-------------------------------------------------------------------------- Part Scrapping

def our_dico_path_url():

    dico_path = {"google":"https://www.google.com/search?sxsrf=ACYBGNSdXLbezE1nvpQMhQ6Hp7qFGaiDxg%3A1570625734452&ei=xtidXfahG8rCgwfSsauQDQ&q=cat%C3%A9gorie+de+l%27objet+{0}&oq=cat%C3%A9gorie+de+l%27objet+{0}&gs_l=psy-ab.3..33i160.683.1619..1667...0.0..0.200.916.0j6j1......0....1..gws-wiz.......33i22i29i30.ya7xfhMLlT8&ved=0ahUKEwj2nOjnnI_lAhVK4eAKHdLYCtIQ4dUDCAs&uact=5",
                 "wikipedia": "https://fr.wikipedia.org/wiki/{}",
                 "exemple_of":"https://www.google.com/search?hl=fr&sxsrf=ACYBGNQeVb_NYY7utIXV-9TKkWxW89ABgg%3A1570629335228&ei=1-adXZHODb6IjLsP6N2VuAc&q=exemple+de+{0}&oq=exemple+de+{0}&gs_l=psy-ab.3..0i22i10i30j0i22i30l9.4989.6189..6333...0.4..0.115.711.4j3......0....1..gws-wiz.......0i71j0j0i20i263j0i203.QvdVxJ7yvh4&ved=0ahUKEwjRleacqo_lAhU-BGMBHehuBXcQ4dUDCAs&uact=5"}

    return dico_path


def bs4_function(path, label, element_search):

    """Request, content, bs4, element"""

    request = requests.get(path.format(label))
    page = request.content
    soup_html = BeautifulSoup(page, "html.parser")
    content_html = soup_html.find_all(element_search)

    return content_html


def treatment_list_category(liste, label):

    print("We found category")

    category_object = ""
    increment = ""
    count = 0

    for i in liste:
        for j in i:
            if j == " ":
                category = str(i).find(str("Catégorie:"))
                category_object = str(i[category+10:count])
                break

            count+=1


    print(label, "=", category_object)
    return category_object



def searching_category(label, dico_path):

    """We search category like plate for vaisselle"""

    print(label)
    print("time to search object catergory...")
    print("")

    liste = []

    #BS4 function
    content_html = bs4_function(dico_path["google"], label, ("a", {"class":"mw-body"}))

    #pass for "" or \n
    for i in content_html:
        if i.get_text() in ("", "\n"):
            pass

        else:
            #search word wikipedia and category
            wiki_search = str(i).find(str("wikipedia"))
            categorie = str(i).find(str("Catégorie"))

            #recup only text for category
            if wiki_search >= 0 and categorie >= 0:
                liste.append(i.get_text())

    #recup category
    object_category = treatment_list_category(liste, label)
    return object_category




def other_element_from_category(object_category, label, dico_path):


    """vaiselle give spoon"""

    print("\nother object from category where ", label, "is ", object_category)

    #BS4 function
    content_html = content_html = bs4_function(dico_path["wikipedia"],
                                               object_category, ("a", {"class":"mw-body"}))
    
    liste = []

    for nb, i in enumerate(content_html):
        no_navigation = str(i).find(str("title"))
        if no_navigation >= 0 and i.get_text() not in (""):
            liste.append(i.get_text())
        if nb >= 10:
            break

    return liste



def search_no_object(content_html):

    """If it's category again like couverts so google give some examples
    BUT there are noises

    else like assiette google doesn't give example
    """

    liste = [str(i.get_text()) for i in content_html]
    liste_object = []
    for i in liste:
        if i in ("Toutes les langues", "Rechercher les pages en Français",
                "Date indifférente", " Moins d'une heure", 
                " Moins de 24 heures", " Moins d'une semaine",
                " Moins d'un mois", " Moins d'un an", "Moins de 24\xa0heures"
                "Tous les résultats", "Mot à mot", "Tous les résultats",
                'Date indifférente', 'Rechercher les pages en Français',
                'Toutes les langues', 'Date indifférente'):
            pass
        else:
            if i[-1] in (".", ",", ";"):
                i = i[:-1]
            liste_object.append(i)


    return liste_object



def transform_category_to_object(category_found, dico_path):

    """There are two differents way:
    the td and the li
    """

    objects_to_search = []
    
    for objects in category_found:
        print(objects, "in course...")

        #BS4 function
        content_html_td = bs4_function(dico_path["exemple_of"],
                                       objects, ("td", {"class":"mod"}))

        content_html_li = bs4_function(dico_path["exemple_of"],
                                        objects, ("li", {"class":"mod"}))


        liste_td = search_no_object(content_html_td)
        liste_li = search_no_object(content_html_li)

        if liste_td == [] and liste_li == []:
            objects_to_search.append(objects)

        else:

            if liste_td not in []:
                for i in liste_td:
                    objects_to_search.append(i)
 
            if liste_li not in []:
                for i in liste_li:
                    objects_to_search.append(i)
        
    print(objects_to_search)


#-------------------------------------------------------------------------- Part Scrapping





if __name__ == "__main__":


    def inventory_item():
        #Writte a new lign in our inventory
        #element_to_detection("1", "assiette")
        #Recup item for our inventory
        number_label, label = element_in_label_PY()

        return number_label, label


    def detection_picture():
        #load model
        model = joblib.load("model/miammiamsvmImage")
        #open img and copy it
        img = open_picture("assiette1.jpg")
        img_copy = img.copy()
        #recup all detection
        list_intersection = parcours_image(img, model)
        #take intersection detection
        x, y, w, h = reconstruction(img, list_intersection)
        #get other items on picture
        liste = get_other_object(img)

        """     IN COURSE    """    
        croping_it_from_original(img_copy, liste, x, y, w, h)


    def searching_on_internet(label):
        our_path = our_dico_path_url()
        category = searching_category(label, our_path)
        category_found = other_element_from_category(category, label, our_path)
        transform_category_to_object(category_found, our_path)


    number_label, label = inventory_item()
    for i in label:
        searching_on_internet(i)
        











