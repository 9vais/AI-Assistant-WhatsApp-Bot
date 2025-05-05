from flask import Flask, request, jsonify
from helper.openai_api import chat_complition
from helper.twilio_api import send_message
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(
        {
            'status': 'OK',
            'wehook_url': 'BASEURL/twilio/receiveMessage',
            'message': 'The webhook is ready.',
            'video_url': 'https://youtu.be/y9NRLnPXsb0'
        }
    )

@app.route('/twilio/receiveMessage', methods=['POST'])
def receiveMessage():
    try:
        message = request.form['Body']
        sender_id = request.form['From']

        print(f"Received message: {message} from {sender_id}")

        result = {}
        try:
            result = chat_complition(message)
            print(f"[DEBUG] Resultado do chat_complition: {result}")
        except Exception as e:
            print(f"[ERRO] Falha ao chamar chat_complition: {e}")

        resp = MessagingResponse()

        # Inicializa a variável de resposta
        resposta = ""

        if result.get("status") == 1:
            raw = result.get("response")

            # Se for uma string
            if isinstance(raw, str):
                resposta = raw

            # Se for dicionário, tenta extrair texto com segurança
            elif isinstance(raw, dict) and 'message' in raw:
                resposta = raw['message'].get('content', '')

            # Se for lista, tenta extrair o primeiro item
            elif isinstance(raw, list) and len(raw) > 0:
                first = raw[0]
                if isinstance(first, dict) and 'message' in first:
                    resposta = first['message'].get('content', '')

        elif result.get("error"):
            resposta = f"Erro da IA: {result['error']}"
        else:
            resposta = "Não entendi sua solicitação."

        # Garante que sempre tenha algo para responder
        if not resposta:
            resposta = "A IA não conseguiu gerar uma resposta."

        resp.message(resposta)
        return str(resp)

    except Exception as e:
        print(f"Error: {e}")
        resp = MessagingResponse()
        resp.message("Erro interno no servidor.")
        return str(resp)
