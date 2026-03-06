# utils/text_cleaner.py
import re

def clean_text(s: str):
    s = s.strip()
    # normalize whitespace
    s = re.sub(r'\s+', ' ', s)
    return s