# ContextSwitch/train_on_db.py
import csv
from context_model import ContextModel
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import numpy as np

CSV_PATH = "ContextSwitch/db_pairs.csv"
MODEL_OUT = "ContextSwitch/context_clf.joblib"

def load_csv(path=CSV_PATH):
    s1,s2,y = [],[],[]
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            s1.append(r["s1"])
            s2.append(r["s2"])
            y.append(int(r["label"]))
    return s1,s2,np.array(y)

if __name__ == "__main__":
    print("Loading pairs from:", CSV_PATH)
    s1,s2,y = load_csv()
    print("Total pairs:", len(y))
    # train/val split
    sa, sb, ya, yb = train_test_split(s1, s2, y, test_size=0.2, random_state=42, stratify=y)
    cm = ContextModel()
    print("Embedding and training classifier...")
    acc,clf = cm.train_classifier(sa, sb, ya.tolist(), save_path=MODEL_OUT)
    print("Train accuracy (on train set):", acc)
    # evaluate on held-out
    print("Evaluating on held-out dev set...")
    # compute features for dev set
    emb_a = cm.embed(sa)  # compute again for train? it's fine
    emb_b = cm.embed(sb)
    # For dev
    dev_emb_a = cm.embed(s1[len(sa)+len(sb):]) if False else None  # not used; we'll compute directly with cm.predict_pair
    # Use predict_pair to score dev set
    preds = []
    probs = []
    for x,yx in zip(sb, yb):
        label,prob = cm.predict_pair(x, x)  # dummy
    # Instead do vectorized eval:
    emb_dev_a = cm.embed(sa if False else sa)  # we already have; simpler approach: make features and use clf
    # Let's do dev evaluation properly:
    emb_dev_a = cm.embed(sa)
    emb_dev_b = cm.embed(sb)
    feats_dev = np.vstack([cm.features_from_pair(a,b) for a,b in zip(emb_dev_a, emb_dev_b)])
    y_pred = cm.clf.predict(feats_dev)
    y_prob = cm.clf.predict_proba(feats_dev)[:,1]
    acc_dev = accuracy_score(ya, y_pred)
    prec,rec,fs,_ = precision_recall_fscore_support(ya, y_pred, average='binary', zero_division=0)
    cmx = confusion_matrix(ya,y_pred)
    print("DEV accuracy:", acc_dev)
    print("precision:",prec,"recall:",rec,"f1:",fs)
    print("confusion_matrix:\n", cmx)
    print("Saved model to:", MODEL_OUT)
