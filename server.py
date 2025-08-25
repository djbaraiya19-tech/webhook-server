from flask import Flask, request, jsonify
import requests
import logging
import os

app = Flask(__name__)

# 🔐 Security Token for Authorization
SECURE_TOKEN = os.getenv("SECURE_TOKEN")

# 📲 Telegram Bot Credentials from Environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 🛎️ Telegram Notification Function
def notify_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        logging.error(f"Telegram notification failed: {str(e)}")

# 🚨 Webhook Endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    # 🐛 Debug: Log incoming request
    print("Headers:", request.headers)
    print("Raw Body:", request.get_data(as_text=True))
    print("Parsed JSON:", request.get_json(force=True, silent=True))

    token = request.headers.get('Authorization')
    print("🔍 Received Token:", token)
    print("🔐 Expected Token:", SECURE_TOKEN)

    if token != SECURE_TOKEN:
        logging.warning("Unauthorized access attempt")
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        data = request.get_json(force=True)
        if not data:
            raise ValueError("Empty payload")

        logging.info(f"Received alert: {data}")
        notify_telegram(f"🚨 Alert received: {data}")

        return jsonify({'status': 'Success'}), 200

    except Exception as e:
        logging.error(f"Error processing alert: {str(e)}")
        return jsonify({'error': 'Bad request', 'details': str(e)}), 400

# 🚀 Run the Flask Server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)