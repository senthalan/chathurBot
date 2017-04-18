import json
import urllib

import requests as requests
from configReader import read_config

access_token = read_config("witaiToken")
equality_map = {"greater": ">=", "less": "<=", "equal": "="}
entity_map = {"number": "ram_size", "amount_of_money": "price", "model": "model", "company": "company", "link": "link"}


def send():
    question = "show me the apple phones with more than 6 gb memory"
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
    print response
    generate(response)


def generate(response):
    query_template = u"SELECT DISTINCT {select} FROM electronics WHERE {expression}"
    where_template = u"{entity_key} {equality} {entity_value}"
    where_between_template = u"{entity_key} BETWEEN {entity_value_one} AND {entity_value_two}"
    entities_list = {}
    intent = ''
    select = ''
    equality = ''
    max_min = ''
    where_list = []
    for key in response:
        if key == 'intent':
            intent = ((response[key])[0])['value']
            print "intent : " + intent
        else:
            entities = (response[key])
            values = []
            for entity in entities:
                values.append(entity['value'])
            entities_list[key] = values
    intent_split = intent.split('_')
    if len(intent_split) == 2:
        if (intent_split[0] == "Max") or (intent_split[0] == "Min"):
            select = intent_split[1].lower()
            max_min = intent_split[0]
        else:
            select = intent_split[0]
            equality = intent_split[1]
            keys = entities_list.keys()
            for key in keys:
                entity_value = entities_list.pop(key, None)
                if (key == "number") or (key == "amount_of_money"):
                    if equality != "between":
                        where_query = where_template.format(entity_key=entity_map[key], equality=equality_map[equality],
                                                            entity_value=str(entity_value[0]))
                        where_list.append(where_query)
                    else:
                        where_query = where_between_template.format(entity_key=entity_map[key],
                                                                    entity_value_one=str(entity_value[0]),
                                                                    entity_value_two=str(entity_value[1]))
                        where_list.append(where_query)
                else:
                    where_query = where_template.format(entity_key=key, equality=equality_map["equal"],
                                                        entity_value="\"" + entity_value[0] + "\"")
                    where_list.append(where_query)
    else:
        print "we are working on !!! "
    print "select : " + select
    print "equality : " + equality
    # print "max min : " + max_min
    final_where = ""
    for i in range(0,len(where_list)):
        final_where += where_list[i] + " "
        if i != len(where_list) -1:
            final_where += "AND "
    final_query = query_template.format(select=select, expression=final_where)
    print final_query


if __name__ == "__main__":
    send()
