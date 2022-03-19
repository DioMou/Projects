import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

# reading from the file
name=["class","cap-shape","cap-surface","cap-color","bruises?","odor","gill-attachment","gill-spacing","gill-size","gill-color","stalk-shape"
,"stalk-root", "stalk-surface-above-ring","stalk-surface-below-ring", "stalk-color-above-ring", "stalk-color-below-ring", "veil-type","veil-color"
, "ring-number", "ring-type", "spore-print-color", "population", "habitat"]
data =  pd.read_csv('agaricus-lepiota.data',names=name)
feature=data[["cap-shape","cap-surface","cap-color","bruises?","odor","gill-attachment","gill-spacing","gill-size","gill-color","stalk-shape"
,"stalk-root", "stalk-surface-above-ring","stalk-surface-below-ring", "stalk-color-above-ring", "stalk-color-below-ring", "veil-type","veil-color"
, "ring-number", "ring-type", "spore-print-color", "population", "habitat"]]

                        

rf_classifier = RandomForestClassifier(
                      min_samples_leaf=50,
                      n_estimators=150,
                      bootstrap=True,
                      oob_score=True,
                      n_jobs=-1,
                      random_state=42,
                      max_features='auto')
b=data["class"].astype("category").cat.codes#since created dummy, each columns was seperated into more columns, we need original class column to make sure train test split works properly 
#since test column has to be a single column
hot=pd.get_dummies(data)
print(hot)
b=pd.concat([hot, b.rename("class")], axis=1)
b= b.drop(["class_e","class_p"], axis = 1)#drop the seperated class columns
x_train, x_test, y_train, y_test = train_test_split(
            b, b["class"], test_size=0.2, random_state=42)
print(y_train)
print(x_train)
rf_classifier.fit(x_train,y_train)
predictions = rf_classifier.predict(x_test)
print(confusion_matrix(y_test,predictions))
# for n in name:
#     a=data[n].astype("category").cat.codes
#     b=pd.concat([b, a.rename(n)], axis=1)
# print(b,"more")

# x_train, x_test, y_train, y_test = train_test_split(
#             feature, data["class"], test_size=0.33, random_state=42)
# OHE=OneHotEncoder()
# OHE.fit(data)
# result=OHE.transform(x_train).toarray()
# print(result)
# print(x_train)
# print(y_train)
# a=rf_classifier.fit(x_train,y_train)
# print(data)

