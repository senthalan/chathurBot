import mysql.connector
from witAI import load_entity, load_intent


cnx = mysql.connector.connect(host="localhost", user="root", passwd="root", db="Catalog")
tableName = "electronics"


def init():
    cursor = cnx.cursor(buffered=True)
    cursor.execute("SHOW columns FROM " + tableName)
    columns = []
    for column in cursor.fetchall():
        load_data(column)
        columns.append(column[0])
        load_intent(columns)



def load_data(column):
    print "column : " + column[0]
    if "int" in column[1]:
        print "int"
    if "double" in column[1]:
        print "double"

    else:
        cursor = cnx.cursor(buffered=True)
        cursor.execute("SELECT " + column[0] + " FROM " + tableName)
        values = []
        for data in cursor.fetchall():
            if type(data[0]) == unicode:
                temp = {'value': data[0], 'expressions': [data[0], data[0].upper(), data[0].lower(), "\"" + data[0] + "\""]}
                if temp not in values:
                    values.append(temp)
        if len(values) > 0:
            print "upload it"
            load_entity(column[0], values)
