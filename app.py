from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # هادا هو السر باش يخدم مع v0

@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        channel = data.get('channel', 'unknown')
        
        # نتيجة مؤقتة باش نتأكدو باللي كلشي خدام
        result = {
            'status': 'success',
            'channel': channel,
            'subscribers': '10.5M',
            'avg_views': '2.3M',
            'engagement': '8.2%',
            'message': 'الموقع خدام مزيان 🎉'
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
