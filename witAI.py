import json
import urllib

import requests as requests
from configReader import read_config

access_token = read_config("witaiToken")


def load_entity(entity, values):
    url = 'https://api.wit.ai/entities?v=20160526'
    headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
    payload = {'id': entity,
               'values': values}

    r = requests.post(url, data=json.dumps(payload), headers=headers)
    if r.status_code == 200:
        print 'entity uploaded successfully ' + entity
    else:
        print 'something went wrong when uploading ' + entity + ': error code ' + str(r.status_code)
        print r.content


def load_intent(intents):
    values = []
    for intent in intents:
        value = {'value': intent,
                 'expressions': []
                 }
        values.append(value)

    payload = {'values': values}
    url = 'https://api.wit.ai/entities/intent?v=20160526'
    headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
    r = requests.put(url, data=json.dumps(payload), headers=headers)
    if r.status_code == 200:
        print 'intents uploaded '
    else:
        print 'something went wrong when updating intent ' + ': error code ' + str(r.status_code)
        print r.content


comparator_map = {"more": ">=", "less": "<=", "equal": "=", "between": "between"}
order_map = {"highest": "DES", "lowest": "ASC"}
entity_map = {"number": "memory", "amount_of_money": "price", "model": "model", "company": "company", "onlineStore": "onlineStore", "brand" : "brand"}
limit_map = {"is" : "1", "are" : ""}

def send_question(question):
    question = urllib.quote(question)
    url = 'https://api.wit.ai/message?v=20170324&q=' + question
    headers = {'Authorization': 'Bearer ' + access_token}

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print r.content
        return -1
    else:
        response = json.loads(r.content)
    response = response['entities']

    intent = ''
    entities_list = {}
    extremum = ''
    comparator = "="
    order_by = ''
    order = ''
    limit = ''
    # reading the response
    for key in response:
        if key == 'intent':
            intent = ((response[key])[0])['value']
        elif key == 'extremum':
            extremum = ((response[key])[0])['value']
        elif key == 'comparator':
            comparator = comparator_map[((response[key])[0])['value']]
        elif key == 'rank_for':
            order_by = ((response[key])[0])['value']
        elif key == 'rank':
            order = order_map[((response[key])[0])['value']]
        elif key =='limit' :
            limit = limit_map[((response[key])[0])['value']]
        else:
            entities = (response[key])
            values = []
            for entity in entities:
                values.append(str(entity['value']))
            entities_list[entity_map[key]] = values

    return intent, entities_list, extremum, comparator, order_by, order, limit
