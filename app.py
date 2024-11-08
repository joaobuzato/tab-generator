from flask import Flask, jsonify, request
from services import audio_service

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "API Up! Use /process to process audio"})

@app.route('/process', methods=['POST'])
def process():
    body = request.get_json()
    filepath = body['filepath']
    notes = audio_service.extract_frequencies(filepath)
    return jsonify({"notes": notes})

if __name__ == '__main__':
    app.run(debug=True)
