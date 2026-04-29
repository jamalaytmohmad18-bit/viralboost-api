from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

YOUTUBE_API_KEY = "AIzaSyA8kW0IA6Qg9JXjQ2Pj4V3Xz5"

@app.route('/')
def home():
    return jsonify({
        "status": "success",
        "message": "ViralBoost API is running",
        "endpoints": {
            "analyze": "/analyze [POST]"
        }
    })

@app.route('/analyze', methods=['POST'])
def analyze_channel():
    try:
        data = request.get_json()
        channel_url = data.get('url', '')

        if 'youtube.com' not in channel_url:
            return jsonify({"error": "رابط غير صحيح"}), 400

        channel_id = ""
        if '/channel/' in channel_url:
            channel_id = channel_url.split('/channel/')[1].split('/')[0]
        else:
            return jsonify({"error": "حط رابط القناة الكامل لي فيه /channel/"}), 400

        url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics,snippet&id={channel_id}&key={YOUTUBE_API_KEY}"
        response = requests.get(url)
        result = response.json()

        if 'items' not in result or len(result['items']) == 0:
            return jsonify({"error": "القناة غير موجودة"}), 404

        channel_data = result['items'][0]
        stats = channel_data['statistics']
        snippet = channel_data['snippet']

        return jsonify({
            "title": snippet['title'],
            "subscribers": stats.get('subscriberCount', '0'),
            "views": stats.get('viewCount', '0'),
            "videos": stats.get('videoCount', '0'),
            "thumbnail": snippet['thumbnails']['high']['url']
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
