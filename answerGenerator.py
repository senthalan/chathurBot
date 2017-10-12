import unicodedata
import json, ast
from ast import literal_eval
def generate_answer(answers, intent):
    answerList=[]
    # print answers
    # if len(answers) == 1:
    #     print 3
    #     print intent + " is "+ str(answers[0][0])
    #     print 4
    # else:
    #     print 5
    #     print "no answer"
    #     print 6
    # # print "still working"



    for tup in answers:
        answerList = answerList + [str(item).encode('ascii', 'backslashreplace') for item in tup]
    return toString(answerList)

def toString(answerList):
    result=[]
    for val in answerList:

        result.append(str(val))
    return result




