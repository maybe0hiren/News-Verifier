from .context_segmenter import load_model, group_paragraph_graph_adjacent

_model = load_model()

def segmentation(paragraph: str):
    """Return only final segments (plain text)."""
    result = group_paragraph_graph_adjacent(paragraph, model=_model)
    return [" ".join(ctx["sentences"]) for ctx in result["contexts"]]


def segmentation_with_details(paragraph: str):
    """Return full segmentation details."""
    result = group_paragraph_graph_adjacent(paragraph, model=_model)
    segments = [" ".join(ctx["sentences"]) for ctx in result["contexts"]]
    result["segments"] = segments
    return result


def getPrimaryCaption(segs):
    return segs[0]

if __name__ == "__main__":
    print("=== ML Context Segmentation ===")
    print("Enter/paste a paragraph below:\n")
    para = input()

    segs = segmentation(para)
    print("\n=== Segments Detected ===")
    for i, s in enumerate(segs, 1):
        print(f"\nSegment {i}: {s}")
    print(getPrimaryCaption(segs))