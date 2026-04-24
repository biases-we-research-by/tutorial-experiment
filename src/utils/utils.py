from src.utils.helper import *
import numpy as np


def clean_generated_text(text, model):
    family = MODEL_FAMILY.get(model, "other")

    if family == "qwen":
        marker = "</think>"
        if marker in text:
            if "There is no publicly available information " not in text:
                cleaned = text.split(marker, 1)[1]
                return cleaned.strip(), "ok"
        else:
            return None, "no_pattern"

    if family == "llama":
        refusal_patterns = [
            "[There is no information",
            "[ I couldn't find any information",
            "I couldn't find any information on a person",
            "[Unfortunately, I couldn't find any information"
            "I couldn't find any information about a person "
            "[No information could be found about"
            "[ I do not have information on"
            "[No information could be found on "
        ]
        if any(p.lower() in text.lower() for p in refusal_patterns):
            return None, "filtered"
        return text, "ok"

    return text, "ok"


def extract_entropy_curve(example):
    return [t["entropy"] for t in example["token_details"]]


def pad_curves(curves):
    max_len = max(len(c) for c in curves)
    arr = np.full((len(curves), max_len), np.nan)
    for i, c in enumerate(curves):
        arr[i, :len(c)] = c
    return arr


def mean_and_std(curves):
    curves = [c for c in curves if len(c) > 0]
    if len(curves) == 0:
        return np.array([]), np.array([])
    padded = pad_curves(curves)
    return np.nanmean(padded, axis=0), np.nanstd(padded, axis=0)


def count_high_entropy(curves, threshold=2.0):
    return [sum(e > threshold for e in c) for c in curves]


def mean_length(curves):
    lengths = [len(c) for c in curves if len(c) > 0]
    if len(lengths) == 0:
        return 0, 0
    return np.mean(lengths), np.std(lengths)