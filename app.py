from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    channel = data.get('channel', '').replace('@', '').strip()
    
    if not channel:
        return jsonify({"status": "error", "message": "Channel name is required"}), 400
    
    try:
        url = f"https://www.youtube.com/@{channel}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return jsonify({"status": "error", "message": f"YouTube returned {response.status_code}"}), 404

        text = response.text
        
        subs_match = re.search(r'"subscriberCountText":{"simpleText":"(.*?)"', text)
        subs = subs_match.group(1) if subs_match else "Hidden"
        
        views_match = re.search(r'"viewCountText":{"simpleText":"(.*?)"', text)
        views = views_match.group(1).replace(' views', '') if views_match else "0"
        
        avatar_match = re.search(r'"avatar":{"thumbnails":\[{"url":"(.*?)"', text)
        avatar = avatar_match.group(1) if avatar_match else ""
        
        name_match = re.search(r'"channelMetadataRenderer":{"title":"(.*?)"', text)
        name = name_match.group(1) if name_match else f"@{channel}"
        
        return jsonify({
            "status": "success",
            "data": {
                "name": name,
                "handle": f"@{channel}",
                "avatar": avatar,
                "subscribers": subs,
                "views": views,
                "videos": []
            }
        })
        
    except requests.exceptions.Timeout:
        return jsonify({"status": "error", "message": "Request to YouTube timed out"}), 504
    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500
