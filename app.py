from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

@app.route('/')
def home():
    return "ViralBoost API is Live with Groq 🔥"

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    niche = data.get('niche', 'general')
    prompt = f"Generate 3 viral content ideas for {niche} niche. Format as a numbered list."
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "llama-3.1-70b-versatile"
    }
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        ai_reply = result['choices'][0]['message']['content']
        return jsonify({"ideas": ai_reply})
    else:
        return jsonify({"error": "Groq API failed"}), 500

if __name__ == '__main__':
    app.run()
