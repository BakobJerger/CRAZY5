import os
import requests
from flask import Flask, request

# OpenAI API Key aus Umgebungsvariablen
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Telegram Bot Token & Chat ID
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Flask Webserver
app = Flask(__name__)

# OpenAI API-Funktion
def chat_with_openai(user_message):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

# Telegram Nachrichten senden
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

# Webhook für Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    if "message" in update and "text" in update["message"]:
        user_text = update["message"]["text"]
        ai_response = chat_with_openai(user_text)
        send_telegram_message(ai_response)
    return "OK", 200

# Server starten
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
