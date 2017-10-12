from evaluationMetricCalculator import *
from collections import Iterable
from systemEvaluator import flatten

noOfCorrectQueries=0

def evaluateSqlPerQuestion(actualAns,estimatedAns):
    global noOfCorrectQueries
    # print actualAns
    # print estimatedAns

    TP=len(set(actualAns).intersection(set(estimatedAns)))
    FP=len(set(estimatedAns).difference(set(actualAns)))
    FN=len(set(actualAns).difference(set(estimatedAns)))
    print TP,FP,FN
    precision=calculatePrecision(TP,FP)
    recall=calculateRecall(TP,FN)


    if precision==0 and recall==0:
        fMeasure=0
    else:
        fMeasure=calculateFMeasure(precision,recall)
    if(fMeasure>=0.75):

        noOfCorrectQueries+=1

    print "\t Query measure:"
    print "\t   Recall : ",recall
    print "\t   Precision : ",precision
    print "\t   FMeasure : ",fMeasure


def getNoOfCorrectQueries():
    return noOfCorrectQueries