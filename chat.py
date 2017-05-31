from witAI import send_question
from queryGenerator import generate_query
from databaseConnector import run_query
from answerGenerator import generate_answer

if __name__ == "__main__":
    repeat = True
    while repeat:
        # question = raw_input('Question : ')
        # if question.strip() == "":
        #     repeat = False
        # else:
        question = "what is the price of HTC Desire 310 Dual SIM"
        response = send_question(question.strip())
        query = generate_query(response)
        print "query    : " + query
        result = run_query(query)
        answer = generate_answer(result, response)
        print answer
        print
        repeat = False
