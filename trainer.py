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
        # load_entity("wit$datetime", [])
    if "double" in column[1]:
        print "double"
        # load_entity("wit$datetime", [])

    else:
        cursor = cnx.cursor(buffered=True)
        cursor.execute("SELECT " + column[0] + " FROM " + tableName)
        values = []
        for data in cursor.fetchall():
            if type(data[0]) == unicode:
                values.append({'value': data[0]})
        if len(values) > 0:
            load_entity(column[0], values)
