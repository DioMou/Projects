# naive_bayes_mixture.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018
# Modified by Jaewook Yeom 02/02/2020

"""
This is the main entry point for Part 2 of this MP. You should only modify code
within this file for Part 2 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import nltk
nltk.download('punkt')
from nltk.util import ngrams
import collections
import math

def extract_ngrams(data, num):
    n_grams = ngrams(nltk.word_tokenize(data), num)
    return [ ' '.join(grams) for grams in n_grams]


def naiveBayesMixture(train_set, train_labels, dev_set, bigram_lambda,unigram_smoothing_parameter, bigram_smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each email
    example: suppose I had two emails 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two emails, first one was ham and second one was spam.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each email that we are testing on
              It follows the same format as train_set

    bigram_lambda - float between 0 and 1

    unigram_smoothing_parameter - Laplace smoothing parameter for unigram model (between 0 and 1)

    bigram_smoothing_parameter - Laplace smoothing parameter for bigram model (between 0 and 1)

    pos_prior - positive prior probability (between 0 and 1)
    """
    hamCounterUni=collections.Counter()
    spamCounterUni=collections.Counter()
    hamCountBI=collections.Counter()
    spamCountBI=collections.Counter()
    hamPosteriorDict={}
    spamPosteriorDict={}
    sumHam=0.0
    sumSpam=0.0
    resultLableList=[]
    for eachSetIndex in range(len(train_labels)):
        if train_labels[eachSetIndex] == 1:#ham label counter
            hamCounterUni.update(train_set[eachSetIndex])
            sumHam=sumHam+len(train_set[eachSetIndex])
        elif train_labels[eachSetIndex] == 0:#spam label counter 
            spamCounterUni.update(train_set[eachSetIndex])
            sumSpam=sumSpam+len(train_set[eachSetIndex])

    for eachHam in hamCounterUni:#calculate probability
        hamPosteriorDict[eachHam]=(hamCounterUni[eachHam]+unigram_smoothing_parameter)/(sumHam+len(hamCounterUni)*unigram_smoothing_parameter)
    for eachSpam in spamCounterUni:
        spamPosteriorDict[eachSpam]=(spamCounterUni[eachSpam]+unigram_smoothing_parameter)/(sumSpam+len(spamCounterUni)*unigram_smoothing_parameter)
    hamPosteriorDict["unknown"]=(0+unigram_smoothing_parameter)/(sumHam+len(hamCounterUni)*unigram_smoothing_parameter)
    spamPosteriorDict["unknown"]=(0+unigram_smoothing_parameter)/(sumSpam+len(spamCounterUni)*unigram_smoothing_parameter)
    # TODO: Write your code here
    # return predicted labels of development set

    #creating bigram
    sumHamBI=0
    sumSpamBI=0
    for eachSetIndex in range(len(train_labels)): #bigram for training set
        train_set[eachSetIndex]=' '.join(train_set[eachSetIndex])
        bigramDataSet=extract_ngrams(train_set[eachSetIndex], 2)
        if train_labels[eachSetIndex] == 1:#ham label counter
            hamCountBI.update(bigramDataSet)
            sumHamBI=sumHamBI+len(bigramDataSet)
        elif train_labels[eachSetIndex] ==0:
            spamCountBI.update(bigramDataSet)
            sumSpamBI=sumSpamBI+len(bigramDataSet)
    
    hamPosDictBI={}
    spamPosTDictBI={}
    
    
    #calculate probability dictionary
    for eachHam in hamCountBI:
        hamPosDictBI[eachHam]=(hamCountBI[eachHam]+bigram_smoothing_parameter)/(sumHamBI+len(hamCountBI)*bigram_smoothing_parameter)
    for eachSpam in spamCountBI:
        spamPosTDictBI[eachSpam]=(spamCountBI[eachSpam]+bigram_smoothing_parameter)/(sumSpamBI+len(spamCountBI)*bigram_smoothing_parameter)
    hamPosDictBI["unknown"]=(0+bigram_smoothing_parameter)/(sumHamBI+len(hamCountBI)*bigram_smoothing_parameter)
    spamPosTDictBI["unknown"]=(0+bigram_smoothing_parameter)/(sumSpamBI+len(spamCountBI)*bigram_smoothing_parameter)


    for eachBigIndex in range(len(dev_set)):
        pHam=math.log(pos_prior)
        pSpam=math.log(1-pos_prior)

        hTemp=0
        sTemp=0
        for eachElementInSet in dev_set[eachBigIndex]:
            if eachElementInSet in hamPosteriorDict:
                hTemp=hTemp+math.log(hamPosteriorDict[eachElementInSet])#so log of each word and add all, then add post prior
            else:
                hTemp=hTemp+math.log(hamPosteriorDict["unknown"])
            if eachElementInSet in spamPosteriorDict:
                sTemp=sTemp+math.log(spamPosteriorDict[eachElementInSet])
            else:
                sTemp=sTemp+math.log(spamPosteriorDict["unknown"])
        hTemp=hTemp*(1-bigram_lambda)
        sTemp=sTemp*(1-bigram_lambda)

        hTemp2=0
        sTemp2=0
        dev_set[eachBigIndex]=' '.join(dev_set[eachBigIndex])
        bigDevSet=extract_ngrams(dev_set[eachBigIndex],2)
        for eachElementInSet in bigDevSet:
            if eachElementInSet in hamPosDictBI:
                hTemp2=hTemp2+math.log(hamPosDictBI[eachElementInSet])
            else:
                hTemp2=hTemp2+math.log(hamPosDictBI["unknown"])
            if eachElementInSet in spamPosTDictBI:
                sTemp2=sTemp2+math.log(spamPosTDictBI[eachElementInSet])
            else:
                sTemp2=sTemp2+math.log(spamPosTDictBI["unknown"])
        hTemp2=hTemp2*bigram_lambda
        sTemp2=sTemp2*bigram_lambda
        
        pHam=pHam+hTemp+hTemp2
        pSpam=pSpam+sTemp+sTemp2
        if pSpam<pHam:
            resultLableList.append(1)
        else:
            resultLableList.append(0)
    return resultLableList