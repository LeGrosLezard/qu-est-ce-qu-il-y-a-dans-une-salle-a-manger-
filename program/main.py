from label.search_label import element_in_label_PY

from detection.crop_objects import detection_picture
from detection.detection import detection_picture_hog




def detection_object():

    """
        We recup the label from label.py
        we try to detect one of label from model
    """

    number_label, label = element_in_label_PY()
    detection_picture_hog(number_label, label)











if __name__ == "__main__":
    detection_object()















