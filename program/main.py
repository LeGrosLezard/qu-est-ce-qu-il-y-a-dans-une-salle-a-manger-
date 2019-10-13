import os


from label.search_label import element_in_label_PY
def our_object():
    number_label, label = element_in_label_PY()
    return number_label, label

from detection.crop_objects import detection_picture
def detect_objects(model, image):
    detection_picture(model, image)



from detection.detection import detection_picture_hog
def detection_object(model, image, number_label, label, path):

    """
        We recup the label from label.py
        we try to detect one of label from model
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
    detection_object(model, image, number_label, label, path_to_analysis)















