import json
import urllib
import requests as requests

from IntentClassificationNeuralNetworks import classifyNN

comparator_map = {"more": ">=", "less": "<=", "equal": "=", "between": "between"}
order_map = {"highest": "DESC", "lowest": "ASC"}
entity_map = {"number": "memory", "amount_of_money": "price", "model": "model", "company": "company",
              "online_store": "onlineStore", "brand": "brand"}
limit_map = {"is": "1", "are": ""}


def send_question_core_nlp(question):
    intent = classifyNN(question)
    question = urllib.quote(question)
    url = 'http://localhost:8080/entity/extract?question=' + question

    r = requests.get(url)
    if r.status_code != 200:
        print r.content
        return -1
    else:
        response = json.loads(r.content)

    entities_list = {}
    extremum = ''
    comparator = "="
    order_by = ''
    order = ''
    limit = ''
    # reading the response
    for key in response:
        key_str = str(key).lower()
        if key_str == 'intent':
            intent = response[key]
        elif key_str == 'extremum':
            extremum = response[key]
        elif key_str == 'comparator':
            comparator = comparator_map[response[key]]
        elif key_str == 'rank_for':
            order_by = response[key]
        elif key_str == 'rank':
            order = order_map[response[key]]
        elif key_str == 'limit':
            limit = limit_map[response[key]]
        else:
            entities_list[entity_map[key_str]] = [response[key]]

    return intent, entities_list, extremum, comparator, order_by, order, limit
