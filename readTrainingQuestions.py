import os

ques = []
query = []

def read_file():
    #user enter the path of the file which contains question and answers
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    path = 'testing_files/test'
    abs_file_path = os.path.join(script_dir, path)
    # Open this file.
    f = open(abs_file_path, "r")
    i = 0


    # Loop over each line in the file.
    for line in f.readlines():

        # Strip the line to remove whitespace.
        line = line.strip()
        i += 1

        if i == 1:
            ques.append(line)
        elif i == 2:
            query.append(line)
        else:
            i = 0


def get_question():
    return ques

def get_query():
    return query