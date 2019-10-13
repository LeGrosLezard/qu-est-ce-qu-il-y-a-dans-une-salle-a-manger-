import os


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



def chercher_objet(objects, objects_detected):
    pass




if __name__ == "__main__":

    model = "models/miammiamsvmImage"
    image = "dataset/assiette_couvert/assiette1.jpg"
    path_to_analysis = "dataset/data_analysing/"


    #1 on coupe tout -> detecter par exemple un manche
    #2 on fait une detection pour voir si on a l'objet
    #3 si on a objet afficher
    #4 si on a pas objet: rechercher


    number_label, label = our_object()

    #detect_objects(model, image)


    objects, objects_detected\
    = detection_object(model, image,
                       number_label, label,
                       path_to_analysis)

    chercher_objet(objects, objects_detected)













