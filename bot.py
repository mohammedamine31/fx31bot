import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta

TOKEN = "8714414653:AAGYv4-OJiG-Yc3AKMTrHEjAhBC7wVDJ7rI"
CHAT_ID = -1003962736289

sent_events = set()

def get_calendar():
    url = "https://www.forexfactory.com/calendar"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    events = []
    rows = soup.select("tr.calendar__row")

    for row in rows:
        impact = row.select_one(".impact")

        if impact and "High" in impact.get("title", ""):
            time_el = row.select_one(".calendar__time")
            currency = row.select_one(".calendar__currency")
            event = row.select_one(".calendar__event")
            forecast = row.select_one(".calendar__forecast")
            actual = row.select_one(".calendar__actual")

            event_time = time_el.text.strip() if time_el else ""
            currency = currency.text.strip() if currency else ""
            event = event.text.strip() if event else ""
            forecast = forecast.text.strip() if forecast else ""
            actual = actual.text.strip() if actual else ""

            events.append({
                "time": event_time,
                "currency": currency,
                "event": event,
                "forecast": forecast,
                "actual": actual
            })

    return events


def send(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    })


def format_before(e):
    return f"""
🚨 *HIGH IMPACT NEWS* 🚨

💱 *{e['currency']}*
📊 *{e['event']}*

📈 Forecast: `{e['forecast']}`

⏳ *Starts Soon*
━━━━━━━━━━━━━━━
🤖 FX31 News Bot
"""


def format_after(e):
    bias = "⚪ Neutral"

    if e["actual"] and e["forecast"]:
        if e["actual"] > e["forecast"]:
            bias = "🟢 Bullish"
        elif e["actual"] < e["forecast"]:
            bias = "🔴 Bearish"

    return f"""
📊 *NEWS RESULT*

💱 *{e['currency']}*
📊 *{e['event']}*

📈 Forecast: `{e['forecast']}`
📉 Actual: `{e['actual']}`

🎯 Bias: {bias}
━━━━━━━━━━━━━━━
🤖 FX31 News Bot
"""


def run():
    while True:
        events = get_calendar()

        for e in events:
            unique = f"{e['currency']}-{e['event']}-{e['time']}"

            # قبل الخبر
            if unique not in sent_events:
                send(format_before(e))
                sent_events.add(unique)

            # بعد الخبر
            if e["actual"]:
                result_id = unique + "-done"

                if result_id not in sent_events:
                    send(format_after(e))
                    sent_events.add(result_id)

        time.sleep(600)  # كل 10 دقائق


run()
