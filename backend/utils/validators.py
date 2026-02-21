import os
from typing import Tuple

ALLOWED_EXTENSIONS = {".mp4", ".mov", ".webm"}
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB

def validate_video_file(filename: str, file_size: int) -> Tuple[bool, str]:
    """Validate video file extension and size"""
    
    # Check extension
    file_ext = os.path.splitext(filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        return False, f"Invalid file format. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
    
    # Check size
    if file_size > MAX_FILE_SIZE:
        return False, f"File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024)}MB"
    
    return True, "Valid"
