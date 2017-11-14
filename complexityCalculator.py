
from readQuestionsWit import *
import math
from decimal import *

operators=["AND","OR","=","<",">","+","-","/","*","||","!=","^=","<>",">=","<=","IN","ANY","SOME","NOT IN","IN","ALL","BETWEEN",
           "like","NULL","IS","DESC","ASC"]

expressions=["UNION","UNION ALL","MINUS","INTERSECT","JOIN","GROUP BY", "ORDER BY","DISTINCT"]

functions=["MIN","MAX","SUM","COUNT","*"]
coloumns=["model","brand","onlineStore","memory","price"]

operatorCount=0
expressionCount=0
distinctColumn=0
coloumnCount=0
functionCount=0


def calculateComplexity():
    global operatorCount,expressionCount,distinctColumn,functionCount,coloumnCount
    querySet=get_query()
    intentSet=get_intent()
    entityTypeList=get_entities()
    for i in range(len(querySet)-1):
        print
        print "Question ", i + 1, " :     "
        print querySet[i]
        queryContent=querySet[i].split(" ");
        distinctQueryContent=[]

        for content in queryContent:
            if content not in distinctQueryContent:
                distinctQueryContent.append(content)

        # print queryContent
        # print distinctQueryContent
        # calculate distict operators and expressions
        for word in distinctQueryContent:
            if word in operators:
                operatorCount+=1
            if word in expressions:
                expressionCount+=1
        # calculate distinct functions
        minword="min("+intentSet[i]+")"
        maxword = "max(" + intentSet[i] + ")"

        if minword in queryContent:
            functionCount+=1
        if maxword in queryContent:
            functionCount+=1

        # calculate distinct coloumn names
        # currently system supports only one intent
        for j in distinctQueryContent:
            if j in coloumns:
                distinctColumn+=1

        # calculate coloumn names
        for k in queryContent:
            if k in coloumns:
                coloumnCount+=1

        totalOperators = operatorCount + expressionCount + functionCount
        # print totalOperators, distinctColumn
        logValue=Decimal(math.log((totalOperators+distinctColumn),2))
        complexity=Decimal((totalOperators*coloumnCount*logValue))/Decimal(2*distinctColumn)
        print "Complexity :     ",round(complexity,3)

        # print operatorCount
        # print expressionCount
        # print functionCount
        # print distinctColumn
        # print coloumnCount
        # complexity=intentCount*(functionCount+expressionCount+operatorCount)*()
        operatorCount=0
        expressionCount=0
        distinctColumn=0
        coloumnCount=0
        functionCount=0





if __name__ == "__main__":
    #Read the test file
    readFileWit()
    calculateComplexity()





