from witAI import send_question
from queryGenerator import generate_query
from databaseConnector import run_query
from readTrainingQuestions import get_question
from readTrainingQuestions import read_file
from readTrainingQuestions import get_query
from readTrainingQuestions import get_intent
from readTrainingQuestions import get_entities
from readTrainingQuestions import generateEntityList
from intentEvaluator import evaluate_intent
from calculation import calculateTruePositiveRate
import unicodedata
from entityEvaluator import eveluateEntity

ques=[]
j=0

intentTP = 0
intentFN = 0

def evaluateQuestion():

    global intentTP
    global intentFN
    for j in range(len(questions)-1):
        print 'Question :' + questions[j]
        actualEntityList=generateEntityList(entitiesList[j])

        evaluatedEntityList = {}
        response = send_question(questions[j])

        for key in response:
            if key == 'intent':
                intent = ((response[key])[0])['value']

            else:
                entities = (response[key])
                values = []
                for entity in entities:

                    values.append((unicodedata.normalize('NFKD', unicode(entity['value'])).encode('ascii', 'ignore')).lower())
                    evaluatedEntityList[unicodedata.normalize('NFKD',key.lower()).encode('ascii', 'ignore')] = values

        if evaluate_intent(response,intents[j]):
            intentTP +=1
            print 'intentTP:', intentTP
        else:
            intentFN +=1
            print 'intentFN: ',intentFN

        #evaluate entity
        print 'evaluate entity'
        eveluateEntity(actualEntityList,evaluatedEntityList)
        print "------------------------------------------------"
        print '\n'
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
    entitiesList=list(get_entities())
    evaluateQuestion();
    evaluateSystem();
