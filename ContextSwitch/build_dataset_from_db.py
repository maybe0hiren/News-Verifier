# ContextSwitch/build_dataset_from_db.py
import sqlite3
import csv
import random
import os
from itertools import combinations

DB_PATH = "NewsStorage/storage.db"     # relative path from repo root
OUT_CSV = "ContextSwitch/db_pairs.csv"  # created in repo

def load_captions(limit_hashes=None):
    """
    Return dict: {hash: [caption1, caption2, ...]} with empty captions removed.
    """
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("PRAGMA journal_mode=WAL;")
    cur.execute("SELECT * FROM storage")
    rows = cur.fetchall()
    col_names = [d[0] for d in cur.description]
    # caption columns are caption1..caption50
    caption_cols = [c for c in col_names if c.startswith("caption")]
    data = {}
    for row in rows:
        rowd = dict(zip(col_names, row))
        h = rowd.get('hash')
        captions = []
        for c in caption_cols:
            txt = rowd.get(c)
            if txt and isinstance(txt, str):
                t = txt.strip()
                if len(t) >= 5:
                    captions.append(t)
        if captions:
            data[h] = captions
        if limit_hashes and len(data) >= limit_hashes:
            break
    con.close()
    return data

def build_pairs(data, max_pos_per_hash=200, neg_pos_ratio=1.0, random_seed=42):
    """
    Build positive and negative pairs.
    - data: {hash: [caps...]}
    - max_pos_per_hash: cap the number of positive pairs per hash to avoid explosion.
    - neg_pos_ratio: how many negative examples per positive example
    """
    random.seed(random_seed)
    positives = []
    for h, caps in data.items():
        # all combinations of captions from same hash
        pairs = list(combinations(caps, 2))
        if len(pairs) > max_pos_per_hash:
            pairs = random.sample(pairs, max_pos_per_hash)
        positives.extend(pairs)

    # build caption pool for negatives (one caption per hash to reduce collision)
    hash_caps = []
    for h, caps in data.items():
        # pick one representative caption per hash randomly
        hash_caps.append((h, random.choice(caps)))

    negatives = []
    # sample negative pairs by pairing captions from different hashes
    num_neg = int(len(positives) * neg_pos_ratio)
    if num_neg == 0:
        num_neg = len(positives)
    while len(negatives) < num_neg:
        a = random.choice(hash_caps)
        b = random.choice(hash_caps)
        if a[0] == b[0]:
            continue
        negatives.append((a[1], b[1]))

    return positives, negatives

def write_csv(positives, negatives, out_path=OUT_CSV):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["s1","s2","label"])
        for a,b in positives:
            writer.writerow([a,b,1])
        for a,b in negatives:
            writer.writerow([a,b,0])
    print(f"Wrote {len(positives)} positives and {len(negatives)} negatives to {out_path}")

if __name__ == "__main__":
    print("Loading captions from DB:", DB_PATH)
    data = load_captions(limit_hashes=None)  # use all hashes; set limit_hashes=500 to debug
    print("Hashes with captions:", len(data))
    pos, neg = build_pairs(data, max_pos_per_hash=200, neg_pos_ratio=1.0)
    write_csv(pos, neg)
