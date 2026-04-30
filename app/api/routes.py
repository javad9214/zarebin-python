from fastapi import APIRouter
from app.schemas.car_inspection import CarInspectionSchema
from app.services.pdf_generator import generate_pdf

router = APIRouter()

@router.post("/generate")
def generate_pdf_api(payload: CarInspectionSchema):
    path = generate_pdf(payload.dict())
    return {"status": "ok", "filePath": str(path)}
