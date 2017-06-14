from calculation import *

noOfCorrectQueries=0
def evaluateSqlPerQuestion(actualAns,estimatedAns):
    global noOfCorrectQueries

    TP=len(set(actualAns).intersection(estimatedAns))

    FP=len(set(estimatedAns).difference(actualAns))

    FN=len(set(actualAns).difference(estimatedAns))

    precision=calculatePrecision(TP,FP)
    recall=calculateRecall(TP,FN)
    if precision==0 and recall==0:
        fMeasure=0
    else:
        fMeasure=calculateFMeasure(precision,recall)
    if(fMeasure>=0.75):

        noOfCorrectQueries+=1
    print "Precision,recall,F-Measure for query : ",precision, '    ',recall,'   ',fMeasure
def getNoOfCorrectQueries():
    return noOfCorrectQueries