import os
import threading

#Main function picture
from main_function_image import open_picture
from main_function_image import show_picture
from main_function_image import save_picture
from main_function_image import to_crop
from main_function_image import write_position

#Background
from picture_operation.background import main_background

#multiple objects
from picture_operation.multiple_objects import take_features_multi_obj

#rotation objects
from picture_operation.picture_orientation import take_features_position



def step_one():
    """
        Input image
    """
    
    path_picture = "dataset/image/current/current.jpg"
    path_current = "dataset/image/current/"
    oInput = input("Enter an image")

    oInput = r"C:\Users\jeanbaptiste\Desktop\assiette\v2\dataset\image\test\assiette1.jpg"
    img = open_picture(oInput)
    save_picture(path_picture, img)

    print("Treatement in progress... \n")

    print("Treatment Background in progress ...")
    img = main_background(path_picture)
    save_picture(path_picture, img)
    print("Treatment Background finish")
    show_picture("img", img, 1, "y")


    print("Separate objects...")
    img = take_features_multi_obj(path_picture, "")

    liste = os.listdir(path_current)
    for i in liste:
        
        im = path_current + i
        img = open_picture(im)

        if i not in ("current.jpg", "current_copy"):
            print("Recuperate position")
            _, positionx, positiony = to_crop(img)
            write_position(positionx, positiony, str(im))

        show_picture("display", img, 1, "y")

    print("Separate objects finish")


    print("Reposition of objects... ")
    liste = os.listdir(path_current)
    for i in liste:
        if i not in ("current.jpg", "current_copy"):
            img = path_current + i
            img = take_features_position(img)

            img, _, _ = to_crop(img)
            save_picture(str(path_current + i), img)
            show_picture("display", img, 1, "y")

    print("Reposition of objects finsh")

    print("\nTreatment finish")



#Detection
from object_detection.objects_detection import detection

#Label
from dataset.information_data.labels_function import treatment_read
from dataset.information_data.labels_function import read

#Main function
from main_function_image import recup_position
from main_function_image import draw

def step_two():

    print("Detection in progress ...")

    path_current = "dataset/image/current/"
    path_models = "training/models/models/"
    path_label = "dataset/information_data/label.py"

    liste_picture = os.listdir(path_current)
    model_list = os.listdir(path_models)

    detections = []
    images = []
    for picture in liste_picture:

        if picture != "current.jpg":

            image = path_current + str(picture)
            img = open_picture(image)

            for models in model_list:
                model = path_models + str(models)

                labels = read(path_label, str(models))
                for lab in labels:
                    information = treatment_read([lab])

                    w = int(information["dimension"][0])
                    h = int(information["dimension"][1])

                    try:
                        prediction = detection(model, w, h, img)
                    except:
                        pass

                    if prediction == int(information["label"]):
                        detections.append([information["name"],
                                           recup_position(image)])
                        images.append(image)
                        break
                    else:
                        detections.append(["", recup_position(image)])
                        images.append(image)
                        break
        
                    #show_picture("picture", img, 1, "y")


    #print(detections)

    for nb, i in enumerate(detections):

        if i[1] == None:pass
        else:
            img = draw(i, nb, images[nb])
            show_picture("display", img, 1, "y")
            save_picture("dataset/image/current/current_copy.jpg", img)


    return detections



from scraping.object_category import main_scrap
from scraping.download_data import download_picture
def step_three(detection):

    #Scrap
    liste = []
    for i in detection:
        items = main_scrap(i)
        for it in items:
            liste.append(it)


    liste_path = os.listdir("dataset/image/dataset")
    for i in liste:
        for j in liste_path:
            if i == j:
                liste.remove(i)

    #Download
    for i in liste:
        path = "dataset/image/dataset/"
        download_picture(i, path.format(i))


    return liste
    


