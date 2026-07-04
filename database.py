import os
import sqlite3
from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = 'Linkiwi2026'

#Absoulute path - Always with app.py folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'Database.db')


# Database Connection
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Create Tables
def init_db():

    conn = get_db()

    # Visitors Table
    conn.execute("""
    CREATE TABLE IF NOT EXISTS visitors(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        visitor_name TEXT NOT NULL,
        student_name TEXT NOT NULL,
        room_no TEXT NOT NULL,
        purpose TEXT NOT NULL
    )
    """)

    # Users Table
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)

    try:
        conn.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'visitors'")
    except:
        pass

    conn.commit()
    conn.close()

init_db()  # Initialize the database

if __name__ == "__main__":
    app.run(debug=True)
    