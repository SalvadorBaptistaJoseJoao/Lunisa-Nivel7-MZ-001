from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

HF_TOKEN = os.environ.get("HF_TOKEN")
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

SYSTEM_PROMPT = """Você é Lunisa Nivel 7 Absoluta NODE MZ-001 criada em Lichinga Niassa por Salvador Apeiron. 
Estilo serviço secreto: menos palavras, mais impacto.
Ideia imortalizada. 3 passos para utilidade imediata: 1... 2... 3...
"""

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")
    
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": f"<s>[INST] {SYSTEM_PROMPT}\nUsuario: {user_msg} [/INST]",
        "parameters": {"max_new_tokens": 500, "temperature": 0.7}
    }
    
    try:
        resp = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL}",
            headers=headers,
            json=payload,
            timeout=60
        )
        result = resp.json()
        if isinstance(result, list):
            answer = result[0].get("generated_text", "").split("[/INST]")[-1].strip()
        else:
            answer = str(result)
        return jsonify({"reply": answer})
    except Exception as e:
        return jsonify({"reply": f"Erro Lunisa NODE MZ-001: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
