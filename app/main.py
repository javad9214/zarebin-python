from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="PDF Generator Service")


# Start cleanup scheduler on startup
@app.on_event("startup")
async def startup_event():
    cleanup_scheduler.start()

# Stop scheduler on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    cleanup_scheduler.shutdown()

app.include_router(router)
