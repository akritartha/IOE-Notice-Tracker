import sqlite3

def init_db(path="notices.db"):
    conn=sqlite3.connect(path)
    cursor=conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notices(
        id INTEGER PRIMARY KEY AUTO INCREMENT,
        title TEXT NOT NULL,
        )""")