from fastapi import APIRouter, HTTPException, Depends, Header
from services.analytics import analytics
import os

router = APIRouter()

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "admin123")

def verify_admin(authorization: str = Header(None)):
    if not authorization or authorization != f"Bearer {ADMIN_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

@router.get("/stats")
async def get_stats(authorized: bool = Depends(verify_admin)):
    return analytics.get_stats()
