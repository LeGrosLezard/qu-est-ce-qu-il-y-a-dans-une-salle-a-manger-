import os


#Main function picture
from main_function_image import open_picture
from main_function_image import show_picture
from main_function_image import save_picture

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
    
    path_picture = "dataset/current/current.jpg"
    path_current = "dataset/current/"
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
            save_picture(str(path_current + i), img)
            show_picture("display", img, 1, "y")
            
    print("Reposition of objects finsh")

    print("\nTreatment finish")


def main():
    step_one()












if __name__ == "__main__":
    main()
