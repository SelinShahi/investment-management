import mysql.connector
from contextlib import contextmanager

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",       
        password="",   
        database="investment_manager"
    )

@contextmanager
def get_cursor():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        yield conn, cursor
        conn.commit()
    finally:
        cursor.close()
        conn.close()

