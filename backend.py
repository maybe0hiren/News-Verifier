from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from NewsStorage.databaseManager import dbSearch, generate_pHash
from Comparison.report import getReport
from ContextSwitch.context_model import ContextModel
import json

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

    articles = [str(caption), str(dbCaption)]
    [similarity, report] = getReport(articles)
    similarity = str(similarity)
    report = str(report)

    return jsonify({
        "message": "Image and caption uploaded successfully!",
        "dbCaption": dbCaption,
        "similarity": similarity,
        "report" : report
    }), 200

# initialize once (loads model when backend starts)
CTX_MODEL_PATH = "ContextSwitch/context_clf.joblib"  # classifier saved from Colab
context_model = ContextModel(clf_path=CTX_MODEL_PATH)

@app.route("/api/context_check", methods=["POST"])
def context_check():
    """
    Accepts JSON:
    {
      "groupA": ["sentence 1", ...],   # or "sentences": ["single sentence", ...]
      "groupB": ["sentence a", ...],   # optional; if omitted, groupB must be provided in body as "sentences_b"
      "threshold": 0.7   # optional for cosine fallback
    }
    Returns: { "label": 0|1, "score": float, "explanation": "..." }
    """
    data = request.get_json(force=True)
    groupA = data.get("groupA") or data.get("sentences") or []
    groupB = data.get("groupB") or data.get("sentences_b") or []
    threshold = float(data.get("threshold", 0.7))

    if not groupA or not groupB:
        return jsonify({"error":"Provide both groupA and groupB as non-empty lists of sentences"}), 400

    label, score = context_model.predict_groups(groupA, groupB, threshold=threshold)
    # Simple explanation
    explanation = "Same context" if label == 1 else "Different context"
    return jsonify({"label": int(label), "score": float(score), "explanation": explanation}), 200



if __name__ == "__main__":
    app.run(debug=True)
