#Evaluate intent of question

def evaluate_intent(intent,actualIntent):

    if intent==actualIntent:
        # print "extracted intent + " + ((response['intent'])[0])['value']
        return 1
    else:
        return 0