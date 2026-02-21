from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from services.video_processor import process_video
from services.analytics import analytics
import uuid
import os
import aiofiles

router = APIRouter()

ALLOWED_EXTENSIONS = {".mp4", ".mov", ".webm"}
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB

@router.post("/upload")
async def upload_video(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file format. Use MP4, MOV, or WebM")
    
    # Generate unique session ID
    session_id = str(uuid.uuid4())
    upload_path = f"temp_uploads/{session_id}{file_ext}"
    
    # Save uploaded file
    try:
        async with aiofiles.open(upload_path, 'wb') as out_file:
            content = await file.read()
            
            # Check file size
            if len(content) > MAX_FILE_SIZE:
                raise HTTPException(status_code=400, detail="File too large. Max 200MB")
            
            await out_file.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
    # Track analytics
    analytics.track_upload()
    analytics.increment_processing()
    
    # Process video in background
    async def process_with_tracking(sid, path):
        try:
            process_video(sid, path)
        finally:
            analytics.decrement_processing()
    
    background_tasks.add_task(process_with_tracking, session_id, upload_path)
    
    return {
        "session_id": session_id,
        "message": "Upload successful. Processing started.",
        "status": "processing"
    }
