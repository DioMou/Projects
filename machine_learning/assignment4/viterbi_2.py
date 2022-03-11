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

import math
class Node:
    def __init__(self,curTag,wayWords):
        self.curTag=curTag
        self.wayWords=wayWords
    def __hash__(self):
        return hash(str(self.wayWords)+str(self.curTag))
    def __eq__(self,other):
        return self.curTag == other.curTag and self.wayWords == other.wayWords 
    def __str__(self):
        return str(self.curTag)+' '+str(self.wayWords)+' '


def viterbi(emission, transition,test):
    initial = transition["START"]
    
    result=[]
    
    #print(initial,"INITIAL")
    tempViterb=0
    curStep=initial
    viterbi={}
    backpointer={}#(biggest probability, the correspondng state from last time stamp)
    
    prevTag='START'
    statelist=emission.keys()
    #print(statelist)
    

    for sentence in test:
        tempDictofProba={}#this dict stores the probabilty of each state, will update everytime 
        tempListofState=[]
        prediction = [('END','END')]
        for eachTag in curStep:#this is only for transition btw S and first timestamp
            # currNode=Node(eachTag,1)
            # prevNode=Node(prevTag,0)
            currNode=(eachTag,1)
            prevNode=(prevTag,0)
            if sentence[1] in emission[eachTag]:
                tempDictofProba[currNode]=curStep[eachTag]+emission[eachTag][sentence[1]]
            else:
                tempDictofProba[currNode]=curStep[eachTag]+emission[eachTag]["unknown"]
            backpointer[currNode]=prevNode
        # for eachNode in tempDictofProba:
        #     print(eachNode)
        # print("arrived")#,(sentence[1],eachTag),(sentence[1],prevTag))
        
        prevWord=sentence[1]
        
        for wordIdx in range(2,len(sentence)-1):
            prevWord=sentence[wordIdx-1]
            for i in statelist:
                tempListofProba=[]
                tempListofState=[]
                #currNode=Node(i,wordIdx)
                currNode=(i,wordIdx)
                for eachState in statelist:
                    #prevNode=Node(eachState,wordIdx-1)
                    prevNode=(eachState,wordIdx-1)
                    #if i in transition[eachState]:
                    tempListofProba.append(tempDictofProba[prevNode]+transition[eachState][i])
                        #print("yeah",i,prevNode,transition[eachState][i],tempDictofProba[prevNode]*transition[eachState][i])
                    #else:
                        #tempListofProba.append(tempDictofProba[prevNode]+transition[eachState]['unknown'])
                        #print('half',(eachState,'unknown'))
                    tempListofState.append(eachState)
                
                maxnum=max(tempListofProba)
                maxTag=tempListofState[tempListofProba.index(maxnum)]
                prevTag=maxTag
                #prevNode=Node(prevTag,wordIdx-1)
                prevNode=(prevTag,wordIdx-1)
                if sentence[wordIdx] in emission[i]:
                    tempDictofProba[currNode]=maxnum+emission[i][sentence[wordIdx]]#Update the cell probability
                else:
                    tempDictofProba[currNode]=maxnum+emission[i]['unknown']
                backpointer[currNode]=prevNode
                #print(backpointer[currNode],'this is back ponter for ',currNode)
                #print()
                    
        compareList=[]
        compareTag=[]
        
        #find MAX among states for last word in sentence
        for j in statelist:
            #lastNode=Node(j,len(sentence)-2)
            lastNode=(j,len(sentence)-2)
            compareList.append(tempDictofProba[lastNode]) 
            compareTag.append(j) 
                    #print(backpointer,"this is backpointer") 
        maxnum=max(compareList)
        maxTag=compareTag[compareList.index(maxnum)] 
        curWord=sentence[1:-1][-1]

        #start Backtracing
        prediction.append((curWord,maxTag))
        #temp=Node(maxTag,len(sentence)-2)
        temp=(maxTag,len(sentence)-2)
        #print(temp,"result")
        #while temp.wayWords!=1:#temp.wayWords[-1]!=sentence[1] and
        while temp[1]!=1:
            temp=backpointer[temp]
            #prediction.append((sentence[temp.wayWords],temp.curTag))
            prediction.append((sentence[temp[1]],temp[0]))
        prediction.append(('START','START'))
        prediction.reverse()
        tempDictofProba.clear()
        backpointer.clear()
        result.append(prediction)
        #print(prediction,"this is prediction")
    return result



"""
Part 3: Here you should improve viterbi to use better laplace smoothing for unseen words
This should do better than baseline and your first implementation of viterbi, especially on unseen words
"""

