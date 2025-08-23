import re

def normalize_token(s: str) -> str:
    s = s.strip()
    s = re.sub(r'\s+', ' ', s)
    return s

def canonicalize_class(s: str) -> str:
    return normalize_token(s)

def canonicalize_method(s: str) -> str:
    return normalize_token(s)
