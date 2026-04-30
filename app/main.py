from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="PDF Generator Service")

app.include_router(router)
