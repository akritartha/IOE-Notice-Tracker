import requests
from bs4 import BeautifulSoup

url="https://pcampus.edu.np/category/student-activity/"
response=requests.get(url,timeout=15)
print(response.status_code)

soup=BeautifulSoup(response.text,"html.parser")

for article in soup.select("article.post"):
    link=article.select_one("h2.entry-title a")
    date=article.select_one("time.entry-date")
    print(link.get_text(strip=True))
    print(link["href"])
    print(date["datetime"])
    print("---")