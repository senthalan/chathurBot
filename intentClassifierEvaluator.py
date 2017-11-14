from witAI import send_question
# from readQuestionsWit import *
from readQuestionsCoreNLP import *
from evaluationMetricCalculator import *
from collections import Iterable
from cosineCalculator import *
from CoreNLP import send_question_core_nlp

i=0

import sys

#Evaluate intent of question
truePositive=0
falsePositive=0
falseNegative=0

# def evaluate_intent(intent,actualIntent):
#
#     if intent==actualIntent:
#         # print "extracted intent + " + ((response['intent'])[0])['value']
#         return 1
#     else:
#         return 0
intentList=["model","onlineStore","brand","price","memory"]

def evaluateIntent(intent, actualIntent):
    predictedIntent=intent.lower()
    global truePositive,falsePositive,falseNegative
    if actualIntent==predictedIntent:
        truePositive+=1
    elif (actualIntent!=predictedIntent) and (predictedIntent in intentList):
        falsePositive+=1
    elif (actualIntent!='' and predictedIntent ==''):
        falseNegative+=1

def startEvaluateIntentExtractor():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    for i in range(len(questions) - 1):
        print "Question ", i + 1, ": ", questions[i]
        # intent, entities_list, extremum, comparator, order_by, order, limit = send_question(questions[i].strip())
        intent, entities_list, extremum, comparator, order_by, order, limit = send_question_core_nlp(questions[i].strip())
        print "Intent:", intent
        evaluateIntent(intent,intents[i])


if __name__ == "__main__":
     # Read the test file
    # readFileWit()
    readFileCoreNLP()
    questions = list(get_question())
    intents = list(get_intent())
    startEvaluateIntentExtractor()
    recall=calculateRecall(truePositive,falseNegative)
    precision=calculatePrecision(truePositive,falsePositive)
    fMeasure=calculateFMeasure(precision,recall)

    print
    print "-----------------------------INTEND EXTACTOR RESULT-----------------------------------"

    print "TP :" ,truePositive
    print "FP :" ,falsePositive
    print "FN :" , falseNegative
    print
    print "Precision :",precision
    print "Recall :",recall
    print "FMeasure :",fMeasure





