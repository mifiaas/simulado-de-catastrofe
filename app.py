from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# URL do Google Apps Script (substitua pela sua)
GOOGLE_SHEETS_URL = "https://script.google.com/macros/s/AKfycbyR8h4p7HrekZHVAZ3m7VUEH90MrMZpJqpykhkC5pTw9JWdgKqPyfINOsVmKCvUql4/exec"

@app.route("/")
def home():
    return "Endpoint ativo! Use /redcap com POST para enviar dados.", 200

@app.route("/redcap", methods=["POST"])
def redcap():
    # Pega os dados enviados pelo REDCap
    record_id = request.form.get('record', 'sem_id')
    total_plan = request.form.get('total_plan', '')
    total_c1 = request.form.get('total_c1', '')
    total_c2 = request.form.get('total_c2', '')
    total_c3 = request.form.get('total_c3', '')
    total_c4 = request.form.get('total_c4', '')

    timestamp = datetime.now().isoformat()

    # Monta o payload a ser enviado ao Google Sheets
    data = [{
        "record_id": record_id,
        "total_plan": total_plan,
        "total_c1": total_c1,
        "total_c2": total_c2,
        "total_c3": total_c3,
        "total_c4": total_c4,
        "timestamp": timestamp
    }]

    try:
        r = requests.post(GOOGLE_SHEETS_URL, json=data)
        print("Google Sheets response:", r.text)
    except Exception as e:
        print("Erro ao enviar para Google Sheets:", e)

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
