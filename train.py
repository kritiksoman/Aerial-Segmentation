
import csv
import numpy as np
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from itertools import *
from numpy import genfromtxt
import graphviz
from sklearn.externals import joblib

a = genfromtxt('train.csv', delimiter=',')

N=len(a)
#a = np.random.permutation(a)

data = a[:,1:6]
#data = preprocessing.scale(data)#for zero mean and unit variance
labels = a[:,6]
f=['nh','h','nd','s','tnd']
#X_train, X_test, y_train, y_test = train_test_split(data, labels, random_state=1)

print(data.shape,labels.shape,a.shape)
clf = tree.DecisionTreeClassifier()
#criterion = "gini", random_state = 100,max_depth=3)
clf.fit(data, labels)

y_predict = clf.predict(data)
print accuracy_score(labels, y_predict)



dot_data = tree.export_graphviz(clf, out_file=None)
graph = graphviz.Source(dot_data)
graph.render("roofModel")
dot_data = tree.export_graphviz(clf, out_file=None, feature_names=f,class_names=['g','ng'],filled=True, rounded=True, special_characters=True)

graph = graphviz.Source(dot_data)
graph

joblib.dump(clf, 'groundTreeModel.pkl') 
