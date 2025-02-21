import requests
import time
import os
import subprocess
from flask import Flask, request

# Deine Server-URL (wird später durch die Render-URL ersetzt)
SERVER_URL = "https://crazy5.onrender.com"

# Dein Telegram Bot Token
TOKEN = "7607568908:AAFtaAEeH73PWjRnJz4-3bFkYYy3W9cFtTQ"
CHAT_ID = "7256492069"

# Flask Webserver für Webhook
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    
    if "message" in update and "text" in update["message"]:
        text = update["message"]["text"].lower()
        print(f"Empfangene Nachricht: {text}")  # Debugging: Zeigt, was empfangen wurde
        
        if text == "/status":
            send_telegram_message("✅ Server läuft und empfängt Nachrichten!")
        
        elif text.startswith("analyse "):
            symbol = text.split(" ")[1].upper() + "/USDT"
            send_telegram_message(f"📊 Starte Analyse für {symbol}...")
            get_market_data(symbol)
        
        else:
            send_telegram_message(f"❌ Unbekannter Befehl: {text}")

    return "", 200

# Funktion zum Senden einer Telegram-Nachricht
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

# Funktion zur Marktanalyse (Platzhalter)
def get_market_data(symbol):
    send_telegram_message(f"📈 {symbol} Analyse läuft... (noch nicht implementiert)")

# Starte den Flask Webserver
if __name__ == '__main__':
    print("🔥 Server gestartet und bereit für Anfragen...")
    send_telegram_message("✅ CRAZY5 ist jetzt online und kann Befehle empfangen!")
    app.run(host='0.0.0.0', port=10000)
