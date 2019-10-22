import os


#Main function picture
from main_function_image import open_picture
from main_function_image import show_picture
from main_function_image import save_picture
from main_function_image import to_crop

#Background
from picture_operation.background import main_background

#multiple objects
from picture_operation.multiple_objects import take_features_multi_obj

#rotation objects
from picture_operation.picture_orientation import take_features_position

#----
"""
    Il faut faire l'apprentissage de l'assiette
    hors programme la
"""
#----

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
    img = take_features_multi_obj(path_picture)

    liste = os.listdir(path_current)
    for i in liste:

        im = path_current + i
        img = open_picture(im)
        show_picture("display", img, 1, "y")

    print("Separate objects finish")


    print("Reposition of objects... ")
    liste = os.listdir(path_current)
    for i in liste:
        if i != "current.jpg":
            img = path_current + i
            img = take_features_position(img)
            img = to_crop(img)
            save_picture(str(path_current + i), img)
            show_picture("display", img, 1, "y")

    print("Reposition of objects finsh")

    print("\nTreatment finish")



from object_detection.objects_detection import detection
from dataset.information_data.labels_function import treatment_read
from dataset.information_data.labels_function import read
def step_two():

    print("Detection in progress ...")

    
    path_current = "dataset/image/current/"
    path_models = "training/models/models/"
    path_label = "dataset/information_data/label.py"

    liste_picture = os.listdir(path_current)
    model_list = os.listdir(path_models)

    detections = 0

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
                        print("Pas le meme model")

                    if prediction == information["label"]:
                        print(information["name"])

                    print(prediction)
                    show_picture("picture", img, 0, "y")


                
    














def main():
    #step_one()
    step_two()











if __name__ == "__main__":
    main()
