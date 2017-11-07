import os

ques = []
intent =[]
entities=[]
query = []
answers=[]

def read_file():
    #user enter the path of the file which contains question and answers

    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    path = 'testing_files/test'
    abs_file_path = os.path.join(script_dir, path)
    # Open this file.
    f = open(abs_file_path, "r")
    i = 0
    j=0
    # Loop over each line in the file.
    for line in f.readlines():

        # Strip the line to remove whitespace.
        line = line.strip()

        i += 1

        if i == 1:
            ques.append(line)
        elif i == 2:
            intent.append(line)
        elif i==3:
            entities.append(line)
        elif i == 4:
            query.append(line)
        elif i==5:
            answers.append(line.lower().split(','))
        else:
            i = 0

def get_question():
    return ques

def get_intent():
    return intent

def get_query():
    return query

def get_entities():
    return entities

def get_answers():
    return answers

def generateEntityList(entity):
    entityList = {}
    entityTypeList=entity.split(';')

    for entityType in entityTypeList:
        value=[]
        entityKeyValuePair=str(entityType).split('-')

        key=entityKeyValuePair[0]

        for x in str(entityKeyValuePair[1]).split(','):
            value.append(x.lower())
        # value=str(entityKeyValuePair[1]).split(',')

        entityList[key.lower()]=value


    return entityList