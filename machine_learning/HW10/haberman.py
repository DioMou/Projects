import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

name=["age","year","Number of positive axillary nodes", "class"]
data =  pd.read_csv('haberman.data',names=name)
feature=data[["age","year","Number of positive axillary nodes"]]
rf_classifier = RandomForestClassifier(
                      n_estimators=100,
                      max_depth=50)
x_train, x_test, y_train, y_test = train_test_split(
            feature, data["class"], test_size=0.2, random_state=42)
print(y_train)
print(x_train)
rf_classifier.fit(x_train,y_train)
predictions = rf_classifier.predict(x_test)
print(confusion_matrix(y_test,predictions),"rf")

#decision tree
clf = DecisionTreeClassifier(max_depth=50,random_state=42)
clf.fit(x_train, y_train)
decision_tree_predictions = clf.predict(x_test)
print(confusion_matrix(y_test,decision_tree_predictions),"decision tree")