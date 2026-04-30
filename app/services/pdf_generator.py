from io import BytesIO
from pathlib import Path
from datetime import datetime
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from app.core.config import TEMPLATE_PDF, FONT_PATH, OUTPUT_DIR
from app.utils.text_shaper import shape_text

pdfmetrics.registerFont(TTFont("VazirBold", str(FONT_PATH)))

# مختصات‌ها (اینجا تنظیم کن)
FIELD_POSITIONS = {
    # "fullName": (x, y),
    "fullName": (350, 5450),
    "phoneNumber": (300, 5250),
    "carName": (3100, 4700),
    "carModel": (3600, 4700),
    "chassisNumber": (1500, 4700),
    "plateNumber": (300, 4900),
    "inspectionDate": (690, 6000),
    "expertDescription": (350,5750),
}

FONT_SIZE = 110  

def generate_pdf(data: dict) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

    reader = PdfReader(str(TEMPLATE_PDF))
    writer = PdfWriter()

    for page in reader.pages:
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=(width, height))
        c.setFont("VazirBold", FONT_SIZE)

        for field, (x, y) in FIELD_POSITIONS.items():
            value = data.get(field)
            if value is None:
                continue

            # تبدیل تاریخ به رشته
            if isinstance(value, datetime):
                value = value.strftime("%Y-%m-%d %H:%M")

            text = shape_text(str(value))
            c.drawString(x, y, text)

        c.save()
        packet.seek(0)

        overlay_pdf = PdfReader(packet)
        page.merge_page(overlay_pdf.pages[0])
        writer.add_page(page)

    output_path = OUTPUT_DIR / f"inspection_{int(datetime.now().timestamp())}.pdf"
    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path
