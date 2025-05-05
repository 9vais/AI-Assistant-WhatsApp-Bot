import os
from openai import OpenAI
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Cria cliente com a chave da API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_complition(prompt: str) -> dict:
    try:
        # Envia a pergunta para o ChatGPT
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "Você é um assistente pessoal de tarefas. Responda com clareza e objetividade."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extrai o conteúdo da resposta
        return {
            'status': 1,
            'response': response.choices[0].message.content
        }
    except Exception as e:
        print(f"[ERRO OpenAI]: {e}")
        return {'status': 0, 'error': str(e)}
