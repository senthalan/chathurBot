from witAI import send_question
from queryGenerator import generate_query
from databaseConnector import run_query
from readTrainingQuestions import get_question
from readTrainingQuestions import read_file
from readTrainingQuestions import get_query
from readTrainingQuestions import get_intent
from intentEvaluator import evaluate_intent
from calculation import calculateTruePositiveRate

ques=[]
j=0
global intentTP
global intentFN


def evaluateQuestion():
    intentTP=0
    intentFN=0

    for j in range(len(questions)):
        print 'Question :' + questions[j]
        response = send_question(questions[j])
        print response
        print "extracted intent + " + ((response['intent'])[0])['value']
        if evaluate_intent(response,intents[j]):
            intentTP +=1
        else:
            intentFN +=1

        query = generate_query(response)
        print "Generated query    : " + query
        print "Actual query     :" + queries[j]
        print "------------------------------------------------"
    return

def evaluateSystem():
    intent_TPR = calculateTruePositiveRate(intentTP, intentFN)
    print "intentTPR :" + intent_TPR
    return

if __name__ == "__main__":
    read_file()
    questions=list(get_question())
    queries=list(get_query())
    intents=list(get_intent())
    evaluateQuestion();
    evaluateSystem();
