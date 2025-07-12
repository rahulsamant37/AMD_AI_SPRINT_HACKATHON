"""
API Routes Package

Contains all FastAPI route definitions organized by functionality.
"""

from fastapi import APIRouter
from .meetings import router as meetings_router
from .health import router as health_router
from .calendar import router as calendar_router


def create_api_router() -> APIRouter:
    """
    Create and configure the main API router
    
    Returns:
        Configured APIRouter instance
    """
    api_router = APIRouter()
    
    # Include route modules
    api_router.include_router(health_router, tags=["Health"])
    api_router.include_router(meetings_router, prefix="/meetings", tags=["Meetings"])
    api_router.include_router(calendar_router, prefix="/calendar", tags=["Calendar"])
    
    return api_router


__all__ = ["create_api_router"] 