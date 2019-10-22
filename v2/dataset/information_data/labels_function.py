
path_label = r"C:\Users\jeanbaptiste\Desktop\assiette\v2\dataset\information_data\label.py"

def write(path_label):
    with open(path_label, "a") as file:
        pass





#RECUP PART

def read(path_label, model_number):

    informations = [];
    
    with open(path_label, "r") as file:

        for i in file:
            increment=""

            for j in i:
                stop = False;

                if j == ";":
                    if increment == model_number:
                        informations.append(i)
                        increment = ""
                        stop = True

                if stop is True:
                    break

                increment += j

    return informations





def treatment_read(liste):

    informations_object = {"csv_name":"", "name":"", "label":"",
                           "part_object":[], "dimension":[]}
    
    liste = liste[0].split(";")

    informations_object["csv_name"] = liste[0]
    informations_object["name"] = liste[1]
    informations_object["label"] = liste[2]

    increment = ""
    for i in liste[3]:
        if i == ",":
            informations_object["part_object"].append(increment)
            increment = ""
        increment += i

    informations_object["part_object"].append(increment)


    increment = ""
    for i in liste[4]:

        incrementation = True
        if i == "x":
            informations_object["dimension"].append(increment)
            increment = ""
            incrementation = False

        if incrementation is True:
            increment += i

    informations_object["dimension"].append(increment)

    print(informations_object)
    return informations_object

