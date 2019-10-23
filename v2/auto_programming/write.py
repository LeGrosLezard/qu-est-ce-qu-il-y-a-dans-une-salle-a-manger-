import importlib
import to_thread




def writtte(number):

    with open('to_thread.py', 'w') as file:

        file.write("import os\n")
        file.write('import threading\n')

        file.write('from picture_operation.dimension import main_demension\n\n\n')






        file.write('path_data = "dataset/image/dataset"\n')
        file.write('path_folder = "dataset/image/dataset/{}"\n\n')
        file.write('liste_path = os.listdir(path_data)\n\n')



        dico = {1:"a", 2:"b", 3:"c", 4:"d",
                5:"e", 6:"f", 7:"g", 8:"h", 9:"i"}


        file.write('def a(path):\n')
        file.write('    Lm = 0;lcm = 0;nb=0;\n')
        file.write('    liste = os.listdir(path)\n')
        file.write('    for i in liste:\n')
        file.write('        L, l = main_demension(path + i)\n')
        file.write('        Lm += L; lcm+=l;nb += 1;\n')

        
        file.write('    print(Lm/nb, lcm/nb)\n\n')




        file.write('def main_threading():\n')
        for i in range(number):
            file.write('    thread_' + str(i) + ' = threading.Thread(target=a(path_folder.format(liste_path[' + str(i) + '])))\n\n')

        file.write('\n\n')

        for i in range(number):
            file.write('    thread_' + str(i) + '.start()\n\n')

        file.write('\n\n')

        for i in range(number):
            file.write('    thread_' + str(i) + '.join()\n\n')




    importlib.reload(to_thread)



writtte(8)









    
    
    


