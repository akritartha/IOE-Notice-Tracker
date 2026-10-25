import sqlite3

def init_db(path="notices.db"):
    conn=sqlite3.connect(path)
    cursor=conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notices(
        id INTEGER PRIMARY KEY AUTO INCREMENT,
        title TEXT NOT NULL,
        url TEXT NOT NULL UNIQUE,
        date_posted TEXT,
        seen_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")
    conn.commit()
    return conn

def add_to_db(conn,title,url, posted_date):
    cur=conn.execute(
        "INSERT INTO notices(title,url,date_posted) VALUES (?,?,?)",
        (title,url,posted_date)
    )
    conn.commit()
    return cur.rowcount==1