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
            "model": "mistralai/mistral-7b-instruct",  # modelo válido e gratuito
            "messages": [
                {"role": "system", "content": "Você é um assistente pessoal de tarefas."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(API_URL, headers=headers, json=data)
        result = response.json()

        print("[DEBUG] JSON bruto do OpenRouter:", result)

        if "choices" in result and isinstance(result["choices"], list):
            content = result["choices"][0]["message"]["content"]
            return {
                "status": 1,
                "response": content.strip()
            }
        else:
            return {
                "status": 0,
                "error": f"Resposta inválida da IA: {result}"
            }

    except Exception as e:
        print(f"[ERRO OpenRouter]: {e}")
        return {"status": 0, "error": str(e)}
