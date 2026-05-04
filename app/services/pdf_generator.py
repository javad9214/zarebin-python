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
import uuid

logging.basicConfig(level=logging.INFO)

pdfmetrics.registerFont(TTFont("FontBold", str(FONT_PATH)))
persian_blue = colors.HexColor("#10246B")
RED = colors.red

# مختصات‌ها
FIELD_POSITIONS = {
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

def generate_pdf(data: dict, output_filename: str = None) -> Path:
    """
    Generate PDF with data.
    
    Args:
        data: Dictionary containing form data
        output_filename: Optional custom filename (without .pdf extension)
    
    Returns:
        Path to generated PDF file
    """
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
    
    # Generate filename if not provided
    if output_filename is None:
        output_filename = f"inspection_{int(datetime.now().timestamp())}.pdf"
    elif not output_filename.endswith('.pdf'):
        output_filename += '.pdf'
    
    output_path = OUTPUT_DIR / output_filename

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

            text = shape_text(str(value))
            c.drawString(x, y, text)

        # draw boolean X marks
        c.setFillColor(RED)
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

    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path


def generate_pdf_api(payload, custom_filename: str = None):
    """
    Generate PDF from API payload.
    
    Args:
        payload: Pydantic model or dictionary
        custom_filename: Optional custom filename
    
    Returns:
        Dictionary with status and file info
    """
    # Convert payload to dict if it's a Pydantic model
    if hasattr(payload, 'dict'):
        data = payload.dict()
    else:
        data = payload
    
    # Generate filename if not provided
    if custom_filename is None:
        custom_filename = f"inspection_{uuid.uuid4().hex[:8]}_{int(datetime.now().timestamp())}.pdf"
    
    # Generate PDF
    path = generate_pdf(data, custom_filename)
    
    # Return download URL and info
    filename = path.name
    return {
        "status": "success",
        "message": "PDF generated successfully",
        "filePath": str(path),
        "download_url": f"/download/{filename}",
        "filename": filename,
        "expires_in": "1 hour"
    }
