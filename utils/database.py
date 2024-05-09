import sqlite3
from config import DATABASE_PATH

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            age INTEGER,
            gender TEXT,
            case_id TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def insert_patient_details(first_name, last_name, age, gender, case_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO patients (first_name, last_name, age, gender, case_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (first_name, last_name, age, gender, case_id))
    conn.commit()
    conn.close()

def query_patient_details(case_id):
    conn = get_db_connection()
    c = conn.cursor()
    return c.execute('SELECT * FROM patients WHERE case_id = ?', (case_id,)).fetchone()
