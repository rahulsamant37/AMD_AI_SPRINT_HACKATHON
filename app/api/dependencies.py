"""
FastAPI Dependencies

Provides dependency injection for services and utilities.
"""

from functools import lru_cache
from fastapi import Depends, HTTPException
from typing import Optional

from app.services.agent_service import SchedulingAgent
from app.services.google_service import GoogleService
from app.core.logging import get_logger
from app.core.exceptions import AgentException, GoogleServiceException

logger = get_logger(__name__)

# Global service instances
_agent_service: Optional[SchedulingAgent] = None
_google_service: Optional[GoogleService] = None


def get_agent_service() -> SchedulingAgent:
    """
    Dependency to get or create the scheduling agent service
    
    Returns:
        SchedulingAgent instance
        
    Raises:
        HTTPException: If agent initialization fails
    """
    global _agent_service
    
    if _agent_service is None:
        try:
            logger.info("Initializing SchedulAI Agent...")
            _agent_service = SchedulingAgent()
            logger.info("SchedulAI Agent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize SchedulAI Agent: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Agent initialization failed: {str(e)}"
            )
    
    return _agent_service


def get_google_service() -> GoogleService:
    """
    Dependency to get or create the Google service
    
    Returns:
        GoogleService instance
        
    Raises:
        HTTPException: If Google service initialization fails
    """
    global _google_service
    
    if _google_service is None:
        try:
            logger.info("Initializing Google Service...")
            _google_service = GoogleService()
            logger.info("Google Service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Google Service: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Google service initialization failed: {str(e)}"
            )
    
    return _google_service


@lru_cache()
def get_settings():
    """
    Dependency to get application settings
    
    Returns:
        Configuration settings
    """
    from app.config import config
    return config


def reset_services():
    """Reset service instances (useful for testing)"""
    global _agent_service, _google_service
    _agent_service = None
    _google_service = None 