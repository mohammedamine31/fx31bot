import requests
import time
import random
from datetime import datetime

TOKEN = "8714414653:AAGYv4-OJiG-Yc3AKMTrHEjAhBC7wVDJ7rI"
CHAT_ID = -1003962736289

news_samples = [
    {
        "currency": "USD 🇺🇸",
        "event": "Non-Farm Employment Change",
        "forecast": "180K",
        "previous": "150K"
    },
    {
        "currency": "EUR 🇪🇺",
        "event": "ECB Interest Rate Decision",
        "forecast": "4.25%",
        "previous": "4.00%"
    },
    {
        "currency": "GBP 🇬🇧",
        "event": "CPI y/y",
        "forecast": "3.1%",
        "previous": "3.4%"
    }
]

def format_news(news):
    time_now = datetime.now().strftime("%H:%M")

    text = f"""
🚨 *HIGH IMPACT NEWS* 🚨

━━━━━━━━━━━━━━━━━━━
💱 *Currency | العملة:* {news['currency']}

📊 *Event | الخبر:*
{news['event']}

📈 *Forecast | التوقع:* `{news['forecast']}`
📉 *Previous | السابق:* `{news['previous']}`

⏰ *Time | الوقت:* {time_now}
⏳ *Status | الحالة:* Coming Soon

━━━━━━━━━━━━━━━━━━━
🟡 *Impact:* HIGH
⚡ *Source:* Forex Factory

🤖 *FX31 News Bot*
"""
    return text

def send_news():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    news = random.choice(news_samples)
    text = format_news(news)

    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }

    requests.post(url, data=data)

while True:
    send_news()
    time.sleep(60)  # للتجربة فقط