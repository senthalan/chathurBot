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

intentTP = 0
intentFN = 0

def evaluateQuestion():
    global intentTP
    global intentFN
    for j in range(len(questions)-1):
        print 'Question :' + questions[j]
        response = send_question(questions[j])
        if evaluate_intent(response,intents[j]):
            intentTP +=1
            print intentTP
        else:
            intentFN +=1
            print intentFN
        print "------------------------------------------------"
    return

def evaluateSystem():
    print intentFN
    intent_TPR = calculateTruePositiveRate(intentTP, intentFN)
    print "intentTPR :" , intent_TPR
    return

if __name__ == "__main__":
    read_file()
    questions=list(get_question())
    queries=list(get_query())
    intents=list(get_intent())
    evaluateQuestion();
    evaluateSystem();
