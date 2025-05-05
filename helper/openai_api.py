import os
import requests

API_KEY = os.getenv("OPENAI_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def chat_complition(prompt: str) -> dict:
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://openrouter.ai",  # Recomendado
            "X-Title": "whatsapp-assistente"
        }

        data = {
            "model": "openchat/openchat-3.5",  # Gratuito e rápido
            "messages": [
                {"role": "system", "content": "Você é um assistente pessoal de tarefas."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(API_URL, headers=headers, json=data)
        result = response.json()

        return {
            "status": 1,
            "response": result['choices'][0]['message']['content']
        }

    except Exception as e:
        print(f"[ERRO OpenRouter]: {e}")
        return {"status": 0, "error": str(e)}
