from witAI import send_question
from queryGenerator import generate_query
from databaseConnector import run_query

if __name__ == "__main__":
    repeat = True
    while repeat:
        question = raw_input('Question : ')
        if question.strip() == "":
            repeat = False
        else:
            response = send_question(question.strip())
            query = generate_query(response)
            print "query    : " + query
            answers = run_query(query)
            print answers
            print
