# from witAI import send_question
from queryGenerator import generate_query
from databaseConnector import run_query
# from readQuestionsWit import *
from CoreNLP import send_question_core_nlp
from readQuestionsCoreNLP import *
from evaluationMetricCalculator import *
from collections import Iterable
from cosineCalculator import *
from difflib import SequenceMatcher
from evaluateSql import *
from answerGenerator import generate_answer

from queryClassifier import train, predit_query

from intentEvaluator import evaluate_intent

i=0

#measures for intent
intentTP=0
intentFN=0
overallTotalPrecision=0
overallTotalRecall=0
overallFullPrecision=0
overallFullRecall=0
entityTypeList=['model','brand','onlineStore','memory','price']
model=[]
brand=[]
onlineStore=[]
number=[]
money=[]
fullMatch=0
completeMiss=0
partialMatch=0
wrongHit=0
passedQuery=0
import sys

def startEvaluate():
    train()
    reload(sys)
    sys.setdefaultencoding('utf-8')
    global intentTP
    global intentFN

    global completeMiss,partialMatch,fullMatch,wrongHit

    for i in range(len(questions)-1):
        print "Question ",i+1,": ",questions[i]
        # intent, entities_list, extremum, comparator, order_by, order, limit = send_question(questions[i].strip())
        intent, entities_list, extremum, comparator, order_by, order, limit = send_question_core_nlp(questions[i].strip())
        print "output from wit:",intent,entities_list,extremum,comparator,order_by,order,limit
        # print "start"
        # intent="price"
        # entities_list={}
        # entities_list['onlineStore']=['http://telescience.lk','apple','http://aab.lk']
        # entities_list['model']=['HTC Desire 326G','nokia']
        # entities_list['brand'] = ['apple', 'noia','aaacf']
        # extremum='phone'
        # order='at'
        # comparator='more'
        # order_by=''
        # limit='3'
        #evaluate intent accuracy

        if evaluate_intent(intent, intents[i]):
            intentTP += 1
            print "\t Intend : is identified correctly"
            # print "intend",intent
            intentFlag = True
        else:
            intentFN += 1
            print "\t Intend : is not identified correctly"
            intentFlag = False

        calculatePassedQueries(intentFlag)
    #fill the empty entity list
        for entity in entityTypeList:
            if entity not in entities_list:
                entities_list[entity]=[]
        #evaluate entity accuracy
        actutalListx=generateEntityList(entitiesList[i])

        fullMatch=calculateFullMatch(entities_list,actutalListx,extremum,comparator,order_by,order,limit)
        completeMiss,partialMatch,wrongHit=calculateCompleteMiss(entities_list,actutalListx,extremum,comparator,order_by,order,limit)
        evaluateEntityExtraction()
        # print 'fullmatch: ',fullMatch
        # print 'completeMiss:',completeMiss
        # print 'partialMatch:',partialMatch
        # print 'wrongHit:',wrongHit


        # TODO comment below code to execute wit.ai. this is applicable for coreNLP
        storeVal=[]
        for store in entities_list["onlineStore"]:
            storeVal.append("http://"+store)
        entities_list["onlineStore"]=storeVal
        # generatedQuery=generate_query(intent,entities_list,extremum,comparator,order_by,order,limit)
        generatedQuery = predit_query(intent, entities_list, extremum, comparator, order_by, order, limit)
        if generatedQuery!="NULL" and intent!="":
            print "actual query :" + queries[i]
            print "\t Generated query    : " + generatedQuery
            result = run_query(generatedQuery)


            # answer = generate_answer(result, intent)
            print result
            print answers[i]

            evaluateSqlPerQuestion(answers[i],result)
        print ("---------------------------------------------------------------------------------------------------------")
        print



def flatten(lis):
     for item in lis:
         if isinstance(item, Iterable) and not isinstance(item, basestring):
             for x in flatten(item):
                 yield x
         else:
             yield item

def calculateFullMatch(identifiedList,actualList,extremum,comparator, order_by, order, limit):
    fullMatch=0
    temp={}
    for entity in entityTypeList:

        if (len(list(flatten(actualList[entity])))!=0) and (len(identifiedList[entity])!=0) :

            fullMatch+=len(set(list(flatten(actualList[entity]))) & set(identifiedList[entity]))
            # fullMatch

    if extremum != '':
        if extremum in list(flatten(actualList['extremum'])):
            fullMatch+=1
    if comparator != '=':
        if comparator in list(flatten(actualList['comparator'])):
            fullMatch+=1
    if order_by != '':
        if order_by in list(flatten(actualList['rank_for'])):
            fullMatch+=1
    if order != '':
        if order in list(flatten(actualList['rank'])):
            fullMatch+=1
    if limit != '':
        if limit in list(flatten(actualList['limit'])):
            fullMatch+=1
    return fullMatch

