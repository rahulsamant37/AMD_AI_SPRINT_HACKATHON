"""
Logging configuration for SchedulAI

Provides centralized logging setup and utilities.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional


def setup_logging(
    app_name: str = "scheduleai",
    log_level: str = "INFO", 
    log_to_file: bool = True,
    log_dir: str = "logs"
) -> logging.Logger:
    """
    Setup centralized logging configuration
    
    Args:
        app_name: Name of the application
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_to_file: Whether to write logs to file
        log_dir: Directory for log files
        
    Returns:
        Configured logger instance
    """
    
    # Create logs directory
    if log_to_file:
        log_path = Path(log_dir)
        log_path.mkdir(exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler
    if log_to_file:
        file_handler = logging.handlers.RotatingFileHandler(
            log_path / f"{app_name}.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Create and return app logger
    app_logger = logging.getLogger(app_name)
    app_logger.info(f"Logging configured for {app_name} - Level: {log_level}")
    
    return app_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module
    
    Args:
        name: Logger name (usually module name)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


# Pre-configured loggers for common components
api_logger = get_logger("scheduleai.api")
agent_logger = get_logger("scheduleai.agent") 
google_logger = get_logger("scheduleai.google")
config_logger = get_logger("scheduleai.config") 