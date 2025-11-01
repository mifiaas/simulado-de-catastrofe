from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# URL da API do REDCap
REDCAP_API_URL = "https://redcap.fcmsantacasasp.edu.br/api/"
REDCAP_TOKEN = "2B90EF2F5C5A59B08A6655751F613365"

# URL do Google Apps Script – substitua quando implantar
GOOGLE_SHEETS_URL = "https://script.google.com/macros/s/AKfycbyOmdDbI7e2LkEfRSL6Px8Xgo1ouwQ6IeuD1dQuAjJ-rqhGE2gyOT-psiXcU53Zeuyywg/exec"

@app.route("/")
def home():
    return "Endpoint ativo! Use /redcap com POST para enviar dados.", 200

@app.route("/redcap", methods=["POST"])
def redcap():
    record_id = request.form.get("record")
    if not record_id:
        print("❌ Sem record_id recebido do REDCap")
        return jsonify({"error": "Sem record_id"}), 400

    print(f"📩 Trigger recebido para record_id={record_id}")

    payload = {
        "token": REDCAP_TOKEN,
        "content": "record",
        "format": "json",
        "type": "flat",
        "records[0]": record_id
    }

    try:
        redcap_response = requests.post(REDCAP_API_URL, data=payload)
        redcap_data = redcap_response.json()
        print("📤 Resposta do REDCap:", redcap_data)

        if not redcap_data:
            print("⚠️ Nenhum dado retornado do REDCap.")
            return jsonify({"error": "Nenhum dado retornado do REDCap"}), 404

        registro = redcap_data[0]

        data = [{
            "record_id": str(registro.get("record_id", "")),
            "total_plan": registro.get("total_plan", ""),
            "total_c1": registro.get("total_c1", ""),
            "total_c2": registro.get("total_c2", ""),
            "total_c3": registro.get("total_c3", ""),
            "total_c4": registro.get("total_c4", ""),
            "timestamp": datetime.now().isoformat()
        }]

        print("📦 Enviando ao Google Sheets:", data)

        r = requests.post(GOOGLE_SHEETS_URL, json=data)
        print("🪵 Resposta do Google Script:", r.text)

    except Exception as e:
        print("🚨 Erro no processo:", e)
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
