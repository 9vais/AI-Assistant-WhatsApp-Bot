import os
import requests

API_KEY = os.getenv("OPENAI_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def chat_complition(prompt: str) -> dict:
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://openrouter.ai",  # necessário para alguns modelos
            "X-Title": "whatsapp-assistente"
        }

        data = {
            "model": "openchat/openchat-3.5",  # Gratuito
            "messages": [
                {"role": "system", "content": "Você é um assistente pessoal de tarefas. Seja direto, claro e útil."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(API_URL, headers=headers, json=data)
        result = response.json()

        # Depuração no Render
        print(f"[OpenRouter Response] {result}")

        # Acessa corretamente o texto da resposta
        resposta_texto = result['choices'][0]['message']['content']
        return {
            "status": 1,
            "response": resposta_texto.strip()
        }

    except Exception as e:
        print(f"[ERRO OpenRouter]: {e}")
        return {"status": 0, "error": str(e)}
