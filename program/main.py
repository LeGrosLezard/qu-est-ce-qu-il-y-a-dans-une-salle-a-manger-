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
def cleanning_dataset(objects_to_search):

    #['Couteau', 'Cuillère', 'Fourchette']
    #take_features_background(objects_to_search)

    take_features_multi_obj(objects_to_search)


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


    """clean_data.main"""
    objects_to_search = ['Couteau', 'Cuillère', 'Fourchette']
    cleanning_dataset(objects_to_search)


