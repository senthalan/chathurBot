def read_training_questions(intent):
    questions = []
    return questions


def get_questions():
    #user enter the path of the file which contains question and answers
    path = raw_input("Enter file path:")
    # Open this file.
    f = open(path, "r")#Eg path : "/home/mathuriga/CSE-ENG/test"

    i = 0
    ques = []
    query = []

    # Loop over each line in the file.
    for line in f.readlines():

        # Strip the line to remove whitespace.
        line = line.strip()
        i += 1

        # Display the line.
        print(line, i)

        if i == 1:
            ques.append(line)
        elif i == 2:
            query.append(line)
        else:
            i = 0

    print('list of questions')
    for j in range(len(ques)):
        print (ques[j])

    print('list of queries')
    for j in range(len(query)):
        print (query[j])