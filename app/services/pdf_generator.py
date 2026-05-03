from io import BytesIO
from pathlib import Path
from datetime import datetime
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

from app.core.config import TEMPLATE_PDF, FONT_PATH, OUTPUT_DIR
from app.utils.text_shaper import shape_text
import logging

logging.basicConfig(level=logging.INFO)

pdfmetrics.registerFont(TTFont("FontBold", str(FONT_PATH)))
persian_blue = colors.HexColor("#10246B")
RED = colors.red

# مختصات‌ها (اینجا تنظیم کن)
FIELD_POSITIONS = {
    # "fullName": (x, y),
    "fullName": (350, 5450),
    "phoneNumber": (300, 5270),
    "carName": (3100, 4700),
    "carModel": (3600, 4700),
    "chassisNumber": (1600, 4700),
    "plateNumber": (300, 4900),
    "inspectionDate": (350, 5750),
    "expertDescription": (350,5550),
}

BOOLEAN_POSITIONS = {
    "frontBumper": (1600, 4500),
    "hood": (1909, 4015),
    "frontRightFender": (1600, 4300),
    "frontRightDoor": (1909, 3496),
    "rearRightDoor": (1909, 3126),
    "rearLeftDoor": (1909, 3319),
    "rearRightFender": (1600, 4000),
    "trunk": (1909, 3835),
    "rearLeftFender": (3600, 4100),
    "frontLeftDoor": (1909, 3666),
    "frontLeftFender": (3600, 3600),
    "roof": (1600, 3400),
    "rearBumper": (1600, 3300),
    "chassis": (1600, 3200),
}

FONT_SIZE = 90  

def generate_pdf(data: dict) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

    reader = PdfReader(str(TEMPLATE_PDF))
    writer = PdfWriter()

    for page in reader.pages:
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=(width, height))
        c.setFont("FontBold", FONT_SIZE)
        c.setFillColor(persian_blue)
        # draw normal text fields
        for field, (x, y) in FIELD_POSITIONS.items():
            value = data.get(field)
            logging.info("field=%s value=%s", field, value)
            if value is None:
                continue

            # # تبدیل تاریخ به رشته
            # if isinstance(value, datetime):
            #     value = value.strftime("%Y-%m-%d %H:%M")

            text = shape_text(str(value))
            c.drawString(x, y, text)

        # draw boolean X marks
        c.setFillColor(colors.red)
        c.setFont("Helvetica-Bold", 100)
        for field, (x, y) in BOOLEAN_POSITIONS.items():
            value = data.get(field)
            logging.info("bool-field=%s value=%s", field, value)
            if value is True:
                c.drawString(x, y, "X")

        c.save()
        packet.seek(0)

        overlay_pdf = PdfReader(packet)
        page.merge_page(overlay_pdf.pages[0])
        writer.add_page(page)

    output_path = OUTPUT_DIR / f"inspection_{int(datetime.now().timestamp())}.pdf"
    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path
