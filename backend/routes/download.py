from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/status/{session_id}")
async def check_status(session_id: str):
    output_dir = f"temp_outputs/{session_id}"
    
    if not os.path.exists(output_dir):
        return {"status": "processing"}
    
    # Check if all files exist
    expected_files = [
        "video_no_audio.mp4",
        "full_audio.mp3",
        "music_only.mp3",
        "vocals_only.mp3"
    ]
    
    files_ready = all(os.path.exists(f"{output_dir}/{f}") for f in expected_files)
    
    if files_ready:
        # Track downloads
        from services.analytics import analytics
        analytics.track_download()
        
        return {
            "status": "completed",
            "files": {
                "video_no_audio": f"/outputs/{session_id}/video_no_audio.mp4",
                "full_audio": f"/outputs/{session_id}/full_audio.mp3",
                "music_only": f"/outputs/{session_id}/music_only.mp3",
                "vocals_only": f"/outputs/{session_id}/vocals_only.mp3"
            }
        }
    
    return {"status": "processing"}
