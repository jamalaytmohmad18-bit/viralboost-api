import os
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)
CORS(app)

# باش يبانو الأخطاء فـ Logs ديال Render
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def home():
    return "ViralBoost API is Live! 🚀"

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        if not GROQ_API_KEY:
            app.logger.error("GROQ_API_KEY is missing!")
            return jsonify({"error": "مفتاح Groq API غير موجود في السيرفر"}), 500

        data = request.get_json()
        niche = data.get('niche', 'عام')
        app.logger.info(f"Received niche: {niche}")

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "messages": [{"role": "user", "content": f"""أنت خبير في المحتوى الفيروسي على TikTok و Instagram Reels.
المجال ديالي هو: {niche}
عطيني 3 أفكار فيديو قصيرة فيروسية.
رجع الجواب بصيغة JSON فقط، بلا أي شرح ولا ```json:
{{"ideas": [{{"hook": "...", "idea": "...", "cta": "..."}}]}}"""}],
            "model": "llama-3.1-8b-instant",
            "temperature": 0.9,
            "max_tokens": 1024
        }

        response = requests.post(GROQ_URL, headers=headers, json=payload)
        app.logger.info(f"Groq response status: {response.status_code}")

        if response.status_code!= 200:
            app.logger.error(f"Groq API failed: {response.status_code} - {response.text}")
            return jsonify({"error": f"Groq API Error: {response.text}"}), 500

        groq_data = response.json()
        content = groq_data['choices'][0]['message']['content']

        # نحيدو ```json و ``` من الجواب يلا كانو
        content = re.sub(r'^```json\s*', '', content)
        content = re.sub(r'\s*```$', '', content)

        app.logger.info("Success: Returning clean JSON")
        return content.strip(), 200, {'Content-Type': 'application/json'}

    except Exception as e:
        app.logger.error(f"Exception: {str(e)}")
        return jsonify({"error": f"فشل تطبيق: {str(e)}"}), 500

if __name__ == '__main__':
    app.run()
