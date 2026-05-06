import os
import time
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler

# OUTPUT_DIR = Path("/home/javad/zarebin/zarebin-python/output")
OUTPUT_DIR = Path("/home/sadathosseini/JAVAD/zarebin/zarebin-python/output")
MAX_AGE_SECONDS = 18000  # 1 hour
CLEANUP_INTERVAL_MINUTES = 5

def delete_expired_files():
    """Delete PDF files older than 1 hour from output directory"""
    try:
        if not OUTPUT_DIR.exists():
            return
        
        now = time.time()
        deleted_count = 0
        
        for file_path in OUTPUT_DIR.glob("*.pdf"):
            if file_path.is_file():
                file_age = now - file_path.stat().st_mtime
                if file_age > MAX_AGE_SECONDS:
                    file_path.unlink()
                    deleted_count += 1
                    print(f"Deleted expired file: {file_path.name}")
        
        if deleted_count > 0:
            print(f"Cleanup completed: {deleted_count} files deleted")
            
    except Exception as e:
        print(f"Cleanup error: {e}")

# Create scheduler instance
cleanup_scheduler = BackgroundScheduler()
cleanup_scheduler.add_job(
    delete_expired_files,
    'interval',
    minutes=CLEANUP_INTERVAL_MINUTES,
    id='cleanup_job'
)
