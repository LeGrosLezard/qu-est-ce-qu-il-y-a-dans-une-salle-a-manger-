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
        En gros on fait les crop
        les marges pour mettre manche
    """

    detection_picture(model, image)



from detection.detection import detection_picture_hog
def detection_object(model, image, number_label, label, path):

    """
        on fait la detection des objets via
        les crop des images sans marge !
    """


    liste = os.listdir(path)
    for i in liste:
        image = str(path) + str(i)
        detection_picture_hog(number_label, label, model, image)











if __name__ == "__main__":

    model = "models/miammiamsvmImage"
    image = "dataset/assiette_couvert/assiette1.jpg"
    path_to_analysis = "dataset/data_analysing/"

    number_label, label = our_object()

    detect_objects(model, image)
    #detection_object(model, image, number_label, label, path_to_analysis)