def calculateCompleteMiss(identifiedList,actualList,extremum,comparator, order_by, order, limit):
    completeMiss = 0
    partialMatch=0
    wrongHit=0
    tempActualList={}
    tempGeneratedList={}

    for entity in entityTypeList:
        tempA=list(flatten(actualList[entity]))
        tempB=list(flatten(identifiedList[entity]))
        partialMatchList=[]
        for x in set(list(flatten(actualList[entity]))) & set(identifiedList[entity]):
            tempA.remove(x)
            tempB.remove(x)
        for x in tempA:
            flag=False
            for y in tempB:
                # vector1=text_to_vector(x)
                # vector2=text_to_vector(y)
                if SequenceMatcher(None,x,y).ratio() > 0.5:
                    partialMatch+=1
                    # print "pm"
                    # print x,y

                    tempB.remove(y)
                    flag=True
                    break
                elif SequenceMatcher(None,x,y).ratio() ==0:
                    flag=False
            if flag==False:
                completeMiss+=1
        wrongHit+=len(tempB)


    if len(list(flatten(actualList['extremum'])))!=0 and extremum=='':
        completeMiss+=1
    if len(list(flatten(actualList['comparator'])))!=0 and comparator == '=':
        completeMiss+=1
    if len(list(flatten(actualList['rank_for'])))!=0 and order_by == '':
        completeMiss+=1
    if len(list(flatten(actualList['rank']))) !=0 and order == '':
        completeMiss+=1
    if len(list(flatten(actualList['limit']))) !=0 and limit == '':
        completeMiss+=1

    if extremum != '':
        if extremum not in list(flatten(actualList['extremum'])):
            wrongHit += 1
    if comparator != '=':
        if comparator not in list(flatten(actualList['comparator'])):
            wrongHit += 1
    if order_by != '':
        if order_by not in list(flatten(actualList['rank_for'])):
            wrongHit += 1
    if order != '':
        if order not in list(flatten(actualList['rank'])):
            wrongHit += 1
    if limit != '':
        if limit not in list(flatten(actualList['limit'])):
            wrongHit += 1

    # print "partialMatch",partialMatch
    # print "completeMiss",completeMiss
    return completeMiss,partialMatch,wrongHit


def evaluateIntentClassificationModel():
    intentModelPrecision=calculateTruePositiveRate(intentTP,intentFN)
    print "True Positive Rate of intent Classification Model :", intentModelPrecision

def evaluateEntityExtraction():
    global overallTotalPrecision,overallTotalRecall,overallFullPrecision,overallFullRecall
    fullPrecision = calculateFullPrecision(fullMatch, partialMatch, wrongHit)
    fullRecall = calculateFullRecall(fullMatch, partialMatch, completeMiss)
    partialPreciion = calculatePartialPrecision(partialMatch, fullMatch, wrongHit)
    partialRecall = calculatePartialRecall(fullMatch, partialMatch, completeMiss)
    totalPrecisionPerQuestion = calculateTotalPrecision(fullPrecision, partialPreciion)
    totalRecallPerQuestion = calculateTotalRecall(fullRecall, partialRecall)

    print "\t Entity Extraction Result : "
    print "\t   Recall of Question : ", totalRecallPerQuestion
    print "\t   Precision of Question :",totalPrecisionPerQuestion
    totalFMeaurePerQuestion = calculateFMeasure(totalPrecisionPerQuestion, totalRecallPerQuestion)
    print "\t   Fmeasure of Question :" , totalFMeaurePerQuestion
    overallTotalPrecision += totalPrecisionPerQuestion
    overallTotalRecall += totalRecallPerQuestion
    overallFullPrecision+=fullPrecision
    overallFullRecall+=fullRecall

def evaluateSystem():
    # print "overall",passedQuery,getNoOfCorrectQueries(),len(questions)
    print passedQuery,getNoOfCorrectQueries(),len(questions)
    systemRecall=Decimal(passedQuery)/Decimal(len(questions))
    systemPrecision=Decimal(getNoOfCorrectQueries())/Decimal(passedQuery)
    systemFmeasure=calculateFMeasure(systemPrecision,systemRecall)
    print "Query Generator Recall : " , systemRecall
    print "Query Generator Precision : ", systemPrecision
    print "Query Generator Fmeasure : ", systemFmeasure

    return systemRecall,systemPrecision


def evaluateEntityExtractionModel(noOfQuestion):
    overallPrecision = Decimal(overallTotalPrecision) / noOfQuestion
    overallRecall = Decimal(overallTotalRecall) / noOfQuestion
    overallSystemFullRecall=Decimal(overallFullRecall) / noOfQuestion
    overallSystemFullPrecision=Decimal(overallFullPrecision) / noOfQuestion
    overallSystemFMeasure=Decimal(calculateFMeasure(overallSystemFullPrecision,overallSystemFullRecall))
    overallFmeasure = Decimal(calculateFMeasure(overallPrecision,overallRecall))
    print "entityExtractor : Traditional Approach : "
    print "Entity Extraction Model Recall :", overallSystemFullRecall
    print "Entity Extraction Model Precision :", overallSystemFullPrecision
    print "Entity Extraction Model fmeasure :", overallSystemFMeasure

    print "entityExtractor : Adopted Approach : "
    print "Entity Extraction Model Recall :",overallRecall
    print "Entity Extraction Model Precision :",overallPrecision
    print "Entity Extraction Model fmeasure :", overallFmeasure

    return  overallRecall,overallPrecision

def calculatePassedQueries(intentFlag):
    global passedQuery

    if(intentFlag):
        passedQuery+=1

if __name__ == "__main__":
    #Read the test file
    # readFileWit()
    readFileCoreNLP()
    questions=list(get_question())
    queries=list(get_query())
    intents=list(get_intent())
    answers=list(get_answers())
    entitiesList=list(get_entities())
    startEvaluate()
    print
    print
    print
    print "-----------------------------OVER ALL SYSTEM RESULT-----------------------------------"

    evaluateIntentClassificationModel()
    evaluateEntityExtractionModel(len(questions))
    evaluateSystem()





