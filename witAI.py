import json

import requests as requests


def loadEntity(entity, values):
    url = 'https://api.wit.ai/entities?v=20160526'
    headers = {'Authorization': 'Bearer FW7VWV3J2G5K2XKSW2ISXJQNSSOQAUWQ', 'Content-Type' : 'application/json'}
    payload = { 'id': entity,
                'values': values}

    r = requests.post(url, data=json.dumps(payload), headers=headers)
    if r.status_code == 200:
        print "entity uploaded successfully " + entity
    else:
        print "something went wrong when uploading " + entity + ": error code " + str(r.status_code)
        print r.content
