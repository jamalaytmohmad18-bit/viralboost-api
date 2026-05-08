import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def home():
    return "ViralBoost API is Live! 🚀"

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        niche = data.get('niche', 'عام')
        if not niche:
            return jsonify({"error": "المرجو إدخال مجال niche"}), 400

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "messages": [{"role": "user", "content": f"""أنت خبير في المحتوى الفيروسي على TikTok و Instagram Reels.
المجال ديالي هو: {niche}
عطيني 3 أفكار فيديو قصيرة فيروسية دات جودة عالية ومناسبة للمجال.
كل فكرة خاصها تكون فيها:
1. عنوان Hook قوي كيشد فأول 3 ثواني
2. وصف سريع للفكرة ديال الفيديو
3. CTA واضح فاللخر
رجع الجواب بصيغة JSON فقط بهاد الشكل:
{{"ideas": [{{"hook": "العنوان هنا","idea": "وصف الفكرة هنا","cta": "الدعوة لاتخاذ إجراء هنا"}}]}}
لا تزيد أي كلام خارج JSON."""}],
            "model": "llama3-8b-8192",
            "temperature": 0.9,
            "max_tokens": 1024,
            "response_format": {"type": "json_object"}
        }

        response = requests.post(GROQ_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json(), 200

    except Exception as e:
        return jsonify({"error": f"فشل تطبيق Groq API: {str(e)}"}), 500

if __name__ == '__main__':
    app.run()
