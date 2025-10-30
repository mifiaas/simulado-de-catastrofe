from flask import Flask, request
import requests
from datetime import datetime

app = Flask(__name__)

POWERBI_URL = "COLE_AQUI_SUA_PUSH_URL_DO_POWERBI"

@app.route("/redcap", methods=["POST"])
def redcap_webhook():
    data = request.form.to_dict()
    record_id = data.get("record_id")  # Pega apenas o record_id
    
    print("Dados recebidos do REDCap:", data)
    
    payload = [{
        "record_id": record_id,
        "timestamp": datetime.now().isoformat()  # Adiciona timestamp para Power BI
    }]
    
    r = requests.post(POWERBI_URL, json=payload)
    print("Status Power BI:", r.status_code, r.text)
    
    return "Dados recebidos com sucesso!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
