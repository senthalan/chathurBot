def generate_answer(answers, intent):
    if answers == '':
        print "error"
        return
    print answers
    if len(answers) == 1:
        print intent + " is "+ str(answers[0][0])
    else:
        print "still working"