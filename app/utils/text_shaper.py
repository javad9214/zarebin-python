import arabic_reshaper
from bidi.algorithm import get_display

def shape_text(text: str) -> str:
    if not text:
        return ""
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)
