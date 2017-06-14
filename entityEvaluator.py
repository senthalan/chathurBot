import re, math
from collections import Counter
from calculation import *

WORD = re.compile(r'\w+')

entitylist=['model','brand','onlinestore','number','amount_of_money']
overallTotalPrecision=0
overallTotalRecall=0

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)


def eveluateEntityPerQuestion(actualList,estimatedList):
    global overallTotalPrecision,overallTotalRecall
    fullMatch = 0
    partialMatch = 0
    missedEntityCount = 0
    detectedWrongEntityCount = 0
    #print 'actual entity list :', actualList
    #print 'estimated entity list: ' , estimatedList
    # global fullMatch,partialFlag,partialMatch,WHFlag,CMFlag,misssmatch,whmatch
    for entity in entitylist:

        if entity not in actualList:
            actualList[entity]=[]
        if entity  not in estimatedList:
            estimatedList[entity]=[]

    for entity in entitylist:

        matchEntity=set(actualList[entity]).intersection(estimatedList[entity])
        # print matchEntity

        fullMatch+=len(matchEntity)

        for value in actualList[entity]:

            CMFlag = 0
            for key in entitylist:
                if ((value not in set(estimatedList[key]))):
                    CMFlag+=1
                    # print value,CMFlag

                temp=estimatedList[key]
                for str in temp:

                    if str not in matchEntity:
                        vector1 = text_to_vector(value)
                        vector2 = text_to_vector(str)
                        if get_cosine(vector1,vector2)>0.5:
                            # print value,str

                            partialMatch+=1
            if CMFlag==len(entitylist):
                missedEntityCount+=1
        for value in estimatedList[entity]:
            WHFlag = 0

            for key in entitylist:

                if value not in set(actualList[key]):
                    WHFlag+=1
                    # print value, WHFlag
            if WHFlag==len(entitylist):
                detectedWrongEntityCount+=1

    completeMiss=missedEntityCount-partialMatch
    wrongHit=detectedWrongEntityCount-partialMatch
    fullPrecision=calculateFullPrecision(fullMatch,partialMatch,wrongHit)
    fullRecall=calculateFullRecall(fullMatch,partialMatch,completeMiss)
    partialPreciion=calculatePartialPrecision(partialMatch,fullMatch,wrongHit)
    partialRecall=calculatePartialRecall(fullMatch,partialMatch,completeMiss)
    totalPrecisionPerQuestion=calculateTotalPrecision(fullPrecision,partialPreciion)
    totalRecallPerQuestion=calculateTotalRecall(fullRecall,partialRecall)
    overallTotalPrecision+=totalRecallPerQuestion
    overallTotalRecall+=totalRecallPerQuestion

    # print 'FullMatch : ', fullMatch
    # print 'PartialMatch : ', partialMatch
    # print 'Complete miss: ', completeMiss
    # print 'Wrong hit: ', wrongHit
    print 'Full presicion :', fullPrecision
    print 'Full Recall :', fullRecall
    print 'Partial presicion :', partialPreciion
    print 'Partial Recall :', partialRecall
    print 'Total presicion :', totalPrecisionPerQuestion
    print 'Total Recall: ', totalRecallPerQuestion
    return



def getOverallPrecision(i):
    overallPrecision=Decimal(overallTotalPrecision)/i
    return overallPrecision

def getOverallRecall(i):
    overallRecall=Decimal(overallTotalRecall)/i
    return overallRecall



