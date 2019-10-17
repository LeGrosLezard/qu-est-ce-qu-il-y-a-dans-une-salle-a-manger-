
import requests
import datetime
import urllib.request
from bs4 import *
import datetime


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
    #print(path.format(label))
    page = request.content
    soup_html = BeautifulSoup(page, "html.parser")
    content_html = soup_html.find_all(element_search)

    return content_html



def properies_object(objects_to_search):

    key = ["constitué", "constituée", "{} est un", "{} est une"]

    dico_path = our_dico_path_url()
    dico_path["wikipedia"]


    element = []

    for i in objects_to_search:
        
        content = bs4_function(dico_path["wikipedia"], i, ("tr"))

        c = 0
        for cnt in content:
            if c == 1:
                if str(cnt.get_text())[:10] == "Composé de":
                    #print(str(cnt.get_text())[10:])
                    element.append([str(cnt.get_text())[10:] + ",", i])
            c+=1

    return element




def treat_element(element):


    dico = {}

    for i in element:
        dico[i[1]] = []

    print(dico)


    increment = ""
    for i in element:
        for j in i[0]:

            if j in (" ", ","):

                parenthese = str(increment).find(str("("))
                if parenthese >= 0:
                    increment = ""

                else:
                    for letter in increment:
                        if letter == "\n":
                            increment = increment.replace("\n", "")
        
                    for key, value in dico.items():
                        if key == i[1] and increment != "":
                            dico[str(key)].append(increment)

                increment = ""


            else:
                increment += j
            

    return dico



objects_to_search = ['Couteau', 'Cuillère', 'Fourchette']
element = properies_object(objects_to_search)
carac = treat_element(element) 











