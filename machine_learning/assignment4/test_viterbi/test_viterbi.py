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
# Modified Spring 2021 by Kiran Ramnath (kiranr2@illinois.edu)

"""
This file should not be submitted - it is only meant to test your implementation of the Viterbi algorithm. 
"""
from utils import read_files, get_nested_dictionaries
import math
smoothing_constant = 1e-10

def main():
    test, emission, transition, output = read_files()
    emission, transition = get_nested_dictionaries(emission, transition)
    #transition = {key : dict(sorted(val.items(), key = lambda ele: ele[1])) for key, val in transition.items()}
    
    initial = transition["S"]
    prediction = []
    
    print(test,'test')
    print(initial,"INITIAL")
    print(transition,"second")
    print(emission,"emission")
    tempViterb=0
    curStep=initial
    viterbi={}
    backpointer={}#(biggest probability, the correspondng state from last time stamp)
    
    prevTag='S'
    curStepDict={}
    statelist=emission.keys()

    for sentence in test:
        tempDictofProba={}#this dict stores the probabilty of each state, will update everytime 
        tempListofState=[]
        for eachTag in curStep:#this is only for transition btw S and first timestamp
            print(sentence[0],"sentence0")
            tempDictofProba[(eachTag,sentence[0])]=curStep[eachTag]*emission[eachTag][sentence[0]]
            #print(curStep[eachTag]*emission[eachTag][test[0]],eachTag,sentence[0])
            backpointer[(sentence[0],eachTag)]=(sentence[0],prevTag)
        #transition[maxTag]
        #print(tempDictofProba,"initial")
        prevWord=sentence[0]
        for wordIdx in range(1,len(sentence)):
            for i in statelist:
                tempListofProba=[]
                tempListofState=[]
                for eachState in transition[i]:
                    tempListofProba.append(tempDictofProba[(eachState,prevWord)]*transition[eachState][i])
                    tempListofState.append(eachState)
                    if i=="MD" and wordIdx==1 and eachState=="NNP":
                        print(tempListofProba,eachState,sentence[wordIdx],transition[eachState][i])
                maxnum=max(tempListofProba)
                maxTag=tempListofState[tempListofProba.index(maxnum)]
                prevTag=maxTag
                prevWord=sentence[wordIdx-1]
                #print(" ")
                #print(maxnum*emission[i][sentence[wordIdx]])
                tempDictofProba[(i,sentence[wordIdx])]=maxnum*emission[i][sentence[wordIdx]]#Update the cell probability
                backpointer[(sentence[wordIdx],i)]=(sentence[wordIdx-1],prevTag)
                # if wordIdx <3:
                #     print("Dict")
                #print(tempDictofProba)
                #     print("backpointer")
                #print(backpointer)
                    
        compareList=[]
        compareTag=[]
        for j in statelist:
            compareList.append(tempDictofProba[(j,sentence[-1])]) 
            compareTag.append(j)  
        #print(compareTag)
        maxnum=max(compareList)
        maxTag=compareTag[compareList.index(maxnum)] 
        curWord=sentence[-1]
        prediction.append((curWord,maxTag))
        temp=(curWord,maxTag)
        while temp[0]!=sentence[0]:
            temp=backpointer[temp]
            #print(temp)
            prediction.append(temp)
        prediction.reverse()



            # for i in statelist:
            #     tempListofProba=[]
            #     tempListofState=[]
            #     for eachTag in transition[i]:
            #         tempListofProba.append(transition[eachTag][i]*tempDictofProba[eachTag])#第一个乘数要改
            #         tempListofState.append(eachTag)
            #         print(i)
            #         if i=="MD" and wordIdx==1 and eachTag=="NNP":
            #             print(tempListofProba,eachTag,sentence[wordIdx],transition[eachTag][i],tempDictofProba[eachTag])
            #     maxnum=max(tempListofProba)
            #     maxTag=tempListofState[tempListofProba.index(maxnum)]
            #     prevTag=i
            #     print("no")
            #     tempDictofProba[maxTag]=maxnum*emission[maxTag][sentence[wordIdx]]#Update the cell probability
            #     backpointer[(maxTag,sentence[wordIdx])]=(prevTag,sentence[wordIdx-1])
        tempDictofProba.clear()
    
    #print(backpointer['NNP'],len(backpointer))
    """WRITE YOUR VITERBI IMPLEMENTATION HERE"""
    #for predictionTag in backpointer:
        #prediction.append()
    print('Your Output is:',prediction,'\n Expected Output is:',output)


if __name__=="__main__":
    main()