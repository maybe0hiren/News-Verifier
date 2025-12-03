# Comparison/demo_same_context.py

from .same_context_baseline import is_same_context


def demo():
    same_example = [
        "India launched a new lunar mission on Sunday.",
        "The spacecraft aims to explore the Moon's south pole region.",
        "The mission marks India's third attempt at a soft landing on the lunar surface.",
    ]

    diff_example = [
        "The stock market fell sharply today amid global uncertainty.",
        "Heavy rainfall in Kerala has caused severe flooding in several districts.",
        "Scientists announced a major breakthrough in quantum computing.",
    ]

    print("=== SAME CONTEXT EXAMPLE ===")
    same, details = is_same_context(same_example)
    print("Same context? ->", same)
    print("Details:", {k: v for k, v in details.items() if k != "all_sims"})
    print()

    print("=== DIFFERENT CONTEXT EXAMPLE ===")
    same, details = is_same_context(diff_example)
    print("Same context? ->", same)
    print("Details:", {k: v for k, v in details.items() if k != "all_sims"})


if __name__ == "__main__":
    demo()
