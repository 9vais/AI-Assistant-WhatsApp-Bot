import json
import os
import time
from datetime import datetime
from twilio.rest import Client

TAREFAS_FILE = "tarefas.json"

# Carrega variáveis de ambiente
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def carregar_tarefas():
    if os.path.exists(TAREFAS_FILE):
        with open(TAREFAS_FILE, 'r') as f:
            return json.load(f)
    return []

def salvar_tarefas(tarefas):
    with open(TAREFAS_FILE, 'w') as f:
        json.dump(tarefas, f, indent=2)

def verificar_lembretes():
    agora = datetime.now().strftime("%H:%M")
    tarefas = carregar_tarefas()
    lembretes_enviados = 0

    for tarefa in tarefas:
        if tarefa.get("agendado") and not tarefa.get("concluida"):
            if tarefa.get("hora") == agora:
                numero = tarefa.get("telefone")
                texto = f"⏰ Lembrete: {tarefa['descricao']}"
                try:
                    message = client.messages.create(
                        body=texto,
                        from_=TWILIO_PHONE,
                        to=numero
                    )
                    print(f"[✔] Lembrete enviado para {numero}: {texto}")
                    tarefa["concluida"] = True
                    lembretes_enviados += 1
                except Exception as e:
                    print(f"[ERRO] Falha ao enviar lembrete: {e}")

    if lembretes_enviados > 0:
        salvar_tarefas(tarefas)

if __name__ == "__main__":
    print("🔁 Agendador iniciado. Verificando a cada 60 segundos...")
    while True:
        verificar_lembretes()
        time.sleep(60)
