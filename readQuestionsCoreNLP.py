import os

entityTypeList=['model','brand','onlineStore','memory','price','extremum','comparator','rank_for','rank','limit']
ques = []
intent =[]
entities=[]
query = []
answers=[]

def readFileCoreNLP():
    #user enter the path of the file which contains question and answers

    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    # path = 'testing_files/testData'
    path = 'testing_files/testDataNLP'
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
            answers.append(line.split(','))

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
    entityList =[]
    model = []
    brand = []
    onlineStore = []
    number = []
    money = []
    extremum = []
    comparator = []
    order_by = []
    order = []
    limit = []
    completeEntityList = {}

    def get_model():
        return model

    def get_brand():
        return brand

    def get_onlineStore():
        return onlineStore

    def get_number():
        return number

    def get_money():
        return money

    def get_extremum():
        return extremum

    def get_order_by():
        return order_by

    def get_comparator():
        return comparator

    def get_order():
        return order

    def get_limit():
        return limit


    entitiesList=entity.split(';')

    for entityKeyVal in entitiesList:
        value=[]
        entityKeyValuePair=str(entityKeyVal).split('-')
        key=entityKeyValuePair[0]

        if key in entityTypeList:
            if key == "model":
                model.append(entityKeyValuePair[1].split(','))
            elif key == "brand":
                brand.append(entityKeyValuePair[1].split(','))
            elif key == "onlineStore":
                onlineStore.append(entityKeyValuePair[1].split(','))
            elif key == "memory":
                number.append(entityKeyValuePair[1].split(','))
            elif key == "price":
                money.append(entityKeyValuePair[1].split(','))
            elif key == "extremum":
                extremum.append(entityKeyValuePair[1].split(','))
            elif key == "comparator":
                comparator.append(entityKeyValuePair[1].split(','))
            elif key == "rank_for":
                order_by.append(entityKeyValuePair[1].split(','))
            elif key == "rank":
                order.append(entityKeyValuePair[1].split(','))
            elif key == "limit":
                limit.append(entityKeyValuePair[1].split(','))
    for key in entityTypeList:
        if key =="model":
            completeEntityList[key]=get_model()
        if key == "brand":
            completeEntityList[key]=get_brand()
        if key == "onlineStore":
            completeEntityList[key]=get_onlineStore()
        if key == "memory":
            completeEntityList[key]=get_number()
        if key == "price":
            completeEntityList[key]=get_money()
        if key == "extremum":
            completeEntityList[key]=get_extremum()
        if key == "comparator":
            completeEntityList[key]=get_comparator()
        if key == "rank_for":
            completeEntityList[key]=get_order_by()
        if key == "rank":
            completeEntityList[key]=get_order()
        if key == "limit":
            completeEntityList[key]=get_limit()
    return completeEntityList
