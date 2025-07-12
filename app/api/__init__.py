"""
API Layer Package

Contains FastAPI application, routes, middleware, and dependencies.
"""

from .dependencies import get_agent_service, get_google_service
from .middleware import setup_middleware

__all__ = [
    "get_agent_service",
    "get_google_service", 
    "setup_middleware"
] 