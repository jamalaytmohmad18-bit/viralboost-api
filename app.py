from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

YOUTUBE_API_KEY =  "AIzaSyCBJUOYddr6ttJ3A5maxH0q_8K3Wm65GXsبدل_هادي_بالـKey_ديالك"

@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json()
        channel = data.get('channel').replace("@", "")

        # 1. نجيبو Channel ID
        search_url = "https://www.googleapis.com/youtube/v3/search"
        search_params = {"part": "snippet", "q": channel, "type": "channel", "maxResults": 1, "key": YOUTUBE_API_KEY}
        search_res = requests.get(search_url, params=search_params).json()

        if not search_res.get("items"):
            return jsonify({"error": "Channel not found"}), 404

        channel_id = search_res["items"][0]["snippet"]["channelId"]

        # 2. نجيبو إحصائيات القناة
        stats_url = "https://www.googleapis.com/youtube/v3/channels"
        stats_params = {"part": "statistics,snippet", "id": channel_id, "key": YOUTUBE_API_KEY}
        stats_data = requests.get(stats_url, params=stats_params).json()["items"][0]

        # 3. نجيبو آخر 5 فيديوهات
        videos_url = "https://www.googleapis.com/youtube/v3/search"
        videos_params = {
            "part": "snippet",
            "channelId": channel_id,
            "order": "date",
            "maxResults": 5,
            "type": "video",
            "key": YOUTUBE_API_KEY
        }
        videos_items = requests.get(videos_url, params=videos_params).json()["items"]

        # 4. نجيبو مشاهدات كل فيديو
        video_ids = ",".join([v["id"]["videoId"] for v in videos_items])
        details_url = "https://www.googleapis.com/youtube/v3/videos"
        details_params = {"part": "statistics,snippet", "id": video_ids, "key": YOUTUBE_API_KEY}
        videos_details = requests.get(details_url, params=details_params).json()["items"]

        # 5. نرجعو كلشي لـ v0
        result = {
            "channel_stats": {
                "title": stats_data["snippet"]["title"],
                "subscribers": int(stats_data["statistics"].get("subscriberCount", 0)),
                "views": int(stats_data["statistics"].get("viewCount", 0)),
                "thumbnail": stats_data["snippet"]["thumbnails"]["high"]["url"]
            },
            "last_5_videos": [
                {
                    "title": v["snippet"]["title"],
                    "views": int(v["statistics"].get("viewCount", 0)),
                    "thumbnail": v["snippet"]["thumbnails"]["medium"]["url"],
                    "video_id": v["id"]
                } for v in videos_details
            ]
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
