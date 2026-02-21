import json
import os
from datetime import datetime
from pathlib import Path
from collections import defaultdict

ANALYTICS_FILE = "analytics.json"

class Analytics:
    def __init__(self):
        self.data = self._load_data()
    
    def _load_data(self):
        if os.path.exists(ANALYTICS_FILE):
            with open(ANALYTICS_FILE, 'r') as f:
                return json.load(f)
        return {
            "total_uploads": 0,
            "total_downloads": 0,
            "active_sessions": 0,
            "uploads_by_date": {},
            "current_processing": 0
        }
    
    def _save_data(self):
        with open(ANALYTICS_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def track_upload(self):
        self.data["total_uploads"] += 1
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in self.data["uploads_by_date"]:
            self.data["uploads_by_date"][today] = 0
        self.data["uploads_by_date"][today] += 1
        self._save_data()
    
    def track_download(self):
        self.data["total_downloads"] += 1
        self._save_data()
    
    def increment_processing(self):
        self.data["current_processing"] += 1
        self._save_data()
    
    def decrement_processing(self):
        self.data["current_processing"] = max(0, self.data["current_processing"] - 1)
        self._save_data()
    
    def get_stats(self):
        return self.data

analytics = Analytics()
