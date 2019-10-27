import os
import shutil



def read_label(path_label, label):

    liste = []
    with open(path_label, "r") as file:
        for i in file:
            liste.append(i)

    liste1 = []
    for i in liste:
        i = i.split(";")
        for j in label:
            if j == i[1] and i[0] == "None":
                i[0] = i[1]
                liste1.append(";".join(i))
            elif i[0] not in "None":
                liste1.append(";".join(i))

    return list(set(liste1))

def updatet_label(path_label, label):

    with open(path_label, "w") as file:
        for i in label:
            file.write(i)


def step_height(liste, path_label, path_models_training, path_model):

    label = list(set([i[0] for i in liste]))

    labels = read_label(path_label, label)
    updatet_label(path_label, labels)
 
    liste_training = os.listdir(path_models_training)
    

    for i in liste_training:
        for j in label:
            if j == i:
                shutil.move(path_models_training + "/" +  i, path_model + "/" + i)
