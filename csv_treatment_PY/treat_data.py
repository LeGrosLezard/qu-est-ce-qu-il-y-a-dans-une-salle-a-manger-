import csv
import os
import cv2

def csv_write():
    with open('../csv/csv_model.csv', 'w') as file:
        writer = csv.writer(file)
        file.write("label;")
        for i in range(0, 2500):
            file.write("pixel"+str(i)+";")

        file.write("\n")


def reshape_thresh(thresh):
    thresh = cv2.resize(thresh, (50, 50))
    return thresh


def to_list(thresh):

    data = []
    for i in range(thresh.shape[0]):
        for j in range(thresh.shape[1]):
            if thresh[i, j] > 120:
                nb = 1
            else:
                nb = 0
        
            data.append(nb)

    return data



def write_data_into_csv(data, label):

    with open('../csv/csv_model.csv', 'a') as file:
        writer = csv.writer(file)
        file.write(label+";")
        for i in data:
            file.write(str(i)+";")

        file.write("\n")


def csv_file_label(label, liste, path):
    
    for i in liste:

        img = cv2.imread(path.format(i), 0)
        img = cv2.medianBlur(img, 5)

        th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                    cv2.THRESH_BINARY,11,2)

        th3 = reshape_thresh(th3)

        data = to_list(th3)
        write_data_into_csv(data, label)




def data_treatment():

    #assiette
    folder_assiette = r"C:\Users\jeanbaptiste\Desktop\assiette\image\assiette"
    path_assiette = "../image/assiette/{}"

    #negative path (buffy)
    folder_negative = r"C:\Users\jeanbaptiste\Desktop\assiette\image\N"
    path_negative = "../image/N/{}"

    #les listes des directions
    liste_assiette = os.listdir(folder_assiette)
    liste_negative = os.listdir(folder_negative)

    #on ecrit le head (label + pixel1 -> 2500)
    csv_write()

    #on ecrit le label + les pixel
    csv_file_label("0", liste_assiette, path_assiette)
    csv_file_label("1", liste_negative, path_negative)









if __name__ == "__main__":
    data_treatment()































