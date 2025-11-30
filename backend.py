from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from NewsStorage.databaseManager import dbSearch, generate_pHash

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    caption = request.form.get("caption")
    if caption is None:
        return jsonify({"message": "Caption missing"}), 400
    if "image" not in request.files:
        return jsonify({"message": "Image missing"}), 400

    image_file = request.files["image"]
    image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    image_file.save(image_path)

    key = generate_pHash(image_path)
    dbCaption = dbSearch(key)
    print(dbCaption)

    return jsonify({
        "message": "Image and caption uploaded successfully!",
        "saved_caption": dbCaption
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
