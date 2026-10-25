import os
import requests

WEBHOOK_URL= os.environ.get("NOTICE_DISCORD_WEBHOOK")

def send_notice(notice):
    if not WEBHOOK_URL:
        print("No discord webhooks set")
        return False

    message=f"📢 **{notice["title"]}**\n**{notice["url"]}**"
    try:
        resp=requests.post(WEBHOOK_URL,json={"content": message},timeout=10)
        resp.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Discord send failed: {e}")
        return False