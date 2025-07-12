"""
Custom exceptions for SchedulAI

Defines application-specific exceptions for better error handling.
"""

from typing import Optional, Dict, Any


class ScheduleAIException(Exception):
    """Base exception for SchedulAI application"""
    
    def __init__(
        self, 
        message: str, 
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class AgentException(ScheduleAIException):
    """Exception raised by AI agent operations"""
    pass


class GoogleServiceException(ScheduleAIException):
    """Exception raised by Google API operations"""
    pass


class ConfigurationException(ScheduleAIException):
    """Exception raised by configuration issues"""
    pass


class ValidationException(ScheduleAIException):
    """Exception raised by data validation errors"""
    pass


class AuthenticationException(ScheduleAIException):
    """Exception raised by authentication issues"""
    pass


class CalendarException(GoogleServiceException):
    """Exception raised by Google Calendar operations"""
    pass


class EmailException(GoogleServiceException):
    """Exception raised by Gmail operations"""
    pass 