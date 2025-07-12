"""
FastAPI Middleware Configuration

Contains middleware setup for the application.
"""

import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.logging import get_logger
from app.core.exceptions import ScheduleAIException

logger = get_logger(__name__)


def setup_middleware(app: FastAPI) -> None:
    """
    Setup middleware for the FastAPI application
    
    Args:
        app: FastAPI application instance
    """
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify allowed origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        
        logger.info(f"{request.method} {request.url.path} - Started")
        
        # Log request details for debugging
        if logger.isEnabledFor(10):  # DEBUG level
            logger.debug(f"Request headers: {dict(request.headers)}")
            if request.method in ["POST", "PUT", "PATCH"]:
                body = await request.body()
                if body:
                    logger.debug(f"Request body: {body.decode()}")
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.3f}s"
        )
        
        return response
    
    # Exception handling middleware
    @app.exception_handler(ScheduleAIException)
    async def scheduleai_exception_handler(request: Request, exc: ScheduleAIException):
        logger.error(f"ScheduleAI exception: {exc.message}", exc_info=True)
        return JSONResponse(
            status_code=400,
            content={
                "detail": exc.message,
                "error_code": exc.error_code,
                "type": "ScheduleAI Error"
            }
        )
    
    # General exception handling
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "type": "Server Error"
            }
        ) 