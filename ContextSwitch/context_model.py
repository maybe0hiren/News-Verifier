# ContextSwitch/context_model.py
import os
import numpy as np
from typing import List, Tuple, Optional
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
import joblib

class ContextModel:
    def __init__(self,
                 embed_model_name: str = "all-MiniLM-L6-v2",
                 clf_path: Optional[str] = None):
        # sentence transformer (embedding)
        self.embedder = SentenceTransformer(embed_model_name)
        self.clf = None
        if clf_path and os.path.exists(clf_path):
            self.clf = joblib.load(clf_path)

    def embed(self, sentences: List[str]) -> np.ndarray:
        """Return NxD embeddings for list of sentences."""
        if not sentences:
            return np.zeros((0, self.embedder.get_sentence_embedding_dimension()))
        return np.array(self.embedder.encode(sentences, convert_to_numpy=True, show_progress_bar=False))

    @staticmethod
    def features_from_pair(e1: np.ndarray, e2: np.ndarray) -> np.ndarray:
        """Create feature vector from two embeddings (abs diff and elementwise product)."""
        diff = np.abs(e1 - e2)
        prod = e1 * e2
        # combine features (2*D -> 768 dims for all-MiniLM)
        feat = np.concatenate([diff, prod], axis=-1)
        return feat

    def predict_similarity_score(self, s1: str, s2: str) -> float:
        """Return cosine similarity in [-1,1] between two sentences (no classifier)."""
        e1 = self.embed([s1])[0]
        e2 = self.embed([s2])[0]
        # cosine
        denom = (np.linalg.norm(e1) * np.linalg.norm(e2)) + 1e-9
        return float(np.dot(e1, e2) / denom)

    def predict_pair(self, s1: str, s2: str, threshold: float = 0.7) -> Tuple[int, float]:
        """
        If classifier present, return (label, prob). label: 1 = same context, 0 = different.
        If no classifier, fall back to thresholding cosine similarity.
        """
        if self.clf is None:
            score = self.predict_similarity_score(s1, s2)
            label = 1 if score >= threshold else 0
            return label, float(score)

        # classifier path
        e1 = self.embed([s1])[0]
        e2 = self.embed([s2])[0]
        feat = self.features_from_pair(e1, e2).reshape(1, -1)
        prob = float(self.clf.predict_proba(feat)[0, 1])
        label = int(prob >= 0.5)
        return label, prob

    def predict_groups(self, groupA: List[str], groupB: List[str], agg: str = "mean", threshold: float = 0.7):
        """
        Compare two groups (lists) of sentences:
         - Compute embeddings for each list, take mean embedding (or median if needed),
         - Then use predict_pair on the two mean embeddings by computing similarity directly or using classifier features.
        Returns (label, score).
        """
        if not groupA or not groupB:
            return 0, 0.0

        embA = np.mean(self.embed(groupA), axis=0)
        embB = np.mean(self.embed(groupB), axis=0)

        if self.clf is None:
            denom = (np.linalg.norm(embA) * np.linalg.norm(embB)) + 1e-9
            score = float(np.dot(embA, embB) / denom)
            label = 1 if score >= threshold else 0
            return label, score

        feat = self.features_from_pair(embA, embB).reshape(1, -1)
        prob = float(self.clf.predict_proba(feat)[0, 1])
        label = int(prob >= 0.5)
        return label, prob

    def train_classifier(self,
                         sentences_a: List[str],
                         sentences_b: List[str],
                         labels: List[int],
                         save_path: Optional[str] = None) -> Tuple[float, object]:
        """
        Train a LogisticRegression classifier on the provided sentence pairs.
        sentences_a, sentences_b: same length lists
        labels: 0/1 list
        Saves to save_path if provided.
        Returns (train_accuracy, trained_clf)
        """
        assert len(sentences_a) == len(sentences_b) == len(labels)
        # embed both lists in a single batch for speed
        emb_a = self.embed(sentences_a)
        emb_b = self.embed(sentences_b)
        feats = np.vstack([self.features_from_pair(a, b) for a, b in zip(emb_a, emb_b)])
        clf = LogisticRegression(max_iter=2000)
        clf.fit(feats, labels)
        self.clf = clf
        if save_path:
            joblib.dump(clf, save_path)
        acc = clf.score(feats, labels)
        return float(acc), clf

    def save_classifier(self, path: str):
        if self.clf is None:
            raise ValueError("No classifier to save.")
        joblib.dump(self.clf, path)
