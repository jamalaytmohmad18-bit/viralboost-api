from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    if request.method == 'OPTIONS':
        return '', 200
    
    data = request.get_json()
    channel = data.get('channel', 'unknown')
    
    result = {
        'status': 'success',
        'channel': channel,
        'subscribers': '10.5M',
        'message': 'الموقع خدام مزيان 🎉'
    }
    return jsonify(result), 200

if __name__ == '__main__':
    app.run()
