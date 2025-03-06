from flask import Flask, request
import requests
import telegram
from dotenv import load_dotenv
import os
import google.auth
from google.auth.transport.requests import Request
from google.oauth2 import service_account

load_dotenv()  # Carregar variáveis do .env

# Variáveis de ambiente
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DIALOGFLOW_PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")
DIALOGFLOW_LANGUAGE = "pt-br"
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Autenticação do Google
credentials = service_account.Credentials.from_service_account_file(GOOGLE_CREDENTIALS_PATH)
scoped_credentials = credentials.with_scopes(["https://www.googleapis.com/auth/cloud-platform"])

app = Flask(__name__)
bot = telegram.Bot(token=TOKEN)

def dialogflow_response(text, session_id):
    """Envia uma mensagem para o Dialogflow e retorna a resposta."""

    url = f"https://dialogflow.googleapis.com/v2/projects/{DIALOGFLOW_PROJECT_ID}/agent/sessions/{session_id}:detectIntent"
    
    # Atualizar token de autenticação
    scoped_credentials.refresh(Request())
    token = scoped_credentials.token

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "queryInput": {
            "text": {
                "text": text,
                "languageCode": DIALOGFLOW_LANGUAGE
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json().get("queryResult", {}).get("fulfillmentText", "Erro ao obter resposta do Dialogflow.")
    else:
        return f"Erro na requisição: {response.status_code} - {response.text}"

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

