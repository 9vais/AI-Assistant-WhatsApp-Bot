# Import the required modules
from flask import Flask, request, jsonify
from helper.openai_api import chat_complition
from helper.twilio_api import send_message
from twilio.twiml.messaging_response import MessagingResponse  # <-- IMPORTANTE

# Create a Flask application
app = Flask(__name__)

# Define the route for the home page
@app.route('/')
def home():
    # Return a JSON response with the status, webhook URL, message, and video URL
    return jsonify(
        {
            'status': 'OK',
            'wehook_url': 'BASEURL/twilio/receiveMessage',
            'message': 'The webhook is ready.',
            'video_url': 'https://youtu.be/y9NRLnPXsb0'
        }
    )

# Define the route for receiving messages from Twilio
@app.route('/twilio/receiveMessage', methods=['POST'])
def receiveMessage():
    try:
        # Extract incoming parameters from Twilio
        message = request.form['Body']
        sender_id = request.form['From']

        # Print the received message and sender id
        print(f"Received message: {message} from {sender_id}")  

        result = {}
        try:
            result = chat_complition(message)
            print(f"[DEBUG] Resultado do chat_complition: {result}")
        except Exception as e:
            print(f"[ERRO] Falha ao chamar chat_complition: {e}")

        # Build Twilio response
        resp = MessagingResponse()

        # Verifica e interpreta corretamente a resposta
        resposta = ""
        if result.get("status") == 1 and isinstance(result.get("response"), str):
            resposta = result["response"]
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
