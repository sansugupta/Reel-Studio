from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from routes import upload, download, health, admin
from services.cleanup import start_cleanup_scheduler

app = FastAPI(title="Reel-Studio API")

# Get port from environment (Railway/Render)
PORT = int(os.getenv("PORT", 8000))

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
os.makedirs("temp_uploads", exist_ok=True)
os.makedirs("temp_outputs", exist_ok=True)

# Mount static files for downloads
app.mount("/outputs", StaticFiles(directory="temp_outputs"), name="outputs")

# Include routes
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(download.router, prefix="/api", tags=["download"])
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

# Start cleanup scheduler
start_cleanup_scheduler()

@app.get("/")
def root():
    return {"message": "Reel-Studio API is running"}
