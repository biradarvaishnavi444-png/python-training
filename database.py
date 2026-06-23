import sqlite3
from flask import Flask,render_template,request,redirect,flash
app = Flask(__name__)
app.secret_key ='Linkiwi2026'   # Necessary for flash messages

#2 function
def get_db_():
    """Database connection"""
    conn = sqlite3.connect('Database.db')
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn

def init_db():
    """ Create table """
    conn = get_db_()
    # Create users table if it doesn't exist
    conn.execute("""
    CREATE TABLE IF NOT EXISTS visitors(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
        visitor_name TEXT NOT NULL,
        student_name TEXT NOT NULL,
        room_no TEXT NOT NULL,
        purpose TEXT NOT NULL
   """ )
    conn.close()

    if __name__ == '__main__':
        init_db()  # Initialize the database 