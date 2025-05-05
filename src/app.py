from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import json
import os
from datetime import datetime

app = Flask(__name__)

TAREFAS_FILE = "tarefas.json"

def carregar_tarefas():
    if os.path.exists(TAREFAS_FILE):
        with open(TAREFAS_FILE, 'r') as f:
            return json.load(f)
    return []

def salvar_tarefas(tarefas):
    with open(TAREFAS_FILE, 'w') as f:
        json.dump(tarefas, f, indent=2)

@app.route('/')
def home():
    return jsonify({"status": "OK", "message": "Assistente ativo com agendamento."})

@app.route('/twilio/receiveMessage', methods=['POST'])
def receiveMessage():
    try:
        mensagem = request.form['Body'].strip().lower()
        telefone = request.form['From']
        tarefas = carregar_tarefas()
        resp = MessagingResponse()

        if mensagem.startswith("adicionar tarefa:"):
            descricao = mensagem.replace("adicionar tarefa:", "").strip()
            tarefas.append({"descricao": descricao, "concluida": False})
            salvar_tarefas(tarefas)
            resp.message(f"Tarefa adicionada: {descricao}")

        elif mensagem.startswith("agendar:"):
            try:
                texto = mensagem.replace("agendar:", "").strip()
                if " às " in texto:
                    descricao, hora = texto.split(" às ")
                    hora_agendada = datetime.strptime(hora.strip(), "%H:%M").strftime("%H:%M")
                    tarefas.append({
                        "descricao": descricao.strip(),
                        "hora": hora_agendada,
                        "concluida": False,
                        "agendado": True,
                        "telefone": telefone
                    })
                    salvar_tarefas(tarefas)
                    resp.message(f"Tarefa agendada para {hora_agendada}: {descricao.strip()}")
                else:
                    resp.message("Use o formato: agendar: tarefa às HH:MM")
            except:
                resp.message("Formato inválido. Exemplo: agendar: beber água às 15:00")

        elif mensagem == "listar tarefas":
            if not tarefas:
                resp.message("Você não tem tarefas.")
            else:
                resposta = "📋 Suas tarefas:\n"
                for i, t in enumerate(tarefas):
                    status = "✅" if t["concluida"] else "❌"
                    hora = f" às {t['hora']}" if t.get("hora") else ""
                    resposta += f"{i+1}. {t['descricao']}{hora} {status}\n"
                resp.message(resposta)

        elif mensagem.startswith("concluir tarefa"):
            try:
                num = int(mensagem.replace("concluir tarefa", "").strip()) - 1
                if 0 <= num < len(tarefas):
                    tarefas[num]["concluida"] = True
                    salvar_tarefas(tarefas)
                    resp.message(f"Tarefa {num+1} marcada como concluída.")
                else:
                    resp.message("Número inválido.")
            except:
                resp.message("Formato inválido. Use: concluir tarefa 1")

        else:
            comandos = (
                "Comandos disponíveis:\n"
                "➕ adicionar tarefa: comprar pão\n"
                "📋 listar tarefas\n"
                "✅ concluir tarefa 1\n"
                "⏰ agendar: beber água às 15:30"
            )
            resp.message(comandos)

        return str(resp)

    except Exception as e:
        print(f"[ERRO]: {e}")
        resp = MessagingResponse()
        resp.message("Erro ao processar a mensagem.")
        return str(resp)
