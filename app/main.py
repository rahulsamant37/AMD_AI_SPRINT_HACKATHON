"""
SchedulAI FastAPI Application

Main application entry point with clean layered architecture.
"""

from fastapi import FastAPI
import uvicorn

from app.config import config
from app.core.logging import setup_logging
from app.api.middleware import setup_middleware
from app.api.routes import create_api_router

# Setup logging
logger = setup_logging(
    app_name="scheduleai",
    log_level=config.LOG_LEVEL,
    log_to_file=True
)


def create_app() -> FastAPI:
    """
    Application factory pattern
    
    Returns:
        Configured FastAPI application
    """
    
    logger.info("Creating SchedulAI FastAPI application...")
    
    # Create FastAPI app
    app = FastAPI(
        title="SchedulAI API",
        description="Autonomous Meeting Booking Agent with vLLM DeepSeek AI Integration",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Setup middleware
    setup_middleware(app)
    
    # Include routers
    api_router = create_api_router()
    app.include_router(api_router)
    
    logger.info("SchedulAI application created successfully")
    return app


# Create app instance
app = create_app()


def main():
    """Main entry point for the application"""
    
    logger.info("Starting SchedulAI FastAPI Server...")
    logger.info(f"API will be available at: http://{config.API_HOST}:{config.API_PORT}")
    logger.info(f"Swagger UI Documentation: http://{config.API_HOST}:{config.API_PORT}/docs")
    logger.info(f"ReDoc Documentation: http://{config.API_HOST}:{config.API_PORT}/redoc")
    logger.info(f"Debug mode: {config.DEBUG}")
    logger.info(f"Log level: {config.LOG_LEVEL}")
    
    # Validate configuration
    logger.info("Validating configuration...")
    missing_configs = config.validate_required_config()
    if missing_configs:
        logger.error(f"Configuration validation failed. Missing: {', '.join(missing_configs)}")
        return 1
    logger.info("Configuration validated successfully")
    
    logger.info("Initializing FastAPI application...")
    
    try:
        # Run the server
        uvicorn.run(
            "app.main:app",
            host=config.API_HOST,
            port=config.API_PORT,
            reload=False,  # Disable reload for production
            log_level=config.LOG_LEVEL.lower()
        )
        return 0
        
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main()) 