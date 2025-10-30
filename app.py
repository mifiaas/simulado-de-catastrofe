from flask import Flask, request
import requests
from datetime import datetime

app = Flask(__name__)

POWERBI_URL = "https://api.powerbi.com/beta/f85b6051-e263-462b-9ca5-f211f1f783d2/datasets/e3190e2e-748b-4e94-8571-df62578bbd5b/rows?experience=power-bi&key=hmmd2YgFcFYVzEDqMI0MtbMvsJIy3dnoUIVd0hAi7I9peGu9YIZK5OU7bCy7I2HCu6Jce7Z9FwcbpEZMJtRGCw%3D%3D"

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