def viterbi_2(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    tagSingleDict={}
    tagDoubleDict={}
    tagSingleProbDict={}#emission P
    tagDoubleProbDict={}#transition P
    each_tag_have_tags={}
    each_tag_have_frequency={}
    each_word_have_frequency={}
    #countTag=["unknown"]
    countTag=[]
    singleOccur={}
    single_Probability={}
    totalSingle=1
    totalDouble=1
    smoothing_parameter=math.exp(-5)
    hepexWeight=0.5
    
    for sentence in train:
        for eachTupleIdx in range(1,len(sentence)-1):
            if sentence[eachTupleIdx][1] not in countTag:#a list contain all TAGS
                countTag.append(sentence[eachTupleIdx][1])

            if sentence[eachTupleIdx][1] not in each_tag_have_frequency:#COUNT tag frequency
                each_tag_have_frequency[sentence[eachTupleIdx][1]]=1
            else:
                each_tag_have_frequency[sentence[eachTupleIdx][1]]+=hepexWeight

            if sentence[eachTupleIdx][0] not in each_word_have_frequency:#COUNT word frequency
                each_word_have_frequency[sentence[eachTupleIdx][0]]=1
            else:
                each_word_have_frequency[sentence[eachTupleIdx][0]]+=hepexWeight

            
            if sentence[eachTupleIdx] in tagSingleDict:#count single tag occurance, word tag pair
                tagSingleDict[sentence[eachTupleIdx]]+=hepexWeight
                totalSingle+=1
            else:
                tagSingleDict[sentence[eachTupleIdx]]=1
            if eachTupleIdx <len(sentence)-2:
                if eachTupleIdx+1 < len(sentence) and (sentence[eachTupleIdx][1],sentence[eachTupleIdx+1][1]) in tagDoubleDict:#Double TAG
                    tagDoubleDict[(sentence[eachTupleIdx][1],sentence[eachTupleIdx+1][1])]+=hepexWeight;
                    totalDouble+=1
                else:
                    if eachTupleIdx+1 < len(sentence):
                        tagDoubleDict[(sentence[eachTupleIdx][1],sentence[eachTupleIdx+1][1])]=1;
    num_of_unique_word=0
    #count number of unique words overall
    for eachWord in each_word_have_frequency:
        num_of_unique_word+=1
    
    sumOccur=0
    for eachComb in each_word_have_frequency:# COUNT. words that appear once, and store(word, tag) to SINGLE_OCCUR dict
        if each_word_have_frequency[eachComb]==1:
            for eachTag in countTag:
                if (eachComb,eachTag) in tagSingleDict:#make sure it exist in word tag pair list
                    if eachTag in singleOccur:
                        singleOccur[eachTag]+=hepexWeight
                        sumOccur+=hepexWeight
                    else:
                        singleOccur[eachTag]=1
                        sumOccur+=1
    for eachTag in countTag:
        if eachTag in singleOccur:
            single_Probability[eachTag]=singleOccur[eachTag]/sumOccur
        else:
            single_Probability[eachTag]=0.0001


    for eachComb in tagSingleDict:#calculate probability of EMISSSION
        hapax_parameter=single_Probability[eachComb[1]]*smoothing_parameter
        if eachComb[1] in tagSingleProbDict:
            tagSingleProbDict[eachComb[1]][eachComb[0]]=math.log(tagSingleDict[eachComb]+hapax_parameter)-math.log(each_tag_have_frequency[eachComb[1]]+(each_word_have_frequency[eachComb[0]]+1)*hapax_parameter)
        else:
            tagSingleProbDict[eachComb[1]]={}
            tagSingleProbDict[eachComb[1]][eachComb[0]]=math.log(tagSingleDict[eachComb]+hapax_parameter)-math.log(each_tag_have_frequency[eachComb[1]]+(each_word_have_frequency[eachComb[0]]+1)*hapax_parameter)
    #tagSingleProbDict["unknown"]={}
    each_word_have_frequency['unknown']=num_of_unique_word
    print(each_tag_have_frequency[eachComb[1]])
    for eachTag in countTag:
        hapax_parameter=single_Probability[eachTag]*smoothing_parameter
        tagSingleProbDict[eachTag]["unknown"]=math.log(0+hapax_parameter)-math.log(15000+(each_word_have_frequency['unknown']+1)*hapax_parameter)

    for eachComb in tagDoubleDict:#how many tags is inside currentTag----unique types in X
        if eachComb[0] in each_tag_have_tags:
            each_tag_have_tags[eachComb[0]]+=hepexWeight
        else:
            each_tag_have_tags[eachComb[0]]=1
    #each_tag_have_frequency['unknown']=1#len(countTag)
    #each_tag_have_tags['unknown']=1#len(countTag)
    

    for eachTagStart in countTag:#give every transition a base value
        for eachTagEnd in countTag:
            if eachTagStart in tagDoubleProbDict:
                tagDoubleProbDict[eachTagStart][eachTagEnd]=math.log(0+smoothing_parameter)-math.log(each_tag_have_frequency[eachTagStart]+(each_tag_have_tags[eachTagStart]+1)*smoothing_parameter)
            else:
                tagDoubleProbDict[eachTagStart]={}
                tagDoubleProbDict[eachTagStart][eachTagEnd]=math.log(0+smoothing_parameter)-math.log(each_tag_have_frequency[eachTagStart]+(each_tag_have_tags[eachTagStart]+1)*smoothing_parameter)
    
    # with open('tagDoubleRaw-P3.txt','w') as filehandle:
    #     for item in tagDoubleProbDict:
    #         for tags in tagDoubleProbDict[item]:
    #             #print(item,tags,tagDoubleProbDict[item])
    #             filehandle.write('%s' % str(item))
    #             filehandle.write(' %s' % str(tags))
    #             filehandle.write(' %s\n' % str(tagDoubleProbDict[item][tags]))
    
    #TRANSITION
    for eachComb in tagDoubleDict:#calculate probability for known possibility
        #hapax_parameter=single_Probability[eachComb[0]]*smoothing_parameter
        hapax_parameter=smoothing_parameter
        if eachComb[0] in tagDoubleProbDict:
            tagDoubleProbDict[eachComb[0]][eachComb[1]]=math.log(tagDoubleDict[eachComb]+hapax_parameter)-math.log(each_tag_have_frequency[eachComb[0]]+(each_tag_have_tags[eachComb[0]]+1)*hapax_parameter)
        else:
            tagDoubleProbDict[eachComb[0]]={}
            tagDoubleProbDict[eachComb[0]][eachComb[1]]=math.log(tagDoubleDict[eachComb]+hapax_parameter)-math.log(each_tag_have_frequency[eachComb[0]]+(each_tag_have_tags[eachComb[0]]+1)*hapax_parameter)
    
    #tagDoubleProbDict["unknown"]={}
    tagDoubleProbDict['START']={}
    for eachTag in countTag:
        hapax_parameter=single_Probability[eachTag]*smoothing_parameter
        hapax_parameter=smoothing_parameter
        tagDoubleProbDict['START'][eachTag]=1#math.log(1+hapax_parameter)-math.log(1+(len(countTag))*hapax_parameter)
        #tagDoubleProbDict["unknown"][eachTag]=math.log(0+hapax_parameter)-math.log(each_tag_have_frequency[eachTag]+(each_tag_have_tags['unknown']+1)*hapax_parameter)
        #tagDoubleProbDict[eachTag]["unknown"]=math.log(0+hapax_parameter)-math.log(each_tag_have_frequency['unknown']+(each_tag_have_tags[eachTag]+1)*hapax_parameter)


#     with open('tagSingle.txt','w') as filehandle:
#         for item in tagSingleDict:
#             filehandle.write('%s' % str(item))
#             filehandle.write('%s\n' % str(tagSingleDict[item]))
    # with open('singleOccurWord.txt','w') as filehandle:
    #     for item in singleOccur:
    #         filehandle.write('%s' % str(item))
    #         filehandle.write('%s\n' % str(singleOccur[item]))
    # with open('single_Probability.txt','w') as filehandle:
    #     for item in single_Probability:
    #         filehandle.write('%s' % str(item))
    #         filehandle.write('%s\n' % str(single_Probability[item]))
#     with open('tagSingleProbDict-P3.txt','w') as filehandle:
#         for item in tagSingleProbDict:
#             for tags in tagSingleProbDict[item]:
#                 filehandle.write('%s' % str(item))
#                 filehandle.write(' %s' % str(tags))
#                 #print(tags,"open")
#                 filehandle.write(' %s\n' % str(tagSingleProbDict[item][tags]))
            
#     with open('tagDouble.txt','w') as filehandle:
#         for item in tagDoubleDict:
#             filehandle.write('%s' % str(item))
#             filehandle.write('%s\n' % str(tagDoubleDict[item]))
    # with open('tagDoubleProbDict-P3.txt','w') as filehandle:
    #     for item in tagDoubleProbDict:
    #         for tags in tagDoubleProbDict[item]:
    #             #print(item,tags,tagDoubleProbDict[item])
    #             filehandle.write('%s' % str(item))
    #             filehandle.write(' %s' % str(tags))
    #             filehandle.write(' %s\n' % str(tagDoubleProbDict[item][tags]))
    #print(test[0])
    #ans = viterbi(tagSingleProbDict, tagDoubleProbDict,[test[1]])
    ans = viterbi(tagSingleProbDict, tagDoubleProbDict,test)
    return ans