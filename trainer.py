import mysql.connector
from witAI import loadEntity

cnx = mysql.connector.connect(host="localhost",  # your host, usually localhost
                                  user="root",  # your username
                                  passwd="root",  # your password
                                  db="Book")  # name of the data base
tableName = "BX_Books"

def init():
    cursor = cnx.cursor(buffered=True)
    cursor.execute("SHOW columns FROM " + tableName)
    for column in cursor.fetchall():
        loadData(column)


def loadData(column):
    print "column : " + column[0]
    if "int" in column[1]:
        print "int"
        loadEntity("wit$datetime", [])
    # else:
    #     cursor = cnx.cursor(buffered=True)
    #     cursor.execute("SELECT " + column[0] + " FROM " + tableName)
    #     values = []
    #     for data in cursor.fetchall():
    #         if type(data[0]) == unicode:
    #             values.append({'value': data[0]})
    #     if len(values) > 0:
    #         loadEntity(column[0], values)

