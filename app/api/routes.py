from fastapi import APIRouter, HTTPException
from app.schemas.car_inspection import CarInspectionSchema
from app.services.pdf_generator import generate_pdf, generate_pdf_api
import uuid
import os
from pathlib import Path
from datetime import datetime

router = APIRouter()

OUTPUT_DIR = Path("/home/javad/zarebin/zarebin-python/output")
# OUTPUT_DIR = Path("/home/sadathosseini/JAVAD/zarebin/zarebin-python/output")

@router.post("/generate")
async def generate_pdf_endpoint(data: CarInspectionSchema):
    """Generate PDF and return download URL"""
    # Generate unique filename
    filename = f"inspection_{uuid.uuid4().hex[:8]}_{int(datetime.now().timestamp())}.pdf"
    output_path = OUTPUT_DIR / filename
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
    
    # Generate PDF with dynamic filename
    try:
        # اول باید دیکشنری از data بسازیم
        data_dict = data.dict()
        
        # کپی از generate_pdf می‌سازیم که فایل‌نیم دلخواه بپذیرد
        from io import BytesIO
        from pypdf import PdfReader, PdfWriter
        from reportlab.pdfgen import canvas
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from app.services.pdf_generator import (
            TEMPLATE_PDF, FONT_PATH, FONT_SIZE, 
            FIELD_POSITIONS, BOOLEAN_POSITIONS,
            persian_blue, RED, shape_text
        )
        import logging
        
        pdfmetrics.registerFont(TTFont("FontBold", str(FONT_PATH)))
        
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
                value = data_dict.get(field)
                logging.info("field=%s value=%s", field, value)
                if value is None:
                    continue

                text = shape_text(str(value))
                c.drawString(x, y, text)

            # draw boolean X marks
            c.setFillColor(RED)
            c.setFont("Helvetica-Bold", 100)
            for field, (x, y) in BOOLEAN_POSITIONS.items():
                value = data_dict.get(field)
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
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")
    
    # Return download URL
    return {
        "status": "success",
        "message": "PDF generated successfully",
        "download_url": f"/download/{filename}",
        "filename": filename,
        "expires_in": "1 hour",
        "file_size": os.path.getsize(output_path) if os.path.exists(output_path) else 0
    }


@router.get("/download/{filename}")
async def download_file(filename: str):
    """
    Download a PDF file from output directory.
    Files older than 1 hour will be rejected.
    """
    # Security: only allow PDF files
    if not filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    filepath = OUTPUT_DIR / filename
    
    # Check if file exists
    if not filepath.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Check if file is expired (older than 1 hour)
    import time
    file_age = time.time() - os.path.getmtime(filepath)
    if file_age > 3600:  # 1 hour in seconds
        # Delete expired file immediately
        try:
            filepath.unlink()
        except:
            pass
        raise HTTPException(status_code=410, detail="File has expired (older than 1 hour)")
    
    # Return file for download
    from fastapi.responses import FileResponse
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type='application/pdf'
    )
