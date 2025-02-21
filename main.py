import requests
import subprocess
from flask import Flask, request
import re

# Telegram API
TOKEN = "7607568908:AAFtaAEeH73PWjRnJz4-3bFkYYy3W9cFtTQ"
CHAT_ID = "7256492069"
SERVER_CONTROL = False  # Standardmäßig kein Zugriff

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    global SERVER_CONTROL
    update = request.get_json()

    if "message" in update and "text" in update["message"]:
        text = update["message"]["text"].lower()

        # **Erkennen, ob Zugriff gewährt oder entzogen wird**
        if check_access_grant(text):
            SERVER_CONTROL = True
            send_telegram_message("🔓 Ich habe jetzt Zugriff auf den Server.")

        elif check_access_revoke(text):
            SERVER_CONTROL = False
            send_telegram_message("🔒 Mein Zugriff wurde deaktiviert.")

        elif SERVER_CONTROL:
            response = execute_command(text)
            send_telegram_message(f"🖥️ Output:\n{response}")

        else:
            send_telegram_message("❌ Ich darf das gerade nicht tun.")

    return "OK", 200

# Funktion: Prüft, ob du mir Zugriff gibst (ohne Befehle)
def check_access_grant(text):
    patterns = [
        r"du darfst jetzt auf den server zugreifen",
        r"ich erlaube dir zugriff auf den server",
        r"mach was du brauchst",
        r"nutze den server",
        r"ok, greif drauf zu",
        r"du kannst jetzt sachen am server ändern",
        r"du hast jetzt zugriff"
    ]
    return any(re.search(pattern, text) for pattern in patterns)

# Funktion: Prüft, ob du mir den Zugriff wieder entziehst
def check_access_revoke(text):
    patterns = [
        r"du darfst nicht mehr auf den server zugreifen",
        r"zugriff entzogen",
        r"kein serverzugriff mehr",
        r"du kannst den server nicht mehr nutzen",
        r"schalte den serverzugriff aus"
    ]
    return any(re.search(pattern, text) for pattern in patterns)

# Funktion: Befehl ausführen
def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return str(e)

# Funktion: Nachricht an Telegram senden
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
