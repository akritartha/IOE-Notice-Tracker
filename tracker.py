from fetcher import fetch_notices
from db import init_db, add_to_db
from notifier import send_notice
import requests

def main():
    conn=init_db("notices.db")
    try:
        notices= fetch_notices()
    except requests.RequestException as e:
        print(f"Fetch failed: {e}")
        return
    for n in reversed(notices):
        is_new=add_to_db(conn,n["title"],n["url"],n["date"])
        if is_new:
            send_notice(n)

if __name__=="__main__":
    main()