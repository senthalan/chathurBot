def generate_answer(answers, response):
    print answers
    intent = ''
    for key in response:
        if key == 'intent':
            intent = ((response[key])[0])['value']
    if len(answers) == 1:
        print intent + " is "+ str(answers[0][0])


    print "still working"