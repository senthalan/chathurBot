from witAI import send_question
from queryGenerator import generate_query
from databaseConnector import run_query
from answerGenerator import generate_answer
from spellCorrector import correction, load_table_data
from nltk.corpus import stopwords
from enchant.checker import SpellChecker
from enchant.tokenize import EmailFilter, URLFilter
import enchant


def find_ngrams(input, n):
    output = []
    for i in range(len(input) - n + 1):
        output.append(' '.join(input[i:i + n]))
    return output


if __name__ == "__main__":
    stopWord = stopwords.words('english')
    stopWord.append('?')
    s = set(stopWord)
    database_name = load_table_data()
    chkr = SpellChecker("en_US", filters=[EmailFilter, URLFilter])
    for name in database_name:
        ns = name.split()
        for n in ns:
            chkr.add(n)
    questions = ['What are the Apple phone models available in www.ideabeam.com ?',
                 'Where can i get Aple iPhne 6s 16GB ?',
                 'Where can i get HTC brnd phones ?',
                 'What is the brand of Mirosoft Lmia 430 Dual SIM ?',
                 'What is the maximum price of HC Desire 826 Dual Sim ?',
                 'What is the least price of Samsug Galaxy S5 ?']
    for question in questions:
        question_without_stop_words = filter(lambda w: not w in s, question.split())
        # question_set = []
        # for j in range(1, 7):
        #     n_grams = find_ngrams(question_without_stop_words, j)
            # if j == 1:
            #     for word in n_grams:
            #         if not d.check(word):
            #             print "correcting word", word, d.suggest(word)
            # question_set.extend(n_grams)
        # database_entity = list(set(database_name) & set(question_set))
        # database_entity.sort(key=len, reverse=True)
        # start = question.find(database_entity[0])
        # end = start + len(database_entity[0]) + 1
        # entities = [database_entity[0]]
        # for i in range(1, len(database_entity)):
        #     inner_start = question.find(database_entity[i])
        #     inner_end = inner_start + len(database_entity[i]) + 1
        #     if not ((start <= inner_start <= end) and (start <= inner_end <= end)):
        #         entities.append(database_entity[i])
        # print "final entities", entities
        # print "---------------------------------------------------------"
        # chkr.set_text(question)
        # for err in chkr:
        #     print "ERROR:", err.word, d.suggest(err.word)
        for word in question_without_stop_words:
            if not chkr.check(word):
                print chkr.suggest(word)
        print
        # intent, entities_list, extremum, comparator, order_by, order, limit = send_question(question.strip())
        # print ("intent : " + intent)
        # # print ("entities_list : " + entities_list)
        # print ("extremum : " + extremum)
        # print ("comparator : " + comparator)
        # print ("order_by : " + order_by)
        # print ("order : " + order)
        # print ("limit : " + limit)
        # query = generate_query(intent, entities_list, extremum, comparator, order_by, order,limit)
        # print "query    : " + query
        # result = run_query(query)
        # answer = generate_answer(result, intent)
        # print ("----------------------------------")
        # print
