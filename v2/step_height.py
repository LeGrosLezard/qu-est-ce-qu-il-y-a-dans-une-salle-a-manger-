import os
import csv

def step_height(liste):

    name = list(set([i[0] for i in liste]))

    path_csv_training = "../training/csv/in_training"
    liste_training_csv = os.listdir(path_csv_training)

    path_csv = "../training/csv/csv"
    liste_csv = os.listdir(path_csv)


    path_model_training = "../training/models/in_training"
    liste_model_training = os.listdir(path_model_training)

    path_model = "../training/models/models"
    liste_model = os.listdir(path_model)

    to_change = []
    for i in name:
        for csv in liste_training_csv:
            if str(i) + ".csv" == str(csv):
                to_change.append(csv)



    for i in to_change:
        print(i)

        path = path_csv_training + "/" + str(i)

        f =  open(path, 'r')
        dataframe = f.readlines()
        dataframe = dataframe


        main = open("../training/csv/csv/test.csv", 'w')
        
        for j in dataframe:
            ok = False
            if j[0] == "1":
                j = j.split(";")
                j[0] = "5"

                for k in j[:-1]:
                    main.write(str(k)+";")
                
                ok = True

            if ok is True:
                main.write("\n")













liste =  [['Fourchette', 20, 100, '../dataset/image/current/currentv0.jpg'], ['Fourchette', 20, 100, '../dataset/image/current/currentv00.jpg'], ['Cuillere', 20, 100, '../dataset/image/current/currentv000.jpg'], ['Cuillere', 20, 100, '../dataset/image/current/currentv1.jpg'], ['Fourchette', 20, 100, '../dataset/image/current/currentv1.jpg'], ['Cuillere', 20, 100, '../dataset/image/current/currentv3.jpg']]
step_height(liste)
