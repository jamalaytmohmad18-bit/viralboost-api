from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    channel = data.get('channel', '').replace('@', '')
    
    try:
        # كايقلب على القناة فـ يوتيوب
        url = f"https://www.youtube.com/@{channel}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        
        # كايستخرج البيانات من الصفحة
        subs = re.search(r'"subscriberCountText":{"simpleText":"(.*?)"', response.text)
        subs = subs.group(1) if subs else "0"
        
        views = re.search(r'"viewCountText":{"simpleText":"(.*?)"', response.text)
        views = views.group(1).replace(' views', '') if views else "0"
        
        avatar = re.search(r'"avatar":{"thumbnails":\[{"url":"(.*?)"', response.text)
        avatar = avatar.group(1) if avatar else ""
        
        return jsonify({
            "status": "success",
            "data": {
                "name": f"@{channel}",
                "avatar": avatar,
                "subscribers": subs,
                "views": views,
                "videos": []
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run()
