from witAI import send_question
from queryGenerator import generate_query
from databaseConnector import run_query
from readTrainingQuestions import get_question
from readTrainingQuestions import read_file
from readTrainingQuestions import get_query

ques=[]
j=0

if __name__ == "__main__":
    read_file()
    questions=list(get_question())
    queries=list(get_query())
    for j in range(len(questions)):
        print 'Question :' + questions[j]
        intent, entities_list, extremum, comparator, order_by, order = send_question(questions[j])
        query = generate_query(intent, entities_list, extremum, comparator, order_by, order)
        print "Generated query    : " + query
        print "Actual query     :" + queries[j]
        print "------------------------------------------------"