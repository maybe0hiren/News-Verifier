from flask import Flask, request, jsonify
from flask_cors import CORS 
import os
import sys
folder_parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if folder_parent_path not in sys.path:
    sys.path.insert(0, folder_parent_path)
from ContextSwitch.interface import segmentation

app = Flask(__name__)
CORS(app)

@app.route('/api/process', methods=['POST'])
def process():
    data = request.json
    text = data.get('text', '')
    result = segmentation(text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
