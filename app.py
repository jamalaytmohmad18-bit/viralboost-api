from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# حط الـ API Key ديالك هنا بين " "
YOUTUBE_API_KEY = "AIzaSyCBJUOYddr6ttJ3A5maxH0q_8K3Wm65GXs"

@app.route('/api/analyze', methods=['POST'])
def analyze_channel():
    try:
        data = request.get_json()
        channel_input = data.get('channel', '').strip()

        if not channel_input:
            return jsonify({'error': 'Channel name is required'}), 400

        if not YOUTUBE_API_KEY or YOUTUBE_API_KEY == "حط-الـKEY-ديالك-هنا":
            return jsonify({'error': 'YouTube API Key not configured'}), 500

        # Clean channel name
        if channel_input.startswith('@'):
            channel_input = channel_input[1:]

        # 1. Get channel ID from username
        search_url = f"https://www.googleapis.com/youtube/v3/search"
        search_params = {
            'part': 'snippet',
            'q': channel_input,
            'type': 'channel',
            'key': YOUTUBE_API_KEY,
            'maxResults': 1
        }

        search_response = requests.get(search_url, params=search_params)
        search_data = search_response.json()

        if 'error' in search_data:
            return jsonify({'error': search_data['error']['message']}), 400

        if not search_data.get('items'):
            return jsonify({'error': 'Channel not found'}), 404

        channel_id = search_data['items'][0]['snippet']['channelId']

        # 2. Get channel stats
        channel_url = f"https://www.googleapis.com/youtube/v3/channels"
        channel_params = {
            'part': 'snippet,statistics',
            'id': channel_id,
            'key': YOUTUBE_API_KEY
        }

        channel_response = requests.get(channel_url, params=channel_params)
        channel_data = channel_response.json()

        if not channel_data.get('items'):
            return jsonify({'error': 'Channel details not found'}), 404

        channel_info = channel_data['items'][0]
        stats = channel_info['statistics']
        snippet = channel_info['snippet']

        # 3. Get latest videos
        videos_url = f"https://www.googleapis.com/youtube/v3/search"
        videos_params = {
            'part': 'snippet',
            'channelId': channel_id,
            'type': 'video',
            'order': 'date',
            'key': YOUTUBE_API_KEY,
            'maxResults': 5
        }

        videos_response = requests.get(videos_url, params=videos_params)
        videos_data = videos_response.json()

        videos = []
        for item in videos_data.get('items', []):
            videos.append({
                'title': item['snippet']['title'],
                'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                'videoId': item['id']['videoId'],
                'publishedAt': item['snippet']['publishedAt']
            })

        result = {
            'channelName': snippet['title'],
            'channelId': channel_id,
            'subscribers': stats.get('subscriberCount', '0'),
            'totalViews': stats.get('viewCount', '0'),
            'videoCount': stats.get('videoCount', '0'),
            'description': snippet['description'],
            'thumbnail': snippet['thumbnails']['high']['url'],
            'latestVideos': videos
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
