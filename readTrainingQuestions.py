def read_training_questions(intent):
    questions = []
    return questions

ques = []
intent =[]
entity =[]
query = []

def read_file():
    #user enter the path of the file which contains question and answers
    path = raw_input("Enter file path:")
    # Open this file.
    f = open(path, "r")#Eg path : "/home/mathuriga/CSE-ENG/test"

    i = 0

    # Loop over each line in the file.
    for line in f.readlines():

        # Strip the line to remove whitespace.
        line = line.strip()

        i += 1

        if i == 1:
            ques.append(line)
        elif i == 2:
            intent.append(line)
        elif i == 3:
            query.append(line)
        else:
            i = 0


def get_question():
    return ques

def get_intent():
    return intent

def get_query():
    return query