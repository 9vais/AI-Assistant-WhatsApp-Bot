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

        # Trata a resposta corretamente
        resposta = ""

        if result.get("status") == 1:
            raw = result.get("response")

            # Se a resposta já for texto
            if isinstance(raw, str):
                resposta = raw

            # Se for objeto ou lista, tenta extrair o texto
            elif isinstance(raw, list) or isinstance(raw, dict):
                try:
                    resposta = raw[0]['message']['content']
                except:
                    resposta = "Erro ao interpretar a resposta da IA."
        elif result.get("error"):
            resposta = f"Erro da IA: {result['error']}"
        else:
            resposta = "Não entendi sua solicitação."

        resp.message(resposta)
        return str(resp)

    except Exception as e:
        print(f"Error: {e}")
        resp = MessagingResponse()
        resp.message("Ocorreu um erro no servidor ao tentar responder.")
        return str(resp)
