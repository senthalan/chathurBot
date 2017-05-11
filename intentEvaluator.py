

def evaluate_intent(response,actualIntent):
    key='intent'
    intent = ((response[key])[0])['value']
    if (intent==actualIntent):
        print "extracted intent + " + ((response['intent'])[0])['value']
        return 1
    else:
        return 0

