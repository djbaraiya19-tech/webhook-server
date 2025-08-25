from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# 🔐 Security Token for Authorization
SECURE_TOKEN = "darshit123secure"  # Replace with your actual token

# 📲 Telegram Bot Credentials
TELEGRAM_TOKEN = "your_telegram_bot_token"  # Replace with your bot token
CHAT_ID = "your_chat_id"  # Replace with your Telegram chat ID

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
    token = request.headers.get('Authorization')
    if token != SECURE_TOKEN:
        logging.warning("Unauthorized access attempt")
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        data = request.get_json(force=True)
        if not data:
            raise ValueError("Empty payload")

        logging.info(f"Received alert: {data}")
        notify_telegram(f"🚨 Alert received: {data}")

        # Optional: Add trading logic here
        return jsonify({'status': 'Success'}), 200

    except Exception as e:
        logging.error(f"Error processing alert: {str(e)}")
        return jsonify({'error': 'Bad request', 'details': str(e)}), 400

# 🚀 Run the Flask Server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)