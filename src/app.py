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

        # Get response from OpenAI
        result = chat_complition(message)

        # Print the response from OpenAI
        print(f"OpenAI response: {result}")  

        # Build Twilio response
        resp = MessagingResponse()
        if result['status'] == 1:
            resp.message(result['response'])
        else:
            resp.message("Houve um problema ao processar sua solicitação.")
        return str(resp)

    except Exception as e:
        print(f"Error: {e}")  
        resp = MessagingResponse()
        resp.message("Ocorreu um erro no servidor ao tentar responder.")
        return str(resp)
