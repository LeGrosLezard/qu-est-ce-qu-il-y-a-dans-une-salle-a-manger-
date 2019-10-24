import os
import csv


def csv_labels(path_current_csv):

    liste_csv = os.listdir(path_current_csv)
    current_csv = liste_csv[-1]

    print(current_csv)

    path_current_csv = path_current_csv + "/" + str(current_csv)

    file =  open(path_current_csv, 'r')
    dataframe = file.readlines()

    liste = []

    for i in dataframe:
        liste.append(i[0])


    liste = list(set(liste))
    liste.remove("l")

    new_name_csv = int(current_csv[:-4]) + 1

    return liste, new_name_csv



def define_new_csv(liste, path, new_name):

    
    if len(liste) == 10:
        
        csv_create = path + "/" + str(new_name) + ".csv"

        with open(csv_create, "a") as file:
            pass

        




##
##path_csv = r"C:\Users\jeanbaptiste\Desktop\assiette\v2\training\csv\csv"
##
##liste, new_name_csv = csv_labels(path_csv)
##define_new_csv(liste, path_csv, new_name_csv)











def csv_treatement(path_csv_file, path2):

    file =  open(path_csv_file, 'r')
    dataframe = file.readlines()

    
    for i in dataframe:
        liste = []
        if i[0] == "1":
            liste.append(i)

            liste = liste[0].split(";")

            if liste[-1] == "0\n":liste[-1] = "0";
            if liste[-1] == "1\n":liste[-1] = "1";

            file.close()



            with open(path2, 'a') as add:
                writer = csv.writer(add)

                for element in liste:
                    add.write(str(element)+";")
                add.write("\n")
  
            add.close()





















##path_csv_file = r"C:\Users\jeanbaptiste\Desktop\assiette\v2\training\csv\in_training\{}"
##path1 = path_csv_file.format("Paille.csv")
##path2 = path_csv_file.format("test.csv")
##
##csv_labels(path1)
#csv_treatement(path1, path2)
















