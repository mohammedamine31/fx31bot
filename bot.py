import requests
from flask import Flask
from threading import Thread
import time
import os
# ================== CONFIG ==================
TOKEN = "8714414653:AAGYv4-OJiG-Yc3AKMTrHEjAhBC7wVDJ7rI"
CHAT_ID = -1003962736289

# ====== FLASK ======
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

# ====== TELEGRAM TEST ======
def send_test():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    text = """
🚀 TEST MESSAGE

✅ Bot is working
✅ Render is running
✅ Flask is active

🤖 FX31 Bot
"""

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

# ====== MAIN ======
keep_alive()

while True:
    print("Bot running...")

    send_test()

    time.sleep(60)  # كل دقيقة (باش تشوف بسرعة)
