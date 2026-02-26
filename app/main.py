from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.tts import router as tts_router
from app.config import settings
import os

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Asante Twi and African language TTS API wrapper for Ghana-NLP/Africa-TTS-UI.",
    version=settings.VERSION
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = os.path.join(os.getcwd(), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include API routes
app.include_router(tts_router, prefix=settings.API_PREFIX, tags=["TTS"])

@app.get("/")
async def serve_ui():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/health")
async def root():
    return {
        "status": "online",
        "message": f"Welcome to the {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
