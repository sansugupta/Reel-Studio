from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict

class RateLimiter:
    def __init__(self, max_requests: int = 5, window_minutes: int = 10):
        self.max_requests = max_requests
        self.window = timedelta(minutes=window_minutes)
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if client is allowed to make a request"""
        now = datetime.now()
        
        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.window
        ]
        
        # Check limit
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        
        # Add new request
        self.requests[client_id].append(now)
        return True

# Global rate limiter instance
rate_limiter = RateLimiter()
