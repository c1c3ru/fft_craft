import re

def apply_phrases(text, phrase_map):
    """Replace known English phrases with PT-BR ones, longest-first so
    longer matches win over their substrings."""
    for eng in sorted(phrase_map, key=len, reverse=True):
        if eng in text:
            text = text.replace(eng, phrase_map[eng])
    return text
