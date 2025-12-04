# ContextSwitch/test_context_db.py
from context_model import ContextModel

MODEL_PATH = "ContextSwitch/context_clf.joblib"
cm = ContextModel(clf_path=MODEL_PATH)

examples = [
    ("The mayor cut the ribbon at the new hospital opening.", "A ribbon cutting ceremony marked the opening of the city's hospital."),
    ("An earthquake struck the coastal town causing damage.", "The new phone model has a better camera and battery life.")
]

for a,b in examples:
    label,score = cm.predict_pair(a,b)
    print("A:", a)
    print("B:", b)
    print("label (1=same):", label, "score:", score)
    print("-"*60)
