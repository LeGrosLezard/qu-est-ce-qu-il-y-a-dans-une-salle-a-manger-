import requests
import datetime
import urllib.request
from bs4 import *
import datetime



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
                


def our_dico_path_url():
    """Google for category of our label,
    wiki for words in ahref
    exemple_of google for example of category
    """

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
                #google give: "Categorie:dog - ...."
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

    #BS4 function 1)search category of ... -> 2) give wikipedia:categorie of...
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

    #BS4 function We recup all ahref of text content
    content_html = content_html = bs4_function(dico_path["wikipedia"],
                                               object_category, ("a", {"class":"mw-body"}))

    liste = []

    for nb, i in enumerate(content_html):
        #only tag with title (no navigation)
        no_navigation = str(i).find(str("title"))
        if no_navigation >= 0 and i.get_text() not in (""):
            liste.append(i.get_text())
        #stop at 10 elements
        if nb >= 10:
            break

    return liste



def search_no_object(content_html, mode):

    """If it's category again like couverts so google give some examples
    BUT there are noises

    else like assiette google doesn't give example
    """

    #tag to str
    liste_tag = [str(i) for i in content_html]
    liste = [str(i.get_text()) for i in content_html]
    liste_object = []
    counter = 0
    #filter search
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
            #Sometimes there are in end words
            if i[-1] in (".", ",", ";"):
                i = i[:-1]
            parenthese = str(i).find("(")
            if parenthese >= 0:
                i = i[:parenthese-1]

            if mode == "td":

                increment = ""
                for el_tag in liste_tag[counter]:
                    if el_tag == " ":
                        if increment == " s5aIid":  
                             liste_object.append(i)
                        increment = ""
                    increment += el_tag


            elif mode == "li":
                liste_object.append(i)

        counter +=1


    if mode is "td":

        def td_cleaning_list(liste_object):
            liste = []
            increment = ""
            for i in liste_object:
                for j in i:
                    if j == ",":
                        if increment[0] == " ":
                            increment = increment[1:]
                        liste.append(increment)
                        increment = ""
                    else:
                        increment += j
                if increment != "":
                    liste.append(increment)
                    increment = ""
   
            return liste

        liste_object = td_cleaning_list(liste_object)

    return liste_object



def transform_category_to_object(category_found, dico_path):

    """There are two differents way:
    the td and the li
    """

    objects_to_search = []

    for objects in category_found:
        print(objects, "in course...")

        #BS4 function
        #category of category google give examples -> 1)quadrupede -> 2)(we are here) animals -> 3)god/cat
        content_html_td = bs4_function(dico_path["exemple_of"],
                                       objects, ("td", {"class":"mod"}))

        content_html_li = bs4_function(dico_path["exemple_of"],
                                        objects, ("li", {"class":"mod"}))

        liste_td = search_no_object(content_html_td, "td")
        liste_li = search_no_object(content_html_li, "li")

        if liste_td == [] and liste_li == []:
            objects_to_search.append(objects)

        else:
            if liste_td not in []:
                for i in liste_td:
                    objects_to_search.append(i)

            if liste_li not in []:
                for i in liste_li:
                    objects_to_search.append(i)

    return objects_to_search






def properies_object(objects_to_search):

    dico_path = our_dico_path_url()
    dico_path["wikipedia"]
    
    for i in objects_to_search:
        content = bs4_function(dico_path["wikipedia"], i, p)
        print(content)








def searching_on_internet(label):
    #It's our path ex: wikipedia question url
    our_path = our_dico_path_url()
##    #We search category of our first label
##    category = searching_category(label, our_path)
##    #We recup other object from this last category
##    category_found = other_element_from_category(category, label, our_path)
##    #We filter this object because we can have category of the last category


    category_found = ["aliments"]
    objects_to_search = transform_category_to_object(category_found, our_path)
    print(objects_to_search)


    #objects_to_search = ['Catégories', 'Exemples potentiels', 'Aliments de base', 'Fruits, légumes, lin, poissons gras', 'Aliments transformés', "Céréales de son d'avoine", 'Aliments transformés avec ingrédients ajoutés', 'Jus de fruits enrichi de calcium', 'assiettes', 'Baguettes', 'Couteau', 'Cuillère', 'Cure-dent', 'Fourchette', 'Paille', 'Pincettes', 'verres', 'bols', 'tasses']
    #properies_object(objects_to_search)
    


    
    return objects_to_search




def inventory_item():
    #Writte a new lign in our inventory
    #element_to_detection("1", "assiette")
    #Recup item for our inventory
    number_label, label = element_in_label_PY()

    return number_label, label


number_label, label = inventory_item()
objects_to_search = searching_on_internet(label)

















