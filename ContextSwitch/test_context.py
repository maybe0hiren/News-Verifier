# ContextSwitch/test_context.py
from context_model import ContextModel

cm = ContextModel(clf_path="ContextSwitch/context_clf.joblib")
pairs = [
    ("The president announced a new healthcare bill", "A healthcare bill was introduced by the government"),
    ("A wildfire burned acres of forest", "The basketball team won their game"),
]
for a,b in pairs:
    label,score = cm.predict_pair(a,b)
    print("A:",a)
    print("B:",b)
    print("label (1=same):",label,"score:",score)
    print("-"*40)
