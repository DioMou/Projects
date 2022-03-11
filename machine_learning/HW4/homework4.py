#CS 412 Homework 4 Submission Stub
#First_Name Last_Name

import numpy as np
import sklearn
from random import sample
#import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.datasets import load_digits
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_validate

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
import collections

def get_splits(n, k):
    instances=[i for i in range(0,n)]
    np.random.shuffle(instances)
    result=np.array_split(instances, k)
    #print(type(result))
    #a=[sorted(arr) for arr in result]
    a=[arr for arr in result]
    # for idx in range(len(a)-1):
    #     print('hey')
    #     if collections.Counter(a[idx]) == collections.Counter(a[idx+1]):
    #         print(idx)
    return a


def my_cross_val(method, X, y, k):
    length=len(y)
    o=get_splits(length,k)
    #print(o,len(o[0]),len(o[1]),len(o[2]),len(o[3]),len(o[4]),length)
    print(o[0])
    scaler = StandardScaler()
    #clf=getClassifier(method,x_train,y_train,x_test,y_test)
    clf=getClassifier(method)

    folds_list=[]
    errs=[]
    for arrs in o:
        X_new=np.array(X)
        Y_new=np.array(y)
        #print(X_new.shape,type(X_new))
        # scaler.fit(X_new)
        # X_new=scaler.transform(X_new)
        
        print(len(X_new))
        x_test=X_new[arrs]
        print(len(x_test))
        y_test=Y_new[arrs]
        x_train=np.delete(X_new,(arrs),axis=0)
        print(len(x_train))
        y_train=np.delete(Y_new,(arrs),axis=0)
        
        # print(X_new)
        # print(x_train.shape)
        # print(y_train.shape)
        # x_train=X_new.drop(X_new.index[arrs])
        # y_train=Y_new.drop(Y_new.index[arrs])
        
        #print(y_train)
        # print(x_train)
        # print(y_test)err=getClassifier(method,x_train,y_train,x_test,y_test)

        
        clf.fit(x_train,y_train)
        err=1-clf.score(x_test,y_test)
        errs.append(err)
    print(errs)


    return errs

def my_train_test(method, X, y, pi, k):
    length=len(y)
    rowNum=[i for i in range(0,length)]
    train_fraction=int(length*pi)
    test_fraction=length-train_fraction
    scaler = StandardScaler()
    clf=getClassifier(method)
    
    
    errs=[]
    for iter in range(0,k):
        test_idx=sample(rowNum, test_fraction)
        X_new=np.array(X)
        Y_new=np.array(y)
        # scaler.fit(X_new)
        # X_new=scaler.transform(X_new)

        x_test=X_new[test_idx]
        y_test=Y_new[test_idx]
        x_train=np.delete(X_new,(test_idx),axis=0)
        y_train=np.delete(Y_new,(test_idx),axis=0)
        #err=getClassifier(method,x_train,y_train,x_test,y_test)
        clf.fit(x_train,y_train)
        err=1-clf.score(x_test,y_test)
        errs.append(err)

    print(errs)
    return errs

def test_classification():
    name=[i for i in range(0,65)]
    rowNum=[i for i in range(0,1979)]
    temp=[0 for i in range(0,1979)]
    da=load_digits()
    bigX=da['data']
    bigY=da['target']

    
    
    #data =  pd.read_csv('optdigits.tes',names=name).astype(int)
    Method="LinearSVC"
    pi=0.75
  
    #bigX=data.iloc[:,[i for i in range(0,64)]]
    #bigY=data[64]
    clff=LinearSVC(max_iter=2000)
    #cv_results = cross_validate(clff, bigX, bigY, cv=3)
    #print(cv_results['test_score'])
    my_train_test(Method, bigX, bigY, pi, 3)
    #my_cross_val(Method,bigX,bigY,5)
    return

    o=get_splits(1797,3)
    
    
    #y=pd.concat([data.iloc[arrs] for arrs in o], axis=1)
    
    folds_list=[]
    errs=[]
    for arrs in o:
        X=data.copy()
        test=X.iloc[arrs]
        train=X.drop(X.index[arrs])
        y_train=train[64]
        x_train=train.iloc[:,[i for i in range(0,64)]]

        y_test=test[64]
        x_test=test.iloc[:,[i for i in range(0,64)]]
        #print(y_train)
        # print(x_train)
        # print(y_test)
        err=getClassifier(Method,x_train,y_train,x_test,y_test)
        errs.append(err)
    print(errs)

        #eachFold=data.iloc[arrs]
        #folds_list.append(eachFold)
        #y=pd.concat([data.iloc[arrs] for arrs in o ], axis=1)
        #print(type(eachFold))
    
    print(type(folds_list))
    print(data)
#def getClassifier(Method,x_train,y_train,x_test,y_test):
def getClassifier(Method):
    if Method =="LinearSVC":
        clf=LinearSVC(max_iter=2000)
    elif Method =="SVC":
        clf=SVC(gamma='scale',C=10)
    elif Method =='LogisticRegression':
        clf=LogisticRegression(penalty='l2',solver='lbfgs',multi_class='multinomial')
    elif Method =='RandomForestClassifier':
        clf=RandomForestClassifier(max_depth=20,random_state=0,n_estimators=500)
    elif Method == 'XGBClassifier':
        clf=GradientBoostingClassifier(max_depth=5)
    return clf
    clf.fit(x_train,y_train)
    # y_pred = clf.predict(x_test)   
    # err = 1 - np.sum(y_pred == y_test)/(y_pred.shape[0])
    err=1-clf.score(x_test,y_test)
    return err

        


        

if __name__=='__main__':
    test_classification()
