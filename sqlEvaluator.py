from evaluationMetricCalculator import *

actualSelectClause="Select model,brand"
generatedSelectClause="select model,price"
actualFromClause="from electronics"
generatedFromClause="from electronics"
actualWhereClause="where brand like 'apple'"
generatedWhereClause="where model like 'apple'"

#this class evaluate each sub prt of sql query and weight thos measures

#calculate the evaluation measure of select query
actualSelectClauseVal=[]
actualFromClauseVal=[]
actualWhereClauseVal=[]
generatedSelectClauseVal=[]
generatedFromClauseVal=[]
generatedWhereClauseVal=[]
temp=[]
selectRecall=0
selectPrecision=0


def getActualClauseVal():

    temp_s=actualSelectClause.split(" ")
    for val in temp_s[1].split(","):
        actualSelectClauseVal.append(val)

    temp_f=actualFromClause.split(" ")
    for val in temp_f[1].split(","):
        actualFromClauseVal.append(val)

    temp_w=actualWhereClause.split("where")
    actualWhereClauseVal.append(temp_w[1])

def getGeneratedClauseVal():

    temp_gs=generatedSelectClause.split(" ")
    for val in temp_gs[1].split(","):
        generatedSelectClauseVal.append(val)

    temp_f=generatedFromClause.split(" ")
    for val in temp_f[1].split(","):
        generatedFromClauseVal.append(val)

    temp_w=generatedWhereClause.split("where")
    generatedWhereClauseVal.append(temp_w[1])

def evaluateSelectClause():
    falsePositve=0
    falseNegative=0
    truePositive=len(set(actualSelectClauseVal).intersection(generatedSelectClauseVal))

    for value in generatedSelectClauseVal:
        if(value not in actualSelectClauseVal):
            falsePositve+=1

    for value in actualSelectClauseVal:
        if(value not in generatedSelectClauseVal):
            falseNegative+=1


    selectPrecision=calculatePrecision(truePositive,falsePositve)
    selectRecall=calculateRecall(truePositive,falseNegative)
    print selectPrecision,selectRecall

def evaluateFromClause():
    falsePositive=0
    falseNegative=0
    truePositive=len(set(actualFromClauseVal).intersection(generatedFromClauseVal))


    for value in generatedFromClauseVal:
        if(value not in actualFromClauseVal):
            print value
            falsePositive+=1

    for value in actualFromClauseVal:
        if(value not in generatedFromClauseVal):
            print value
            falseNegative+=1

    fromPrecision=calculatePrecision(truePositive,falsePositive)
    fromRecall=calculateRecall(truePositive,falseNegative)
    print fromPrecision,fromRecall


if __name__ == "__main__":
    getActualClauseVal()
    getGeneratedClauseVal()
    evaluateSelectClause()
    evaluateFromClause()







