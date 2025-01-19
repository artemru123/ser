import sqlite3
import datetime


def get_db_connection():

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn
def codes():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM code WHERE data < ?", (datetime.datetime.now(),));  cursor.execute("DELETE FROM session WHERE exp < ?",(datetime.datetime.now(),))
    conn.commit()




