# Comparison/__init__.py

"""
Comparison package

Responsible for sentence-level and group-level semantic comparisons.

Public API (for other modules):

- from Comparison import is_same_context
- from Comparison import similarity_features

These functions are implemented in:
- context_features.py
- same_context_baseline.py
"""

from .context_features import similarity_features
from .same_context_baseline import is_same_context

__all__ = [
    "similarity_features",
    "is_same_context",
]
