import pandas as pd
import matplotlib.pyplot as plt  
from sklearn import svm
from sklearn import metrics
import joblib
from sklearn.decomposition import PCA
import numpy as np
from sklearn.utils import shuffle



file =  open('../csv/csv_model.csv', 'r')
    
dataframe = file.readlines()
dataframe = dataframe[1:]

X = []
Y = []

for i in dataframe:
    liste_w = []
    for j in i:
        if j == "\n":
            X.append(liste_w)
            liste_w = []
        else:
            if j == ";" or j == " ":
                pass
            else:
                try:
                    j = int(j)
                    liste_w.append(int(j))
                except:
                    liste_w.append(str(j))


for i in X:
    Y.append(i[0])
    del i[0]



X_train, Y_train =  X, Y
X_test,Y_test = X, Y


model = svm.SVC(kernel="linear",C=2)
model.fit(X_train,Y_train)
joblib.dump(model, "../model/miammiam_model") 
predictions = model.predict(X_test)

print("Score", metrics.accuracy_score(Y_test, predictions))












