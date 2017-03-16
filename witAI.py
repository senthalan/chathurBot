import json

import requests as requests
from readTrainingQuestions import read_training_questions
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
        training_questions = read_training_questions(intent)
        value = {'value': intent,
                 'expressions': training_questions
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
