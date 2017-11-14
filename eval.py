from witAI import send_question
from queryGenerator import generate_query
from databaseConnector import run_query
from readQuestionsWit import *

from intentEvaluator import evaluate_intent
from calculation import calculateTruePositiveRate
from sqlEvaluator import *
import unicodedata
from entityEvaluator import *

ques=[]
j=0

intentTP = 0
intentFN = 0
noOfGeneratedQueries=0

def evaluateQuestion():

    global intentTP,intentval
    global intentFN,noOfGeneratedQueries
    for j in range(len(questions)-1):
        print 'Question ',j+1,':'+ questions[j]
        actualEntityList=generateEntityList(entitiesList[j])

        evaluatedEntityList = {}
        response = send_question(questions[j])

        for key in response:
            if key == 'intent':
                intent = ((response[key])[0])['value']

            else:
                entities = (response[key])
                values = []
                for entity in entities:

                    values.append((unicodedata.normalize('NFKD', unicode(entity['value'])).encode('ascii', 'ignore')).lower())
                    evaluatedEntityList[unicodedata.normalize('NFKD',key.lower()).encode('ascii', 'ignore')] = values

        if evaluate_intent(response,intents[j]):
            intentTP +=1
            intentval="Intent is identified correctly"
            #print 'intentTP:', intentTP
        else:
            intentFN +=1
            intentval="Intent is identified incorrectly"
            #print 'intentFN: ',intentFN

        #evaluate entity
        #print 'evaluate entity'
        print "Evaluation results per question :"
        print "_________________________________"
        print "Intent: " + intentval
        eveluateEntityPerQuestion(actualEntityList,evaluatedEntityList)

        #evaluate query
        query = generate_query(response)

        if len(query)!=0:
            estimatedAnswers=[]
            noOfGeneratedQueries+=1
            print " Generated Query    : " + query

            actualAns=get_answers()[j]
            estimatedAnswers = run_query(query)
            print 'actual Answers:', actualAns
            print 'estimatedAnswers :' ,estimatedAnswers
            evaluateSqlPerQuestion(actualAns,estimatedAnswers)
            print "------------------------------------------------"
            print '\n'
        else:
            break

    return

def evaluateSystem():

    intent_TPR = calculateTruePositiveRate(intentTP, intentFN)
    overallEntityPrecision=getOverallPrecision(len(questions))
    overallEntityRecall=getOverallRecall(len(questions))
    # print len(questions), noOfGeneratedQueries, getNoOfCorrectQueries()
    overallSQLPrecision=calcultaeSQLPrecision(noOfGeneratedQueries,getNoOfCorrectQueries())
    overallSQLRecall=calculateSQLRecall(len(questions),noOfGeneratedQueries)
    fmeasure=calculateFMeasure(overallSQLPrecision,overallSQLRecall)
    print "True Positive Ratio for intent Extraction :" , intent_TPR
    print "Precision Entity Extraction :", overallEntityPrecision
    print "Recall Entity Extraction :", overallEntityRecall

    print "Precision for Query Generation: ",overallSQLPrecision
    print "Recall for Query Generation:", overallSQLRecall
    print "F-Measure for Query :" , fmeasure
    return

if __name__ == "__main__":
    readFileWit()

    questions=list(get_question())
    queries=list(get_query())
    intents=list(get_intent())
    entitiesList=list(get_entities())
    evaluateQuestion();
    print "\n \n Evaluation results for overall system"
    print "----------------------------------------"
    evaluateSystem();
