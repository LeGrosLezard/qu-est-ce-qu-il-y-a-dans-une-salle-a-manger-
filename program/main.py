import os
import cv2

from label.search_label import element_in_label_PY
def our_object():

    """
        En gros c la ou on met les label 1:assiette
    """
    
    number_label, label = element_in_label_PY()
    return number_label, label


from detection.crop_objects import detection_picture
def detect_objects(model, image):

    """
        En gros on fait les crop des objets
        dans l'image (segmentation mieux)
        les marges pour mettre manche
    """

    detection_picture(model, image)



from detection.detection import detection_picture_hog
def detection_object(model, image, number_label, label,
                     path_analysis):

    """
        on fait la detection des objets via
        les crop des images sans marge !
        sinon on cherche
    """

    #image dans le dossier
    liste = os.listdir(path_analysis)

    objects = []
    objects_detected = []

    for i in liste:
        if i not in ("crop_learning", "show"):
            image = str(path_analysis) + str(i)
            detected = detection_picture_hog(number_label, label, model, image)

            objects.append(image)
            objects_detected.append(detected)

    return objects, objects_detected



from searching_data.object_category import our_dico_path_url
from searching_data.object_category import searching_category
from searching_data.object_category import other_element_from_category
from searching_data.object_category import transform_category_to_object

def search_objet(objects, objects_detected, OBJECT_SEARCHING):


    our_path = our_dico_path_url()


    for i in range(len(objects)):
        if objects_detected[i] is None:
            OBJECT_SEARCHING.append(objects[i])
            print(objects[i], "no found")


    for i in range(len(objects)):
        if objects_detected[i] is not None:

            print(objects[i], "Found\n")
            category = searching_category(objects_detected[i], our_path)

            category_found = other_element_from_category(category,
                                                         objects_detected[i],
                                                         our_path)

            objects_to_search = transform_category_to_object(category_found, our_path)

    return objects_to_search 



from download_data.download_data import transform_i
from download_data.download_data import main_download
def download_picture(objects_to_search):

    for objects in objects_to_search:
        objects = transform_i(objects)
        main_download([objects], [200], [0], "dataset/")



from clean_data.background import take_features_background
from clean_data.multiple_object import take_features_multi_obj
from clean_data.position_object import take_features_position
from clean_data.deleting import main_deleting
def cleanning_dataset(objects_to_search):

    #['Couteau', 'Cuillère', 'Fourchette']
    
    save = "dataset/clean/"

    for objects in objects_to_search:
        os.makedirs("dataset/clean/" + str(objects))

        liste = os.listdir("dataset/" + str(objects))

        number = 0
        for picture in liste:
            
            save = "dataset/clean/" + str(objects) + "/{}.jpg"
            picture = str("dataset/") + str(objects) + "/" + str(picture)

            take_features_background(picture, save.format(str(number)))
            number += 1


    for objects in objects_to_search:
        liste = os.listdir("dataset/clean/" + str(objects))
        for picture in liste:

            picture = str("dataset/clean/") + str(objects) + "/" + str(picture)
            take_features_multi_obj(picture)
            take_features_position(picture)



    for objects in objects_to_search:
        liste = os.listdir("dataset/clean/" + str(objects))

        for image in liste:

            picture = "dataset/clean/" + str(objects) + "/{}"

            delete = main_deleting(picture.format(str(image)))
            #show_picture("dza", img, 0, "")

            if delete is True:
                    os.remove(picture.format(str(image)))
                    print("DELETED")




from training.crop_object import main_croping
def croping_data(objects_to_search):

    objects_to_search = ['Cuillere', 'Couteau', 'Fourchette']
    for objects in objects_to_search:
        
        liste = os.listdir("dataset/clean/" + str(objects))

        for picture in liste:

            picture = str("dataset/clean/") + str(objects) + "/" + str(picture)    
            print(picture)
            crop = main_croping(picture)

            cv2.imwrite(picture, crop)



from training.course_object import main_couse
from training.to_csv import verify_name_csv
from training.to_csv import csv_write
from training.to_model import csv_to_data
from training.to_model import training
from training.to_model import verify_name
def trainning(objects_to_search):


    csv_name = verify_name_csv()
    csv_write(csv_name, 10000)
    print(csv_name)


    dico_label = {}
    for nb, objects in enumerate(objects_to_search):
        dico_label[objects] = nb


    print(dico_label)

    for objects in objects_to_search:
        
        liste = os.listdir("dataset/clean/" + str(objects))
        path_crop = "dataset/clean/" + str(objects) + "crop"

 
        for picture in liste:

            picture = str("dataset/clean/") + str(objects) + "/" + str(picture)    

            print(picture)

            for key, value in dico_label.items():
                if key == objects:
                    label = value
            main_couse(picture, csv_name, str(label))


    csv_name = "_in_training.csv"
    name = verify_name()
    data, label = csv_to_data(csv_name)
    training(data, label, name)


from searching_data.caracteristics import properies_object
from searching_data.caracteristics import treat_element
def detection_trainning(objects_to_search):


    element = properies_object(objects_to_search)
    carac = treat_element(element) 
    print(carac)



if __name__ == "__main__":

    model = "models/miammiamsvmImage"
    image = "dataset/assiette_couvert/assiette1.jpg"
    path_to_analysis = "dataset/data_analysing/"

    OBJECT_SEARCHING = []

    #1 on coupe tout -> detecter par exemple un manche
    #2 on fait une detection pour voir si on a l'objet
    #3 si on a objet afficher
    #4 si on a pas objet: rechercher

    """label.search_label.py"""
    number_label, label = our_object()

    """detection.crop_objects"""
    #detect_objects(model, image)

    """detecion.detection"""
    #objects, objects_detected\
    #= detection_object(model, image, number_label, label,
    #                   path_to_analysis)

    """searching_data.object_category"""
    #objects_to_search = search_objet(objects, objects_detected, OBJECT_SEARCHING)


    """download_data.download_data"""
    #download_picture(objects_to_search)


##    """clean_data.main"""

    #cleanning_dataset(objects_to_search)

    objects_to_search = ['Cuillere', 'Couteau', 'Fourchette']
    #croping_data(objects_to_search)

    #trainning(objects_to_search)

    detection_trainning(objects_to_search)
