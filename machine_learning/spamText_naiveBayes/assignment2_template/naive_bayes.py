# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018

"""
This is the main entry point for Part 1 of this MP. You should only modify code
within this file for Part 1 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import collections
import math
from decimal import *

class phrase:
    def __init__(self, name,count):
        self.name=name
        self.count=count
    def __hash__(self):
        return hash(str(self.name))
    def __eq__(self, other):
        return self.name == other
    def __str__(self):
        return "name and count " +str(self.name)+str(self.count) 

def naiveBayes(train_set, train_labels, dev_set, smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each email
    example: suppose I had two emails 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two emails, first one was ham and second one was spam.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each email that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter --laplace (1.0 by default)
    pos_prior - positive prior probability (between 0 and 1)
    """
    # TODO: Write your code here
    # return predicted labels of development set
    hamCounter=collections.Counter()
    spamCounter=collections.Counter()
    
    hamPosteriorDict={}
    spamPosteriorDict={}
    sumHam=0.0
    sumSpam=0.0
    resultLableList=[]
    for eachSetIndex in range(len(train_labels)):
        if train_labels[eachSetIndex] == 1:#ham label counter
            hamCounter.update(train_set[eachSetIndex])
            sumHam=sumHam+len(train_set[eachSetIndex])
        elif train_labels[eachSetIndex] == 0:#spam label counter 
            spamCounter.update(train_set[eachSetIndex])
            sumSpam=sumSpam+len(train_set[eachSetIndex])
    totalCounter=len(hamCounter+spamCounter)
    #with open('hamcounter.txt','w') as filehandle:
        #for item in hamCounter:
            #filehandle.write('%s  ' % item)
            #filehandle.write('%s\n' % hamCounter[item])
    #with open('SPAMcounter.txt','w') as filehandle:
        #for item in hamCounter:
            #filehandle.write('%s  ' % item)
            #filehandle.write('%s\n' % spamCounter[item])
    

    for eachHam in hamCounter:#calculate probability
        hamPosteriorDict[eachHam]=(hamCounter[eachHam]+smoothing_parameter)/(sumHam+len(hamCounter)*smoothing_parameter)
    for eachSpam in spamCounter:
        spamPosteriorDict[eachSpam]=(spamCounter[eachSpam]+smoothing_parameter)/(sumSpam+len(spamCounter)*smoothing_parameter)
    hamPosteriorDict["unknown"]=(0+smoothing_parameter)/(sumHam+len(hamCounter)*smoothing_parameter)
    spamPosteriorDict["unknown"]=(0+smoothing_parameter)/(sumSpam+len(spamCounter)*smoothing_parameter)
    #with open('hamDict.txt','w') as filehandle:
        #for item in hamPosteriorDict:
            #filehandle.write('%s  ' % item)
            #filehandle.write('%s\n' % hamPosteriorDict[item])
    #with open('SPAMDict.txt','w') as filehandle:
        #for item in spamPosteriorDict:
            #filehandle.write('%s  ' % item)
            #filehandle.write('%s\n' % spamPosteriorDict[item])

    for eachSetIndex in range(len(dev_set)):
        pHam=math.log(pos_prior)
        pSpam=math.log(1-pos_prior)
        for eachElementInSet in dev_set[eachSetIndex]:
            if eachElementInSet in hamPosteriorDict:
                pHam=pHam+math.log(hamPosteriorDict[eachElementInSet])#so log of each word and add all, then add post prior
            else:
                pHam=pHam+math.log(hamPosteriorDict["unknown"])
            if eachElementInSet in spamPosteriorDict:
                pSpam=pSpam+math.log(spamPosteriorDict[eachElementInSet])
            else:
                pSpam=pSpam+math.log(spamPosteriorDict["unknown"])
        if pSpam<pHam:
            resultLableList.append(1)
        else:
            resultLableList.append(0)
    #with open('resultLIST.txt','w') as filehandle:
        #for item in resultLableList:
            #filehandle.write(str(item))
    return resultLableList
    