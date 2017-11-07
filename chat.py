from witAI import send_question
from queryGenerator import generate_query
from databaseConnector import run_query
from answerGenerator import generate_answer
from queryClassifier import train, predit_query

if __name__ == "__main__":
    train()
    questions = ['What are the Apple phone models available in http://www.ideabeam.com?',
                 'Where can i get Apple iPhone 6s 16GB?',
                 'Where can i get HTC brand phones?',
                 'What is the brand of Microsoft Lumia 430 Dual SIM?',
                 'What is the maximum price of HTC Desire 826 Dual Sim?',
                 'What is the least price of Samsung Galaxy S5?']
    for question in questions:
        print question
        intent, entities_list, extremum, comparator, order_by, order, limit = send_question(question.strip())
        print ("intent : " + intent)
        print (entities_list)
        print ("extremum : " + extremum)
        print ("comparator : " + comparator)
        print ("order_by : " + order_by)
        print ("order : " + order)
        print ("limit : " + limit)
        query = generate_query(intent, entities_list, extremum, comparator, order_by, order, limit)
        # predit_query(intent, entities_list, extremum, comparator, order_by, order, limit)
        print "query    : " + query
        result = run_query(query)
        answer = generate_answer(result, intent)
        print ("----------------------------------")
        print
        break
