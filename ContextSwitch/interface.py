import re
import sys
import os
folder_parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if folder_parent_path not in sys.path:
    sys.path.insert(0, folder_parent_path)
from ContextSwitch.switchDetection import ContextSwitchDetector


def segmentation(paragraph):
    detector = ContextSwitchDetector()
    sentences = [s.strip() for s in re.split(r'(?<=[.!?]) +', paragraph) if s.strip()]
    segments = []
    start = 0

    for i in range(len(sentences) - 1):
        pair_text = sentences[i] + " " + sentences[i+1]
        result = detector.predict(pair_text)
        if result['has_context_switch']:
            segment = " ".join(sentences[start:i+1])
            segments.append(segment)
            start = i + 1

    segment_list = [seg for idx, seg in enumerate(segments, 1)]
    return segment_list
