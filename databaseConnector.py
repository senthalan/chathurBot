import mysql.connector
import unicodedata
cnx = mysql.connector.connect(host="localhost", user="root", passwd="root", db="Catalog")
cnx.text_factory = str


def run_query(query):
    answers = []
    try :
        cursor = cnx.cursor(buffered=True)
        cursor.execute(query)
        result = [[str(item) for item in results] for results in cursor.fetchall()]
        for val in result:
           answers.append(''.join(val).lower())
        cursor.close()

        return answers
    except mysql.connector.errors.ProgrammingError:
        return answers