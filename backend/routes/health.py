"""
Health check endpoints
"""
import os
import logging
from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["health"])
logger = logging.getLogger(__name__)

@router.get("/health")
async def health_check():
    """
    Check backend and agent availability
    """
    api_key_present = bool(os.getenv("GOOGLE_API_KEY"))

    status = "healthy" if api_key_present else "degraded"

    return {
        "status": status,
        "message": "Backend is operational" if api_key_present else "API key not configured",
        "services": {
            "api": "operational",
            "agent": "configured" if api_key_present else "not_configured"
        }
    }
