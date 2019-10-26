import sys
sys.path.append(r"C:\Users\jeanbaptiste\Desktop\assiette\v2")

import os
import csv
import time
from training.training import csv_to_list
from training.training import training
from training.training import train

#------------------------------------------------------------------
def dection_training(name, liste):
    """We got detection : name and width and height tranined
    We need to recup the name of this csv"""

    #match detection and training csv
    size = []
    for i in liste:
        for n in name:
            if i[0] == n:
                size.append(str(i[0]) + "x" + str(i[1]) + "x" + str(i[2]))
    size = list(set(size))

    return size


def csv_offcials_files(size, liste_csv, element):
    """We need to recuperate an official csv with the lasts
    dimensions """
    print(liste_csv)
    #recup all info: name, width, height
    current = []
    for i in size:
        i = i.split("x")
        if i[0] == element[:-4]:
            current.append(i)

    #recup official csv
    liste_csv_find = []
    for i in liste_csv:
        i = i.split("x")
        if i[-1][-4:] == ".csv":i[-1] = i[-1][:-4]
        liste_csv_find.append(i)

    #match our detection size with official size
    to_search = []
    for i in liste_csv_find:
        for j in current:
            try:
                if i[1] == j[1] and\
                   i[2] == j[2]:
                    to_search.append(i)
            except IndexError:
                pass

    return to_search

    
def recup_last_label(path_csv, current):
    """We got a csv, now we need to recup last label"""

    #go recup label into csv
    labeled = []
    to_read = path_csv + "/" + str(current)

    #recup only label column
    f =  open(to_read, 'r')
    dataframe = f.readlines()
    dataframe = dataframe
    for i in dataframe:
        try:
            labeled.append(int(i[0]))
        except:
            pass

    labeled = max(list(set(labeled)))
    return labeled




def get_csv(element, liste, name, liste_csv):
    """Here we treat the detection who give us
    name, width and height.

    We go into csv trained. We match csv with detection.

    We need to add this to official csv.
    For that we need to recup a csv with current dimension
    if yes we recup last label
    if not we create a new offical csv

    if label is 9 create a new official csv"""

    #match detection and training csv
    size = dection_training(name, liste)

    to_search = csv_offcials_files(size, liste_csv, element)
    #no file create it

    if to_search == []:
        return "file", ""

    #recup all csv with this dimension
    maxi_search = []
    for i in to_search:
        maxi_search.append(i[0])

    #recup the max csv (the last created)
    current = ""
    for i in to_search:
        if i[0] == max(maxi_search):
            current = "x".join(i)
    current = current + ".csv"


    labeled = recup_last_label(path_csv, current)

    #if the last label = 9 go create new file
    if labeled == 9: return "label", ""
    #return label + 1 = new label
    else: label = labeled + 1


    return current, label


#------------------------------------------------------------------

def create(path_csv, liste_csv, liste, name, element):
    """Create a new offical csv"""

    size = dection_training(name, liste)

    #recup the size
    to_size = []
    for i in size:
        i = i.split("x")
        if i[0] == element[:-4]:
            to_size.append(str(i[1]) + "x" + str(i[2]))

    #return the new name csv and label = 0

    to_size = str(1) + "x" + to_size[0] + ".csv"

    return to_size, "0"



def training_to_offical(path_csv_training, path_csv, there_is, label, i):
    """We need to recup training information
    for add it to the official"""

    #write training info into official csv
    path = path_csv_training + "/" + str(i)

    main = open(path_csv + "/" + there_is, 'a')

    f =  open(path, 'r')
    dataframe = f.readlines()
    dataframe = dataframe

    for j in dataframe:
        ok = False
        if j[0] == "1":
            j = j.split(";")
            j[0] = str(label)
            for k in j[:-1]:
                main.write(str(k)+";")
            ok = True
        if ok is True:
            main.write("\n")



def get_model(liste_model_training, liste_model, name_csv):


    liste = [i.split("x") for i in liste_model]
    name_csv = name_csv.split("x")


    for i in liste:
        if i[1] == name_csv[1] and\
           i[2] == name_csv[2][:-4]:
            return "x".join(i)
        else:
            name_csv = "x".join(name_csv)
            name_csv = name_csv[:-4]
            return name_csv
    

def step_height(liste, path_csv_training, path_csv,
                path_model, path_model_training):
    """
    1 - Recup detections informations.
    2 - Match it with his training csv
    3 - Recup official csv with same dimension
        - no create a official csv
        - yes recup label
            - label == 9
            - create new official csv
    4 - add training information into official csv
    5 - need to create new model
    6 - train it
    7 - raised old training
    """

    #path
    liste_training_csv = os.listdir(path_csv_training)
    liste_csv = os.listdir(path_csv)

    liste_model_training = os.listdir(path_model_training)
    liste_model = os.listdir(path_model)


    #get name from detection
    name = list(set([i[0] for i in liste]))


    #csv training == detection
    to_change = []
    for i in name:
        for csv in liste_training_csv:
            if str(i) + ".csv" == str(csv):
                to_change.append(csv)


    #NO CASE ITEMS HAVE DIFFERENTS SIZES
    cre = False
    c = 0
    a = 0
    for i in to_change:
        print(i)
        there_is, label = get_csv(i, liste, name, liste_csv)

        if there_is is "file" or there_is is "label":
            there_is, label = create(path_csv, liste_csv, liste, name, i)
            cre = True

        #no time for reload folder...
        if cre is True:
            if c >= 1:
                label = int(a) + 1
                label = str(label)
            else:
                c += 1
                a = label

    
        print(label)
        training_to_offical(path_csv_training, path_csv, there_is, label, i)




    name_model = get_model(liste_model_training, liste_model, there_is)
        
    X, Y = csv_to_list(there_is)
    training(X, Y, name_model)
    

















path_csv_training = "../training/csv/in_training"
path_csv = "../training/csv/csv"

liste_model = "../training/models/models"
path_models_training = "../training/models/in_training/"

liste_model_training = os.listdir(path_models_training)
liste_model = os.listdir(liste_model)

##liste = [['Fourchette', 20, 100, '../dataset/image/current/currentv0.jpg'], ['Fourchette', 20, 100, '../dataset/image/current/currentv00.jpg'], ['Cuillere', 20, 100, '../dataset/image/current/currentv000.jpg'], ['Cuillere', 20, 100, '../dataset/image/current/currentv1.jpg'], ['Fourchette', 20, 100, '../dataset/image/current/currentv1.jpg'], ['Cuillere', 20, 100, '../dataset/image/current/currentv3.jpg']]
##
##
##step_height(liste, path_csv_training, path_csv,
##            liste_model, path_models_training)


##get_model(liste_model_training, liste_model, "1x20x100.csv")




