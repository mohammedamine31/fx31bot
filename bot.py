import requests
from bs4 import BeautifulSoup
import time
from flask import Flask
from threading import Thread
import os

TOKEN = "8714414653:AAGYv4-OJiG-Yc3AKMTrHEjAhBC7wVDJ7rI"
CHAT_ID = -1003962736289

sent_ids = set()

# ====== FLAGS ======
flags = {
    "USD": "🇺🇸",
    "EUR": "🇪🇺",
    "GBP": "🇬🇧",
    "JPY": "🇯🇵",
    "AUD": "🇦🇺",
    "CAD": "🇨🇦",
    "CHF": "🇨🇭",
    "NZD": "🇳🇿"
}

# ====== FLASK ======
app = Flask('')

@app.route('/')
def home():
    return "Bot is running ✅"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    Thread(target=run_web).start()

# ====== TELEGRAM ======
def send(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    })

# ====== GET NEWS ======
def get_news():
    url = "https://www.forexfactory.com/calendar"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    events = []
    rows = soup.select("tr.calendar__row")

    for row in rows:
        impact = row.select_one(".impact")

        # 🔥 فلترة High Impact فقط
        if impact and "High" in impact.get("title", ""):

            currency = row.select_one(".calendar__currency")
            event = row.select_one(".calendar__event")
            forecast = row.select_one(".calendar__forecast")
            actual = row.select_one(".calendar__actual")

            c = currency.text.strip() if currency else ""
            e = event.text.strip() if event else ""
            f = forecast.text.strip() if forecast else ""
            a = actual.text.strip() if actual else ""

            uid = f"{c}-{e}"

            events.append({
                "id": uid,
                "currency": c,
                "event": e,
                "forecast": f,
                "actual": a
            })

    return events

# ====== FORMAT ======
def format_news(e):
    flag = flags.get(e['currency'], "")
    currency_display = f"{flag} {e['currency']}"

    impact = "⚪ محايد"

    try:
        if e["actual"] and e["forecast"]:
            a = float(e["actual"].replace("%","").replace("K",""))
            f = float(e["forecast"].replace("%","").replace("K",""))

            if a > f:
                impact = "🟢 إيجابي"
            elif a < f:
                impact = "🔴 سلبي"
    except:
        pass

    return f"""
📊 نتيجة الخبر

💱 {currency_display}
📊 {e['event']}

📈 التوقعات: `{e['forecast']}`
📉 النتيجة: `{e['actual']}`

📊 التأثير: {impact}
━━━━━━━━━━━━━━━
🤖 FX31 News Bot
"""

# ====== MAIN ======
def run_bot():
    while True:
        print("Running...")

        events = get_news()

        for e in events:
            if e["actual"] and e["id"] not in sent_ids:
                send(format_news(e))
                sent_ids.add(e["id"])
                time.sleep(5)

        time.sleep(600)  # كل 10 دقائق

# ====== START ======
keep_alive()
def start_bot():
    run_bot()

keep_alive()

from threading import Thread
Thread(target=start_bot).start()

while True:
    time.sleep(60)
