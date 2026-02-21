import os
import time
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler

def cleanup_old_files():
    """Delete files older than 30 minutes"""
    current_time = time.time()
    max_age = 30 * 60  # 30 minutes
    
    for directory in ["temp_uploads", "temp_outputs"]:
        if not os.path.exists(directory):
            continue
            
        for item in Path(directory).iterdir():
            try:
                item_age = current_time - item.stat().st_mtime
                if item_age > max_age:
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        import shutil
                        shutil.rmtree(item)
                    print(f"Cleaned up: {item}")
            except Exception as e:
                print(f"Error cleaning {item}: {e}")

def start_cleanup_scheduler():
    """Start background scheduler for cleanup"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(cleanup_old_files, 'interval', minutes=5)
    scheduler.start()
    print("Cleanup scheduler started")
