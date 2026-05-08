import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

# المفتاح كياخدو من Render Environment
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

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

        # البرومبت ديالنا
        prompt = f"""أنت خبير في المحتوى الفيروسي على TikTok و Instagram Reels.
المجال ديالي هو: {niche}
عطيني 3 أفكار فيديو قصيرة فيروسية دات جودة عالية ومناسبة للمجال.
كل فكرة خاصها تكون فيها:
1. عنوان Hook قوي كيشد فأول 3 ثواني
2. وصف سريع للفكرة ديال الفيديو
3. CTA واضح فاللخر

رجع الجواب بصيغة JSON فقط بهاد الشكل:
{{
  "ideas": [
    {{
      "hook": "العنوان هنا",
      "idea": "وصف الفكرة هنا",
      "cta": "الدعوة لاتخاذ إجراء هنا"
    }}
  ]
}}
لا تزيد أي كلام خارج JSON.
"""

        # نعيطو لـ Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192", # هذا هو الموديل المجاني السريع
            temperature=0.9,
            max_tokens=1024,
            top_p=1,
            response_format={"type": "json_object"},
        )

        response_content = chat_completion.choices[0].message.content
        return response_content, 200, {'Content-Type': 'application/json'}

    except Exception as e:
        print(f"Groq API Error: {e}")
        return jsonify({"error": f"فشل تطبيق Groq API: {str(e)}"}), 500

if __name__ == '__main__':
    app.run()
