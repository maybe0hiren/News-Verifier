# Comparison/context_features.py

from typing import List, Dict, Any
from itertools import combinations

import numpy as np
from sentence_transformers import SentenceTransformer

# Load model once at module import.
# If you already use a sentence-transformers model elsewhere, you can:
# - either share the model instance
# - or use the same model name here for consistency.
_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
_model = SentenceTransformer(_MODEL_NAME)


def compute_embeddings(sentences: List[str]) -> np.ndarray:
    """
    Convert sentences into L2-normalized embedding vectors.

    Args:
        sentences: List of sentence strings.

    Returns:
        np.ndarray of shape (n_sentences, embedding_dim).
    """
    if not sentences:
        raise ValueError("compute_embeddings(): 'sentences' list cannot be empty.")

    # normalize_embeddings=True ensures each vector has unit length.
    embeddings = _model.encode(sentences, normalize_embeddings=True)
    return np.array(embeddings, dtype=float)


def pairwise_similarities(embeddings: np.ndarray) -> np.ndarray:
    """
    Compute all unique pairwise cosine similarities for a set of embeddings.

    Args:
        embeddings: np.ndarray of shape (n_sentences, embedding_dim), L2-normalized.

    Returns:
        1D np.ndarray of length n_pairs = n_sentences * (n_sentences - 1) / 2
        containing cosine similarities in [-1, 1] (usually [0, 1] in practice).
    """
    n = embeddings.shape[0]
    if n == 0:
        raise ValueError("pairwise_similarities(): 'embeddings' is empty.")

    # For a single sentence, define similarity as 1.0 by convention.
    if n == 1:
        return np.array([1.0], dtype=float)

    sims = []
    for i, j in combinations(range(n), 2):
        sim = float(np.dot(embeddings[i], embeddings[j]))  # dot product = cosine (already normalized)
        sims.append(sim)

    return np.array(sims, dtype=float)


def similarity_features(sentences: List[str]) -> Dict[str, Any]:
    """
    High-level feature extractor for a group of sentences.

    Args:
        sentences: List of sentence strings.

    Returns:
        Dictionary with:
            - n_sentences : int
            - min_sim     : float
            - max_sim     : float
            - mean_sim    : float
            - std_sim     : float
            - all_sims    : np.ndarray (raw pairwise similarities)
    """
    embeddings = compute_embeddings(sentences)
    sims = pairwise_similarities(embeddings)

    return {
        "n_sentences": len(sentences),
        "min_sim": float(sims.min()),
        "max_sim": float(sims.max()),
        "mean_sim": float(sims.mean()),
        "std_sim": float(sims.std()),
        "all_sims": sims,
    }
