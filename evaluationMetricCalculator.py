from decimal import *


getcontext().prec=3
def calculateFullPrecision(FM, PM, WH):
    FP = Decimal(FM) /Decimal((FM + PM + WH))
    return FP


def calculatePartialPrecision(PM, FM, WH):
    PM = Decimal(PM) / Decimal((FM + PM + WH))
    return PM


def calculateFullRecall(FM, PM, CM):
    FR = Decimal(FM) / Decimal((FM + PM + CM))
    return FR


def calculatePartialRecall(FM, PM, CM):
    PR = Decimal(PM) / Decimal((FM + PM + CM))
    return PR


def calculateTotalPrecision(FP, PP):
    totalPrecision = FP + PP
    return totalPrecision


def calculateTotalRecall(FR, PR):
    totalRecall = FR + PR
    return totalRecall


def calculateTruePositiveRate(TP, FN):
    TPR = (Decimal(TP) / (Decimal(TP) + Decimal(FN)))
    # print TPR
    return TPR

def calculatePrecision(TP,FP):
    if TP==0 and FP==0:
        return 0
    else:
        return Decimal(TP)/Decimal(TP+FP)

def calculateRecall(TP,FN):
    return Decimal(TP)/Decimal(TP+FN)

def calculateFMeasure(precision,recall):
    if (precision ==0 and recall==0):
        return 0
    else:
        return (2*Decimal(precision)*Decimal(recall))/(Decimal(precision)+Decimal(recall))

def calculateSQLRecall(noOfQues,noOfGeneratedQuery):
    return Decimal(noOfGeneratedQuery)/Decimal(noOfQues)

def calcultaeSQLPrecision(noOfGeneratedQuery,noOfCorrectQuery):
    return Decimal(noOfCorrectQuery)/Decimal(noOfGeneratedQuery)