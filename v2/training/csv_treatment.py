import os
import csv


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





















path_csv_file = r"C:\Users\jeanbaptiste\Desktop\assiette\v2\training\csv\in_training\{}"
path1 = path_csv_file.format("bol.csv")
path2 = path_csv_file.format("test.csv")

csv_treatement(path1, path2)
















