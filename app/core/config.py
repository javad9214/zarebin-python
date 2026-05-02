from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

TEMPLATE_PDF = BASE_DIR / "templates" / "bishomare.pdf"
FONT_PATH = BASE_DIR / "fonts" / "BTitrBd.ttf"
OUTPUT_DIR = BASE_DIR / "output"
