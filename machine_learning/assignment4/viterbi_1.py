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
    #print(transition)
    #print(test[0])
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
        for eachTag in curStep:#                    BTW S and first timestamp
            currNode=Node(eachTag,1)
            prevNode=Node(prevTag,0)
            if sentence[1] in emission[eachTag]:
                tempDictofProba[currNode]=curStep[eachTag]+emission[eachTag][sentence[1]]
            else:
                tempDictofProba[currNode]=curStep[eachTag]+emission[eachTag]["unknown"]
            backpointer[currNode]=prevNode
        # for eachNode in tempDictofProba:
        #     print(eachNode,tempDictofProba[eachNode])
        # print("arrived")#,(sentence[1],eachTag),(sentence[1],prevTag))
        
        prevWord=sentence[1]
        
        for wordIdx in range(2,len(sentence)-1):
            prevWord=sentence[wordIdx-1]
            for i in statelist:
                tempListofProba=[]
                tempListofState=[]
                currNode=Node(i,wordIdx)
                for eachState in statelist:#?????
                #for eachState in transition[i]:#eachstate is the possible state that can transit into
                    prevNode=Node(eachState,wordIdx-1)
                    if i in transition[eachState]:
                        tempListofProba.append(tempDictofProba[prevNode]+transition[eachState][i])
                        #print("yeah",i,prevNode,currNode,tempDictofProba[prevNode],transition[eachState][i],tempDictofProba[prevNode]+transition[eachState][i])
                    else:
                        tempListofProba.append(tempDictofProba[prevNode]+transition[eachState]['unknown'])
                        #print('half',(eachState,'unknown'))
                    tempListofState.append(eachState)
                
                maxnum=max(tempListofProba)
                maxTag=tempListofState[tempListofProba.index(maxnum)]
                prevTag=maxTag
                prevNode=Node(prevTag,wordIdx-1)
                
                if sentence[wordIdx] in emission[i]:
                    tempDictofProba[currNode]=maxnum+emission[i][sentence[wordIdx]]#Update the cell probability
                else:
                    tempDictofProba[currNode]=maxnum+emission[i]['unknown']
                backpointer[currNode]=prevNode
                #print(backpointer[currNode],'this is back ponter for ',currNode)
                #print()
                    
        compareList=[]
        compareTag=[]
        
        for j in statelist:
            lastNode=Node(j,len(sentence)-2)
            compareList.append(tempDictofProba[lastNode]) 
            compareTag.append(j) 
                    #print(backpointer,"this is backpointer") 
        maxnum=max(compareList)
        maxTag=compareTag[compareList.index(maxnum)] 
        curWord=sentence[1:-1][-1]

        prediction.append((curWord,maxTag))
        temp=Node(maxTag,len(sentence)-2)
        #print(temp,"result")
        while temp.wayWords!=1:#temp.wayWords[-1]!=sentence[1] and
            temp=backpointer[temp]
            prediction.append((sentence[temp.wayWords],temp.curTag))
        prediction.append(('START','START'))
        prediction.reverse()
        tempDictofProba.clear()
        result.append(prediction)
        backpointer.clear()
        #print(prediction,"this is prediction")
    return result


"""
Part 2: This is the simplest version of viterbi that doesn't do anything special for unseen words
but it should do better than the baseline at words with multiple tags (because now you're using context
to predict the tag). count(X,Y) is the frequncy word tag pair happens, X is word, Y is tag, number of unique word, 500 unique word noun then unique types in X is 500. count(Y) is how many  tag in training set
transition: given previous tag, how many next tag can go---unique tyes in X

"""

