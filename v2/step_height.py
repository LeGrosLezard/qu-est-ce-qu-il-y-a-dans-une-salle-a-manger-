import sys
sys.path.append(r"C:\Users\jeanbaptiste\Desktop\assiette\v2")

import os
import csv

from training.training import csv_to_list
from training.training import training
from training.training import train




def get_csv(element, liste, name, liste_csv):

    #match detection and training csv
    size = []
    for i in liste:
        for n in name:
            if i[0] == n:
                size.append(str(i[0]) + "x" + str(i[1]) + "x" + str(i[2]))
    size = list(set(size))


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

    #if label is 9 create a new csv
    labeled = max(list(set(labeled)))
    if labeled == 9:
        return "label", ""

    #return label + 1 = new label
    label = labeled + 1
    print("")
    print("")
    

    return current, label


    

def create(path_csv, liste_csv, liste, name, element):

    #match detection and training csv
    size = []
    for i in liste:
        for n in name:
            if i[0] == n:
                size.append(str(i[0]) + "x" + str(i[1]) + "x" + str(i[2]))
    size = list(set(size))

    print(size)

    #recup the size
    to_size = []
    for i in size:
        i = i.split("x")
        if i[0] == element[:-4]:
            to_size.append(str(i[1]) + "x" + str(i[2]))

    #return the new name csv and label = 0
    print(to_size)
    to_size = str(1) + "x" + to_size[0] + ".csv"

    print(to_size)
    print("")
    
    return to_size, "0"


def step_height(liste, path_csv_training, path_csv,
                path_model_training, path_model):

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

    


    for i in to_change:

        print(i)
        there_is, label = get_csv(i, liste, name, liste_csv)

        if there_is is "file" or there_is is "label":
            there_is, label = create(path_csv, liste_csv, liste, name, i)
        else:
            print(there_is, label)


        #write training info into official csv

        path = path_csv_training + "/" + str(i)
        print(path_csv + "/" + there_is)
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


        print("")
        print("")
    #X, Y = csv_to_list(to_read)
    #training(X, Y, to_read)



















path_csv_training = "../training/csv/in_training"
path_csv = "../training/csv/csv"

path_model = "../training/models/models"
path_models_training = "../training/models/in_training/"


liste = [['Fourchette', 20, 100, '../dataset/image/current/currentv0.jpg'], ['Fourchette', 20, 100, '../dataset/image/current/currentv00.jpg'], ['Cuillere', 20, 100, '../dataset/image/current/currentv000.jpg'], ['Cuillere', 20, 100, '../dataset/image/current/currentv1.jpg'], ['Fourchette', 20, 100, '../dataset/image/current/currentv1.jpg'], ['Cuillere', 20, 100, '../dataset/image/current/currentv3.jpg']]


step_height(liste, path_csv_training, path_csv,
            path_model, path_models_training)