from picture_operation.delete import main_deleting
from picture_operation.multiple_objects import take_features_multi_obj
from picture_operation.picture_orientation import take_features_position
from picture_operation.background import main_background
def step_fourth(objects):

    path_data = "dataset/image/dataset"
    path_folder = "dataset/image/dataset/{}"
    path_image = "dataset/image/dataset/{}/{}"
    liste_path = os.listdir(path_data)
    print(liste_path)

    for i in liste_path:

        picture_folder = os.listdir(path_folder.format(i))
        print(path_folder.format(i))

        for j in picture_folder:

            print(path_image.format(i, j))
            img = main_background(path_image.format(i, j))
            save_picture(path_image.format(i, j), img)


        for j in picture_folder:
            print(path_image.format(i, j))
            img = take_features_multi_obj(path_image.format(i, j))


        for j in picture_folder:
            print(path_image.format(i, j))
            img = take_features_position(path_image.format(i, j))
            save_picture(path_image.format(i, j), img)


        for j in picture_folder:
            print(path_image.format(i, j))
            delete = main_deleting(path_image.format(i, j))
            if delete is True:
                os.remove(path_image.format(i, j))









from training.training import head_writting
from training.training import picture_writting
from training.training import train
from ecriture.write import writtte
import importlib
def step_five():

    path_data = "dataset/image/dataset"

    liste_path = os.listdir(path_data)
    print(len(liste_path))

    liste = []

    write = writtte(len(liste_path))
    if write:
        from ecriture.to_thread import main_threading
        liste = main_threading()

    print(liste)
    return liste


from main_function_image import define_size
from main_function_image import negativ_training
from training.training import head_writting
from training.training import picture_writting
from training.training import train
from dataset.information_data.labels_function import write_labels
def step_six(liste):

    #Verify csv

    path_data = "dataset/image/dataset"
    path_folder = "dataset/image/dataset/{}"
    path_image = "dataset/image/dataset/{}/{}"
    liste_path = os.listdir(path_data)
    path_label = "dataset/information_data/label.py"


    for i in liste_path:
        print(i)

        picture_folder = os.listdir(path_folder.format(i))

        if len(picture_folder) > 10 and i != "assiette":

            for info_size in liste:
                if info_size[2] == path_folder.format(i):
                    size = define_size(info_size)
                    number_pix = size[0] * size[1]
                    write_labels(path_label, "None", str(i),
                                 "None", str(size[0]), str(size[1]), "None")

            csv_name = "training/csv/in_training/" + str(i) + ".csv"
            model_name = "training/models/in_training/" + str(i)

            head_writting(csv_name, number_pix)

            picture_writting(csv_name,
                             path_folder.format(i),
                             "", 
                             size[0], size[1], "1")

            negativ_training(i, csv_name, size)


            train(csv_name, model_name)



def step_seven():

    print("Detection in progress ...")

    path_current = "dataset/image/current/"
    path_models = "training/models/in_training/"
    path_label = "dataset/information_data/label.py"

    liste_picture = os.listdir(path_current)
    model_list = os.listdir(path_models)

    detections = []
    images = []


    for picture in liste_picture:

        if picture != "current.jpg" and\
           picture != "current_copy.jpg":

            image = path_current + str(picture)

            img = open_picture(image)

            for models in model_list:

                model = path_models + str(models)

                labels = read(path_label, str(None))


                for lab in labels:
                    information = treatment_read([lab])

                    w = int(information["dimension"][0])
                    h = int(information["dimension"][1])

                    try:
                        prediction = detection(model, w, h, img)
                        print(models, prediction)
                    except:
                        pass

                    if prediction == 1:
                        detections.append([information["name"], models])
                        images.append(image)

                    else:
                        pass


                    show_picture("picture", img, 1, "y")


    print(detections)



def main():
    #step_one()
    #detection = step_two()

##    via = []
##    for i in detection:
##        if i[0] not in ("?") and\
##           i[1] != None :
##            via.append(i[0])

    #liste = step_three(via)
    #print("\n We need to search this in a first time: ", liste)
    #step_fourth(objects)
    #liste = step_five()
    liste = [[4.385468750000137, 2.9368750000000916, 'dataset/image/dataset/aliment'], [3.3115911458334373, 2.2479661458334026, 'dataset/image/dataset/bol'], [4.904211387434708, 1.5215619546248298, 'dataset/image/dataset/Couteau'], [4.7288758680557015, 1.298111979166708, 'dataset/image/dataset/Cuillere'], [4.772159391534541, 0.9914175485009131, 'dataset/image/dataset/Fourchette'], [4.148116883117012, 2.142094155844224, 'dataset/image/dataset/Paille'], [2.9227008928572342, 2.185962301587369, 'dataset/image/dataset/tasse'], [3.5509643817205414, 2.5156754032258855, 'dataset/image/dataset/verre']]

    step_six(liste)
    #step_seven()








if __name__ == "__main__":
    main()