def viterbi_1(train, test):
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
    countTag=['unknown']
    totalSingle=0
    totalDouble=0
    smoothing_parameter=math.exp(-4)
    
    for sentence in train:
        for eachTupleIdx in range(1,len(sentence)-1):
            if sentence[eachTupleIdx][1] not in countTag:#a list contain all TAGS
                countTag.append(sentence[eachTupleIdx][1])
            
            if sentence[eachTupleIdx][1] not in each_tag_have_frequency:#COUNT tag frequency
                each_tag_have_frequency[sentence[eachTupleIdx][1]]=1
            else:
                each_tag_have_frequency[sentence[eachTupleIdx][1]]+=1

            if sentence[eachTupleIdx][0] not in each_word_have_frequency:#COUNT word frequency
                each_word_have_frequency[sentence[eachTupleIdx][0]]=1
            else:
                each_word_have_frequency[sentence[eachTupleIdx][0]]+=1

            
            if sentence[eachTupleIdx] in tagSingleDict:#count word tag pair
                tagSingleDict[sentence[eachTupleIdx]]+=1
                totalSingle+=1
            else:
                tagSingleDict[sentence[eachTupleIdx]]=1
                totalSingle+=1
            if eachTupleIdx <len(sentence)-2:#DOUBLE TAGS---tag tag pair
                if eachTupleIdx+1 < len(sentence) and (sentence[eachTupleIdx][1],sentence[eachTupleIdx+1][1]) in tagDoubleDict:#Double TAG
                    tagDoubleDict[(sentence[eachTupleIdx][1],sentence[eachTupleIdx+1][1])]+=1;
                    totalDouble+=1
                else:
                    if eachTupleIdx+1 < len(sentence):
                        tagDoubleDict[(sentence[eachTupleIdx][1],sentence[eachTupleIdx+1][1])]=1;
                        totalDouble+=1
    
    # print(countTag)
    num_of_unique_word=0
    #count number of unique words overall
    for eachWord in each_word_have_frequency:
        num_of_unique_word+=1


    for eachComb in tagSingleDict:# EMISSSION
        if eachComb[1] in tagSingleProbDict:
            tagSingleProbDict[eachComb[1]][eachComb[0]]=math.log(tagSingleDict[eachComb]+smoothing_parameter)-math.log(each_tag_have_frequency[eachComb[1]]+(each_word_have_frequency[eachComb[0]]+1)*smoothing_parameter)
        else:
            tagSingleProbDict[eachComb[1]]={}
            tagSingleProbDict[eachComb[1]][eachComb[0]]=math.log(tagSingleDict[eachComb]+smoothing_parameter)-math.log(each_tag_have_frequency[eachComb[1]]+(each_word_have_frequency[eachComb[0]]+1)*smoothing_parameter)
    tagSingleProbDict["unknown"]={}
    each_word_have_frequency['unknown']=num_of_unique_word
    
    for eachTag in countTag:
        tagSingleProbDict[eachTag]["unknown"]=math.log(0+smoothing_parameter)-math.log(each_tag_have_frequency[eachComb[1]]+(each_word_have_frequency['unknown']+1)*smoothing_parameter)
    #denomitator should be same as above

    for eachComb in tagDoubleDict:#how many tags is inside currentTag----unique types in X
        if eachComb[0] in each_tag_have_tags:
            each_tag_have_tags[eachComb[0]]+=1
        else:
            each_tag_have_tags[eachComb[0]]=1
    each_tag_have_frequency['unknown']=len(countTag)
    each_tag_have_tags['unknown']=len(countTag)
    #TRANSITION
    for eachComb in tagDoubleDict:#calculate probability
        if eachComb[0] in tagDoubleProbDict:
            tagDoubleProbDict[eachComb[0]][eachComb[1]]=math.log(tagDoubleDict[eachComb]+smoothing_parameter)-math.log(each_tag_have_frequency[eachComb[0]]+(each_tag_have_tags[eachComb[0]]+1)*smoothing_parameter)
        else:
            tagDoubleProbDict[eachComb[0]]={}
            tagDoubleProbDict[eachComb[0]][eachComb[1]]=math.log(tagDoubleDict[eachComb]+smoothing_parameter)-math.log(each_tag_have_frequency[eachComb[0]]+(each_tag_have_tags[eachComb[0]]+1)*smoothing_parameter)
    
    tagDoubleProbDict["unknown"]={}
    tagDoubleProbDict['START']={}
    for eachTag in countTag:
        tagDoubleProbDict['START'][eachTag]=1
        tagDoubleProbDict["unknown"][eachTag]=math.log(0+smoothing_parameter)-math.log(each_tag_have_frequency[eachTag]+(each_tag_have_tags['unknown']+1)*smoothing_parameter)
        tagDoubleProbDict[eachTag]["unknown"]=math.log(0+smoothing_parameter)-math.log(each_tag_have_frequency['unknown']+(each_tag_have_tags[eachTag]+1)*smoothing_parameter)

    

    # with open('each_tag_have_tags.txt','w') as filehandle:
    #     for item in each_tag_have_tags:
    #         filehandle.write('%s' % str(item))
    #         filehandle.write('%s\n' % str(each_tag_have_tags[item]))
    # with open('each_tag_have_frequency.txt','w') as filehandle:
    #     for item in each_tag_have_frequency:
    #         filehandle.write('%s' % str(item))
    #         filehandle.write('%s\n' % str(each_tag_have_frequency[item]))
    # with open('each_word_have_frequency.txt','w') as filehandle:
    #     for item in each_word_have_frequency:
    #         filehandle.write('%s' % str(item))
    #         filehandle.write('%s\n' % str(each_word_have_frequency[item]))

    # with open('tagSingle.txt','w') as filehandle:
    #     for item in tagSingleDict:
    #         filehandle.write('%s' % str(item))
    #         filehandle.write('%s\n' % str(tagSingleDict[item]))
    # with open('tagSingleProbDict-P2.txt','w') as filehandle:
    #     for item in tagSingleProbDict:
    #         for tags in tagSingleProbDict[item]:
    #             filehandle.write('%s' % str(item))
    #             filehandle.write(' %s' % str(tags))
    #             #print(tags,"open")
    #             filehandle.write(' %s\n' % str(tagSingleProbDict[item][tags]))
            
    # # with open('tagDouble.txt','w') as filehandle:
    # #     for item in tagDoubleDict:
    # #         filehandle.write('%s' % str(item))
    # #         filehandle.write('%s\n' % str(tagDoubleDict[item]))
    # with open('tagDoubleProbDict-P2.txt','w') as filehandle:
    #     for item in tagDoubleProbDict:
    #         for tags in tagDoubleProbDict[item]:
    #             #print(item,tags,tagDoubleProbDict[item])
    #             filehandle.write('%s' % str(item))
    #             filehandle.write(' %s' % str(tags))
    #             filehandle.write(' %s\n' % str(tagDoubleProbDict[item][tags]))
    #ans = viterbi(tagSingleProbDict, tagDoubleProbDict,[test[1]])
    ans = viterbi(tagSingleProbDict, tagDoubleProbDict,test)
    return ans
    
    