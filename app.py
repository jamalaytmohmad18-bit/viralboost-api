from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

YOUTUBE_API_KEY = "AIzaSyA8kW0IA6Qg9JXjQ2Pj4V3Xz5Zq8X7Y9Z0"

@app.route('/analyze', methods=['POST'])
def analyze_channel():
    try:
        data = request.get_json()
        channel_url = data.get('url', '')
        
        if 'youtube.com' not in channel_url:
            return jsonify({'error': 'رابط غير صحيح'}), 400
            
        if '/channel/' in channel_url:
            channel_id = channel_url.split('/channel/')[1].split('/')[0]
        elif '/@' in channel_url:
            username = channel_url.split('/@')[1].split('/')[0]
            search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={username}&type=channel&key={YOUTUBE_API_KEY}"
            search_response = requests.get(search_url)
            channel_id = search_response.json()['items'][0]['id']['channelId']
        else:
            return jsonify({'error': 'الرابط غير مدعوم'}), 400
        
        stats_url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics,snippet&id={channel_id}&key={YOUTUBE_API_KEY}"
        stats_response = requests.get(stats_url)
        channel_data = stats_response.json()['items'][0]
        
        subs = int(channel_data['statistics']['subscriberCount'])
        views = int(channel_data['statistics']['viewCount'])
        videos = int(channel_data['statistics']['videoCount'])
        
        score = 0
        if subs > 100000: score += 30
        elif subs > 10000: score += 20
        elif subs > 1000: score += 10
        
        if views/subs > 100: score += 25
        elif views/subs > 50: score += 15
        
        if videos > 100: score += 20
        elif videos > 50: score += 10
        
        result = {
            'channel_name': channel_data['snippet']['title'],
            'subscribers': subs,
            'total_views': views,
            'video_count': videos,
            'score': min(score, 100),
            'status': 'ناجحة' if score > 60 else 'متوسطة' if score > 30 else 'ضعيفة'
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
