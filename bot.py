import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from flask import Flask
from threading import Thread
import os
# ================== CONFIG ==================
TOKEN = "8714414653:AAGYv4-OJiG-Yc3AKMTrHEjAhBC7wVDJ7rI"
CHAT_ID = -1003962736289

sent_news = set()

# ================== FLASK (KEEP ALIVE) ==================
app = Flask('')

@app.route('/')
def home():
    return "Bot is running ✅"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# ================== TELEGRAM ==================
def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    })

# ================== GET NEWS ==================
def get_news():
    url = "https://www.forexfactory.com/calendar"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    news_list = []
    rows = soup.select("tr.calendar__row")

    for row in rows:
        impact = row.select_one(".impact")

        if impact and "High" in impact.get("title", ""):
            currency = row.select_one(".calendar__currency")
            event = row.select_one(".calendar__event")
            forecast = row.select_one(".calendar__forecast")

            currency = currency.text.strip() if currency else ""
            event = event.text.strip() if event else ""
            forecast = forecast.text.strip() if forecast else ""

            unique_id = f"{currency}-{event}-{forecast}"

            if unique_id not in sent_news:
                sent_news.add(unique_id)

                news_text = f"""
🚨 *HIGH IMPACT NEWS* 🚨

💱 *Currency:* `{currency}`
📊 *Event:* {event}
📈 *Forecast:* `{forecast}`

━━━━━━━━━━━━━━━
🤖 *FX31 News Bot*
"""
                news_list.append(news_text)

    return news_list

# ================== MAIN LOOP ==================
def run_bot():
    while True:
        print("Bot running...")

        news = get_news()

        for item in news:
            send_message(item)
            time.sleep(5)  # anti spam

        time.sleep(600)  # كل 10 دقائق

# ================== START ==================
keep_alive()
run_bot()
