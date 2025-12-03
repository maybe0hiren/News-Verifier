# Comparison/same_context_baseline.py

from typing import List, Dict, Any, Tuple

from .context_features import similarity_features

# Default thresholds – tune them later with your data.
DEFAULT_MIN_SIM_THR = 0.65
DEFAULT_MEAN_SIM_THR = 0.75


def is_same_context(
    sentences: List[str],
    min_thr: float = DEFAULT_MIN_SIM_THR,
    mean_thr: float = DEFAULT_MEAN_SIM_THR,
) -> Tuple[bool, Dict[str, Any]]:
    """
    Decide whether all sentences fall in the same semantic context.

    Args:
        sentences: List of sentence strings.
        min_thr:   Minimum allowed pairwise similarity between the
                   most dissimilar pair of sentences.
        mean_thr:  Minimum allowed average pairwise similarity over
                   all sentence pairs.

    Returns:
        (same_context, details)

        same_context: bool, True if considered same context.
        details: dict with:
            - n_sentences
            - min_sim, max_sim, mean_sim, std_sim
            - min_thr, mean_thr
            - same_context
            - all_sims (removed by callers if they don't want raw sims)
    """
    if not sentences:
        raise ValueError("is_same_context(): 'sentences' list cannot be empty.")

    feats = similarity_features(sentences)

    # Rule:
    #   - If even the *lowest* similarity between any pair is high enough
    #   - AND the average similarity is high enough
    #   => treat as same context.
    same_ctx = (feats["min_sim"] >= min_thr) and (feats["mean_sim"] >= mean_thr)

    details: Dict[str, Any] = {
        **feats,
        "min_thr": float(min_thr),
        "mean_thr": float(mean_thr),
        "same_context": bool(same_ctx),
    }

    return same_ctx, details
