from flask import Flask, request
import requests
import telegram
from dotenv import load_dotenv
import os

load_dotenv()  # Carregar variáveis do .env

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DIALOGFLOW_PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")
DIALOGFLOW_LANGUAGE = "pt-br"

app = Flask(__name__)
bot = telegram.Bot(token=TOKEN)

def dialogflow_response(text, session_id):
    url = f"https://dialogflow.cloud.google.com/v2/projects/{DIALOGFLOW_PROJECT_ID}/agent/sessions/{session_id}:detectIntent"
    headers = {"Content-Type": "application/json"}
    data = {"queryInput": {"text": {"text": text, "languageCode": DIALOGFLOW_LANGUAGE}}}
    response = requests.post(url, headers=headers, json=data)
    return response.json()["queryResult"]["fulfillmentText"]

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]
        resposta = dialogflow_response(text, chat_id)
        bot.sendMessage(chat_id=chat_id, text=resposta)
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

