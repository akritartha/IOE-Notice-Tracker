from fetcher import fetch_notices
from db import init_db, add_to_db

def main():
    conn=init_db("notices.db")
    notices= fetch_notices()

    for n in reversed(notices):
        is_new=add_to_db(conn,n["title"],n["url"],n["date"])
        if is_new:
            print("NEW: ",n["title"])

if __name__=="__main__":
    main()