from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# URL do Google Sheets (Apps Script)
GOOGLE_SHEETS_URL = "https://script.google.com/macros/s/AKfycbyR8h4p7HrekZHVAZ3m7VUEH90MrMZpJqpykhkC5pTw9JWdgKqPyfINOsVmKCvUql4/exec"

# Rota raiz para testar se o serviço está ativo
@app.route("/")
def home():
    return "✅ Endpoint ativo! Use /redcap com POST para enviar dados.", 200

# Rota que recebe os dados do REDCap
@app.route("/redcap", methods=["POST"])
def redcap():
    # Pega apenas o record_id enviado pelo REDCap
    record_id = request.form.get('record', 'sem_id')
    timestamp = datetime.now().isoformat()

    # Monta o payload para enviar ao Google Sheets
    data = [{
        "record_id": record_id,
        "timestamp": timestamp
    }]

    # Envia para a planilha
    try:
        r = requests.post(GOOGLE_SHEETS_URL, json=data)
        print("Google Sheets response:", r.text)
    except Exception as e:
        print("Erro ao enviar para Google Sheets:", e)

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


