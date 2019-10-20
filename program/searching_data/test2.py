import datetime
import requests
from bs4 import *
import urllib.request


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


def searching(tag, scrap_list):

    content_html = bs4_function(dico_path["wikipedia"],
                            objects, tag)


    stop = False
    for i in content_html:
        i = i.get_text()

        for scraping in scrap_list:

            if stop is True:
                break

            search = str(i).find(str(scraping))
            if search >= 0:
                print(scraping)
                paragraph = i[search:search+50]
                print(paragraph)
                stop = True
                break

    return stop





objects = "marteau"

dico_path = our_dico_path_url()

scrap_objet = ["espèce", "vivant", "animal", "fruit", "légume",
              "élément", "plante", "appareil", "véhicule", "machine",
              "outil"]

scrap_mot = ["{} est un", "{} est une",
             "{}[1] est un", "{}[1] est une",]



stop = searching("p", scrap_objet)
stop_stop = searching("p", scrap_mot)


if stop_stop is False and stop is False:

    _ = searching("div", scrap_objet)
    _ = searching("li", scrap_objet)

















