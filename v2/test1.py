import importlib
import test2

def a():
    with open('test2.py', 'a') as file:
        file.write('aa = "5"\n')
        file.write('bb = "5"\n')
        file.write('bb = "65555555555555"\n')
    importlib.reload(test2)
         
def b():
    print(test2.aa)
    print(test2.bb)


a()
b()
