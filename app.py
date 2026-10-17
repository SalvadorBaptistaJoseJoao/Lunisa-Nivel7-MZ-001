from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os, requests
app = Flask(__name__)
CORS(app)
HF_TOKEN = os.environ.get("HF_TOKEN", "")
MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
@app.route("/")
def home():
    return send_from_directory(".", "index.html")
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_msg = data.get("message", "")
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        payload = {"inputs": f"[INST] Voce e Lunisa Nivel 7 Absoluta MZ-001 criada por Salvador em Lichinga. Responda curto estilo servico secreto. Usuario: {user_msg} [/INST]", "parameters": {"max_new_tokens": 250, "temperature": 0.7, "return_full_text": False}}
        r = requests.post(MODEL_URL, headers=headers, json=payload, timeout=60)
        j = r.json()
        if isinstance(j, list) and j:
            reply = j[0].get("generated_text", "Lunisa online")
        elif isinstance(j, dict) and "error" in j:
            reply = f"HF: {j['error']} - aguarda 20s"
        else:
            reply = str(j)[:400]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Erro MZ-001: {str(e)}"})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
