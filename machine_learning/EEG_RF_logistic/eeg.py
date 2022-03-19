import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from scipy.io import arff
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics 
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict
from sklearn.svm import LinearSVC

data = arff.loadarff('EEG Eye State.arff')
df = pd.DataFrame(data[0])
b=df["eyeDetection"].astype("category").cat.codes
b=pd.concat([df, b.rename("class")], axis=1)
print(b)
b= b.drop(["eyeDetection"], axis = 1)#drop the seperated class columns
p=b.copy()
p=p.drop(["class"], axis = 1)
#b=pd.concat([df, b.rename("class")], axis=1)
print(p)
x_train, x_test, y_train, y_test = train_test_split(
            p, b["class"], test_size=0.2, random_state=42)
#random forest
rf = RandomForestClassifier(
                      max_depth=2,
                      n_estimators=100)
rf.fit(x_train, y_train)
predictions = rf.predict(x_test)
print(confusion_matrix(y_test,predictions))
print(metrics.accuracy_score(y_test, predictions))

#decision tree
clf = DecisionTreeClassifier(max_depth=50)
clf.fit(x_train, y_train)
decision_tree_predictions = clf.predict(x_test)
print(confusion_matrix(y_test,decision_tree_predictions),"decision tree")
print(metrics.accuracy_score(y_test, decision_tree_predictions))


#linear logistic regression
logis=LogisticRegression(penalty='l2',solver='lbfgs',multi_class='multinomial')
logis_prediction = cross_val_predict(logis, p, b["class"], cv=5)
print(confusion_matrix(b["class"],logis_prediction),"logistic regression_cv")
print(metrics.accuracy_score(b["class"], logis_prediction),"cv")
logis_o=LogisticRegression(penalty='l2',solver='lbfgs',multi_class='multinomial')
logis_o.fit(x_train, y_train)
logis_pre=logis_o.predict(x_test)
print(confusion_matrix(y_test,logis_pre),"train_test_split")
print(metrics.accuracy_score(y_test, logis_pre),"train test split")

#linearSVC
linear=LinearSVC(max_iter=2000)
l_prediction = cross_val_predict(linear, p, b["class"], cv=5)
print(confusion_matrix(b["class"],l_prediction),"linear svc_cv")
print(metrics.accuracy_score(b["class"], l_prediction))
linear_o=LinearSVC(max_iter=2000)
linear_o.fit(x_train, y_train)
l_pre=linear_o.predict(x_test)
print(confusion_matrix(y_test,l_pre),"train_test_split")
print(metrics.accuracy_score(y_test, l_pre),"train test split")


