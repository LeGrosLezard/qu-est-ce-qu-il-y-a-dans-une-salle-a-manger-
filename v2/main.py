import os


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
    img = take_features_multi_obj(path_picture)

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

    print(detections)
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

    #Download
    for i in liste:

        path = "dataset/image/dataset/{}"
        download_picture(i, path.format(i))






def main():
    #step_one()
    #detection = step_two()

##    via = []
##    for i in detection:
##        if i[0] not in ("?") and\
##           i[1] != None :
##            via.append(i[0])


    via = ['assiette']
    step_three(via)










if __name__ == "__main__":
    main()
