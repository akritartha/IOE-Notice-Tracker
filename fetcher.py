import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://pcampus.edu.np/category/student-activity/"

def fetch_notices():
    response = requests.get(URL, timeout=15, verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    notices = []

    for article in soup.select("article.post"):
        link = article.select_one("h2.entry-title a")
        date = article.select_one("time.entry-date")
        notices.append({
            "title": link.get_text(strip=True),
            "url": link["href"],
            "date": date["datetime"]
        })
    return notices

if __name__ == "__main__":
    for n in fetch_notices():
        print(n["title"], n["date"])