import os
import csv
import importlib




path = r"C:\Users\jeanbaptiste\Desktop\assiette\v2\training\csv\test\miammiamsvmImage.csv"


file =  open(path, 'r')

dataframe = file.readlines()

liste = []
for i in dataframe:
    liste.append(i[0])

liste = list(set(liste))


chiffre = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]


counter_chiffre = 0
for i in liste:
    for nb in chiffre:
        if i == nb:
            counter_chiffre += 1

if counter_chiffre == 10:
    print("ouiiii")

def write_into_file():
    with open('test2.py', 'a') as file:
        file.write('aa = "5"\n')
        file.write('bb = "5"\n')
        file.write('bb = "65555555555555"\n')
    importlib.reload(test2)















