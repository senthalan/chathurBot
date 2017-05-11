from decimal import *

getcontext().prec=3
def calculateFullPrecision(FM, PM, WH):
    FP = FM / (FM + PM + WH)
    return FP


def calculatePartialPrecision(PM, FM, WH):
    PM = PM / (FM + PM + WH)
    return PM


def calculateFullRecall(FM, PM, CM):
    FR = FM / (FM + PM + CM)
    return FR


def calculatePartialRecall(FM, PM, CM):
    PR = PM / (FM + PM + CM)
    return PR


def calculateTotalPrecision(FP, PP):
    totalPrecision = FP + PP
    return totalPrecision


def calculateTotalRecall(FR, PR):
    totalRecall = FR + PR
    return totalRecall


def calculateTruePositiveRate(TP, FN):

    TPR = (Decimal(TP) / (Decimal(TP) + Decimal(FN)))
    print TPR
    return TPR
