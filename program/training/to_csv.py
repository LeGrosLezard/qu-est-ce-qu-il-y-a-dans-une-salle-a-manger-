import csv
import os



def verify_name_csv():

    name = str("_in_training.csv")
    path = "csv"

    c = 0

    liste = os.listdir(path)
    no_save = True;
    while no_save:

        same = False
        for url in liste:

            if url == name:
                name = str(name[:-4]) + str(c) + ".csv"
                same = True
                c+=1

            if same is False:
                no_save = False

    print(name)
    return name



def csv_write(name, rnge):
    path_csv = "csv/" + str(name)
    with open(path_csv, 'w') as file:
        writer = csv.writer(file)
        file.write("label;")
        for i in range(0, rnge):
            file.write("histo"+str(i)+";")

        file.write("\n")




def write_data_into_csv(name, label, data):

    with open("csv/" + str(name), 'a') as file:
        writer = csv.writer(file)
        file.write(label+";")
        for i in data:
            file.write(str(i)+";")

        file.write("\n")















