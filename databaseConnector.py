import mysql.connector

cnx = mysql.connector.connect(host="localhost", user="root", passwd="root", db="Catalog")


def run_query(query):
    cursor = cnx.cursor(buffered=True)
    try:
        cursor.execute(query)
        answers = cursor.fetchall()
        cursor.close()
    except mysql.connector.Error as err:
        answers = ''
    finally:
        cursor.close()
    return answers
