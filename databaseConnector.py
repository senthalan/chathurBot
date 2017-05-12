import mysql.connector

cnx = mysql.connector.connect(host="localhost", user="root", passwd="mathu", db="Catalog")


def run_query(query):
    cursor = cnx.cursor(buffered=True)
    cursor.execute(query)
    answers = cursor.fetchall()
    cursor.close()
    return answers
