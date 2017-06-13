def generate_answer(answers, intent):
    print answers
    if len(answers) == 1:
        print intent + " is "+ str(answers[0][0])
    else:
        print "no answer"
    # print "still working"