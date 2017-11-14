import json
import urllib
import requests as requests

from ExtremumClassificationNeuralNetworks import classifyExtremumNN
from IntentClassificationNeuralNetworks import classifyIntentNN

comparator_map = {"more": ">=", "less": "<=", "equal": "=", "between": "between"}
order_map = {"highest": "DES", "lowest": "ASC", "least":"ASC" }
entity_map = {"memory": "memory", "price": "price", "model": "model", "company": "company",
              "online_store": "onlineStore", "brand": "brand"}
limit_map = {"is": "1", "are": ""}


def send_question_core_nlp(question):
    intent = classifyIntentNN(question)
    extremum = classifyExtremumNN(question)
    if extremum == 'none':
        extremum = ''
    question = urllib.quote(question)
    url = 'http://localhost:8080/entity/extract?question=' + question

    r = requests.get(url)
    if r.status_code != 200:
        print r.content
        return -1
    else:
        response = json.loads(r.content)
    print "response",response

    entities_list = {}
    comparator = "="
    order_by = ''
    order = ''
    limit = ''
    # reading the response
    for key in response:
        key_str = str(key).lower()
        if key_str == 'intent':
            intent = response[key]
        elif key_str == 'comparator':
            comparator = comparator_map[response[key]]
        elif key_str == 'rank_for':
            order_by = response[key]
        elif key_str == 'rank':
            order = order_map[response[key]]
        elif key_str == 'limit':
            limit = limit_map[response[key]]
        else:
            try:
                entities = (response[key])
                values = []
                for entity in entities:
                    if key_str=="price":
                        values.append(str(entity)[2:])
                    elif key_str=="online_store":
                        values.append(str(entity)[7:])
                    else:
                        values.append(str(entity))
                    entities_list[entity_map[key_str]] = values
            except:
                print "Value Error"
    print "intent: ",intent
    print "entity:",entities_list
    print "extremum:", extremum
    print "comparator:",comparator
    print "orderby:",order_by
    print "order:", order
    print "limit:",limit

    return intent, entities_list, extremum, comparator, order_by, order, limit
