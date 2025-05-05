import os
import requests

API_KEY = os.getenv("OPENAI_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def chat_complition(prompt: str) -> dict:
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://openrouter.ai",
            "X-Title": "whatsapp-assistente"
        }

        data = {
            "model": "openchat/openchat-3.5",  # Gratuito e bom
            "messages": [
                {"role": "system", "content": "Você é um assistente pessoal de tarefas. Responda de forma clara."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(API_URL, headers=headers, json=data)
        result = response.json()

        # NOVO: exibe o JSON retornado para debug
        print("[DEBUG] JSON bruto do OpenRouter:", result)

        resposta_texto = result['choices'][0]['message']['content']

        return {
            "status": 1,
            "response": resposta_texto.strip()
        }

    except Exception as e:
        print(f"[ERRO OpenRouter]: {e}")
        return {"status": 0, "error": str(e)}
