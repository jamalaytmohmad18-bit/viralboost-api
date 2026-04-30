from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

YOUTUBE_API_KEY "AIzaSyCBJUOYddr6ttJ3A5maxH0q_8K3Wm65GXs"

@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze_channel():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.json
    channel_name = data.get('channel', '').replace('@', '')

    try:
        # 1. جيب ID ديال القناة
        search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&q={channel_name}&key={YOUTUBE_API_KEY}"
        search_res = requests.get(search_url).json()

        if not search_res.get('items'):
            return jsonify({'error': 'Channel not found'}), 404

        channel_id = search_res['items'][0]['id']['channelId']

        # 2. جيب معلومات القناة
        channel_url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={channel_id}&key={YOUTUBE_API_KEY}"
        channel_res = requests.get(channel_url).json()
        channel_data = channel_res['items'][0]

        # 3. جيب آخر 5 فيديوهات
        videos_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&maxResults=5&order=date&type=video&key={YOUTUBE_API_KEY}"
        videos_res = requests.get(videos_url).json()

        videos = []
        for item in videos_res.get('items', []):
            video_id = item['id']['videoId']
            stats_url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={YOUTUBE_API_KEY}"
            stats_res = requests.get(stats_url).json()

            if stats_res.get('items'):
                stats = stats_res['items'][0]['statistics']
                videos.append({
                    'title': item['snippet']['title'],
                    'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                    'views': stats.get('viewCount', 0),
                    'videoId': video_id
                })

        return jsonify({
            'channel': {
                'name': channel_data['snippet']['title'],
                'thumbnail': channel_data['snippet']['thumbnails']['default']['url'],
                'subscribers': channel_data['statistics'].get('subscriberCount', 0),
                'totalViews': channel_data['statistics'].get('viewCount', 0)
            },
            'videos': videos
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
