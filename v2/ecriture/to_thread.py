import os
import threading
from picture_operation.dimension import main_demension


path_data = "dataset/image/dataset"
path_folder = "dataset/image/dataset/{}"

liste_path = os.listdir(path_data)

def a(path):
    Lm = 0;lcm = 0;nb=0;
    liste = os.listdir(path)
    for i in liste:
        L, l = main_demension(path + i)
        Lm += L; lcm+=l;nb += 1;
    print(Lm/nb, lcm/nb)

def main_threading():
    thread_0 = threading.Thread(target=a(path_folder.format(liste_path[0])))

    thread_1 = threading.Thread(target=a(path_folder.format(liste_path[1])))

    thread_2 = threading.Thread(target=a(path_folder.format(liste_path[2])))

    thread_3 = threading.Thread(target=a(path_folder.format(liste_path[3])))

    thread_4 = threading.Thread(target=a(path_folder.format(liste_path[4])))

    thread_5 = threading.Thread(target=a(path_folder.format(liste_path[5])))

    thread_6 = threading.Thread(target=a(path_folder.format(liste_path[6])))

    thread_7 = threading.Thread(target=a(path_folder.format(liste_path[7])))



    thread_0.start()

    thread_1.start()

    thread_2.start()

    thread_3.start()

    thread_4.start()

    thread_5.start()

    thread_6.start()

    thread_7.start()



    thread_0.join()

    thread_1.join()

    thread_2.join()

    thread_3.join()

    thread_4.join()

    thread_5.join()

    thread_6.join()

    thread_7.join()

