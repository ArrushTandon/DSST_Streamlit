import re

def normalize(text: str):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text.split()
