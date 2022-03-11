# mp4.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created Fall 2018: Margaret Fleck, Renxuan Wang, Tiantian Fang, Edward Huang (adapted from a U. Penn assignment)
# Modified Spring 2020: Jialu Li, Guannan Guo, and Kiran Ramnath
# Modified Fall 2020: Amnon Attali, Jatin Arora
# Modified Spring 2021 by Kiran Ramnath
"""
Part 1: Simple baseline that only uses word statistics to predict tags
"""
START_TAG = "START"
END_TAG = "END"
import collections

def baseline(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    #print(train[0],len(train))
    tagDict={'START':{'START':1}}
    countTag={}
    resultSentenceList=[]
    i=0
    for sentence in train:
        for eachTuple in sentence:
            #print(eachTuple)
            if eachTuple[1] in countTag:
                countTag[eachTuple[1]]+=1
            else:
                countTag[eachTuple[1]]=1;
            if eachTuple[0] in tagDict:
                if eachTuple[1] in tagDict[eachTuple[0]]:
                    tagDict[eachTuple[0]][eachTuple[1]]+=1
                else:
                    tagDict[eachTuple[0]][eachTuple[1]]=1
            else:
                tagDict[eachTuple[0]]={}
                tagDict[eachTuple[0]][eachTuple[1]]=1
    tagDict = {key : dict(sorted(val.items(), key = lambda ele: ele[1])) for key, val in tagDict.items()}
    countTag=dict(sorted(countTag.items(), key=lambda item: item[1]))
    #print(countTag)

    for eachSetIndex in range(len(test)):
        senList=[]
        for eachElementInSet in test[eachSetIndex]:
            if eachElementInSet in tagDict:
                senList.append((eachElementInSet,list(tagDict[eachElementInSet].keys())[-1]))
            else:
                senList.append((eachElementInSet,list(countTag.keys())[-1]))
        resultSentenceList.append(senList)
    
    
    
#     with open('resultSentenceList.txt','w') as filehandle:
#         for item in resultSentenceList:
#             filehandle.write('%s\n' % str(item))
#     print("arrived")

                
    return resultSentenceList


