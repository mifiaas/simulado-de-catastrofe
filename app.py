from flask import Flask, request

app = Flask(__name__)

@app.route("/redcap", methods=["POST"])
def redcap_webhook():
    data = request.form.to_dict()
    print("Dados recebidos do REDCap:", data)
    return "Dados recebidos com sucesso!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
