import requests
import time
import os
import subprocess
from flask import Flask, request

# Deine Server-URL (wird später durch die Render-URL ersetzt)
SERVER_URL = "https://crazy5bot.onrender.com"

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
        if text == "/status":
            send_telegram_message("✅ Server läuft und empfängt Nachrichten!")
        elif text.startswith("/analyse "):
            symbol = text.split(" ")[1].upper() + "/USDT"
            get_market_data(symbol)
        else:
            send_telegram_message(f"Unbekannter Befehl: {text}")
    return "", 200

# Funktion zum Senden einer Telegram-Nachricht
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, data=data)

# Funktion zum Überprüfen des Server-Status
def check_server():
    try:
        response = requests.get(SERVER_URL, timeout=10)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False

# Funktion zum Neustarten des Servers
def restart_server():
    send_telegram_message("⚠️ Server ist offline! Versuche, ihn neu zu starten...")
    try:
        subprocess.run(["curl", "-X", "POST", "https://api.render.com/v1/services/SERVICE_ID/deploys",
                        "-H", "Authorization: Bearer RENDER_API_KEY"], check=True)
        send_telegram_message("✅ Server erfolgreich neu gestartet!")
    except Exception as e:
        send_telegram_message(f"❌ Fehler beim Neustart: {str(e)}")

# Server überwachen
def monitor_server():
    while True:
        if not check_server():
            restart_server()
        time.sleep(300)

if __name__ == "__main__":
    send_telegram_message("🔄 Server-Überwachungsprozess gestartet!")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
