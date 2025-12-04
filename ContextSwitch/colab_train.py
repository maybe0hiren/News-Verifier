# ContextSwitch/colab_train.py
from context_model import ContextModel
import csv
import os

def build_small_synthetic_dataset(path="ContextSwitch/synthetic_pairs.csv"):
    # Creates a small dataset of pairs with label 1 (same context) or 0 (different).
    rows = [
        ("The government introduced new tax reforms today.", "Parliament passed a new tax reform law.", 1),
        ("Manchester won the match by two goals.", "The football team celebrated their championship win.", 1),
        ("The river flood affected thousands of people.", "New model phones were released this month.", 0),
        ("Scientists discovered a new vaccine.", "The economy saw a decline in the stock market.", 0),
        ("Apple released its quarterly earnings report.", "The tech company reported earnings beating estimates.", 1),
        ("Heavy rains flooded the city.", "The local bakery sold out of cakes.", 0),
    ]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["s1","s2","label"])
        writer.writerows(rows)
    print("Wrote dataset to", path)

def load_pairs(path="ContextSwitch/synthetic_pairs.csv"):
    import csv
    s1,s2,lab = [],[],[]
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            s1.append(r["s1"])
            s2.append(r["s2"])
            lab.append(int(r["label"]))
    return s1,s2,lab

if __name__ == "__main__":
    build_small_synthetic_dataset()
    cm = ContextModel()
    s1,s2,y = load_pairs()
    acc,clf = cm.train_classifier(s1,s2,y, save_path="ContextSwitch/context_clf.joblib")
    print("Train accuracy (on synthetic):", acc)
