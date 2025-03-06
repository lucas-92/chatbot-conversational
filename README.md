# chatbot-conversational

Criando um Chatbot no Dialogflow e Integrando com o Telegram (Publicação no Render)

Este guia detalhado explica como criar um chatbot no Dialogflow, integrá-lo ao Telegram e publicá-lo no Render.

## 1. Criar um Projeto no Google Cloud

### Criando o agente no Dialogflow

1. Acesse Dialogflow ES.
2. Clique em "Go to Console" e faça login.
3. Clique em "Create Agent" e preencha:
   - Nome do agente: MeuChatbot
   - Idioma: Português (pt-br)
4. Selecione um projeto do Google Cloud ou crie um novo.
5. Clique em "Create".

🔗 [Documentação: Criando agentes no Dialogflow](https://cloud.google.com/dialogflow/es/docs/agents-overview)

## 2. Criar Intenções e Respostas

1. No menu "Intents", clique em "Create Intent".
2. Nomeie como `saudacao`.
3. Em "Training Phrases", adicione:
   - "Oi"
   - "Olá, tudo bem?"
4. Em "Responses", adicione respostas personalizadas.
5. Salve.

🔗 [Documentação: Criando Intenções](https://cloud.google.com/dialogflow/es/docs/intents-overview)

## 3. Criar um Bot no Telegram

### Criando o bot no BotFather

1. No Telegram, pesquise `@BotFather`.
2. Envie `/newbot`.
3. Defina um nome e um username terminando em `bot`.
4. O BotFather fornecerá um TOKEN. Guarde esse dado.

🔗 [Documentação: Criando bots no Telegram](https://core.telegram.org/bots#botfather)

## 4. Criar o Webhook em Python

### Instalando dependências

```bash
pip install flask requests python-telegram-bot
```

### Criando `bot.py`

```python
from flask import Flask, request
import requests
import telegram

TOKEN = "SEU_TELEGRAM_BOT_TOKEN"
DIALOGFLOW_PROJECT_ID = "SEU_DIALOGFLOW_PROJECT_ID"
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
```

### Configurando o Webhook no Telegram

1. Rode o servidor localmente:

   ```bash
   python bot.py
   ```

2. Instale o ngrok, se ainda não tiver:

   ```bash
   pip install pyngrok
   ```

3. Crie um túnel com ngrok:

   ```bash
   ngrok http 5000
   ```

4. Copie a URL gerada pelo ngrok e configure o Webhook:

   ```bash
   curl -X POST "https://api.telegram.org/botSEU_TELEGRAM_BOT_TOKEN/setWebhook?url=https://xxxxxxxx.ngrok.io/SEU_TELEGRAM_BOT_TOKEN"
   ```

🔗 [Documentação: Webhook do Telegram](https://core.telegram.org/bots/api#setwebhook)

## 5. Publicar no Render

1. Faça login em [Render](https://render.com).
2. Clique em "New Web Service".
3. Conecte seu repositório GitHub com o código do bot.
4. Configure os detalhes do serviço:
   - Nome do serviço: MeuChatbot
   - Runtime: Python
   - Região: Escolha a mais próxima do seu público
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
   - Environment Variables: Adicione o TOKEN e DIALOGFLOW_PROJECT_ID
5. Clique em "Deploy" e aguarde a implantação.
6. Após a publicação, copie a URL do Render e configure o Webhook no Telegram:

   ```bash
   curl -X POST "https://api.telegram.org/botSEU_TELEGRAM_BOT_TOKEN/setWebhook?url=https://seu-app-no-render.onrender.com/SEU_TELEGRAM_BOT_TOKEN"
   ```

🔗 [Documentação: Deploy no Render](https://render.com/docs)

## 6. Testando o Bot

1. Abra o Telegram.
2. Envie uma mensagem ao bot e veja se responde corretamente.

🎉 Agora seu chatbot está rodando no Telegram via Dialogflow e hospedado no Render!
