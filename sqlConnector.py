import mysql.connector


def sqlconnector(index):
    cnx = mysql.connector.connect(host="localhost",  # your host, usually localhost
                                  user="root",  # your username
                                  passwd="root",  # your password
                                  db="sample")  # name of the data base
    cursor = cnx.cursor()

    query = "SELECT name FROM student where no = %(no)s"

    cursor.execute(query, {'no': index})

    for (name) in cursor:
        fname = name

    cursor.close()
    cnx.close()

    return fname[0]

def sqlQuery(query):
    cnx = mysql.connector.connect(host="localhost",  # your host, usually localhost
                                  user="root",  # your username
                                  passwd="root",  # your password
                                  db="sample")  # name of the data base
    cursor = cnx.cursor()
    cursor.execute(query)
    for (name) in cursor:
        fname = name
    cursor.close()
    cnx.close()
    return fname[0]
