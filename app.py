from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # هادي كتحل مشكل Failed to fetch مع v0

@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    # ضروري للـ CORS
    if request.method == 'OPTIONS':
        return '', 200

    try:
        # كناخدو اسم القناة من v0
        data = request.get_json()
        channel = data.get('channel')
        
        if not channel:
            return jsonify({"error": "Channel name is required"}), 400

        # مثال للتجريب - غادي نبدلوه من بعد بالحقيقي
        result = {
            "title": channel.replace("@", ""),
            "subscribers": 320000000,
            "views": 50000000000,
            "videoCount": 800,
            "thumbnail": "https://yt3.ggpht.com/ytc/AIdro_lh0bO9u-j-k-lM="
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
