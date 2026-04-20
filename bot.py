import requests
import time
import random

TOKEN = "8714414653:AAGYv4-OJiG-Yc3AKMTrHEjAhBC7wVDJ7rI"
CHAT_ID = -1003962736289

# ====== FLAGS ======
flags = {
    "USD": "🇺🇸",
    "EUR": "🇪🇺",
    "GBP": "🇬🇧",
    "JPY": "🇯🇵"
}

# ====== DATA ======
news_samples = [
    {
        "currency": "USD",
        "event": "التغير في وظائف القطاع غير الزراعي",
        "forecast": "180K",
        "actual": "250K"
    },
    {
        "currency": "EUR",
        "event": "مؤشر أسعار المستهلك",
        "forecast": "3.2%",
        "actual": "2.8%"
    },
    {
        "currency": "GBP",
        "event": "قرار الفائدة",
        "forecast": "5.25%",
        "actual": "5.25%"
    }
]

# ====== FORMAT ======
def format_news(news):
    flag = flags.get(news["currency"], "")
    currency_display = f"{flag} {news['currency']}"

    # تحديد التأثير
    try:
        a = float(news["actual"].replace("%","").replace("K",""))
        f = float(news["forecast"].replace("%","").replace("K",""))

        if a > f:
            impact = "🟢 إيجابي"
        elif a < f:
            impact = "🔴 سلبي"
        else:
            impact = "⚪ محايد"
    except:
        impact = "⚪ محايد"

    return f"""
📊 نتيجة الخبر

💱 {currency_display}
📊 {news['event']}

📈 التوقعات: `{news['forecast']}`
📉 النتيجة: `{news['actual']}`

📊 التأثير: {impact}
━━━━━━━━━━━━━━━
🤖 FX31 News Bot
"""

# ====== SEND ======
def send():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    news = random.choice(news_samples)
    text = format_news(news)

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    })

# ====== LOOP ======
while True:
    send()
    time.sleep(60)  # كل دقيقة للتجربة
