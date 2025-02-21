import requests
import time
import os
import subprocess
from flask import Flask, request

# Deine Server-URL (Render)
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
        text = update["message"]["text"]
        antwort = handle_message(text)
        send_telegram_message(antwort)
    return "OK", 200

# Funktion zum Verarbeiten der Nachricht
def handle_message(text):
    if text.lower() == "/status":
        return "✅ Server läuft und empfängt Nachrichten!"
    else:
        return f"🤖 {text}"  # Hier passiert die "Live-Antwort"

# Funktion zum Senden einer Telegram-Nachricht
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

# Starte Flask-Server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
