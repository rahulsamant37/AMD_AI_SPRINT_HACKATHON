"""
Validation utilities

Common validation functions used across the application.
"""

import re
from datetime import datetime
from typing import List, Tuple
from email_validator import validate_email, EmailNotValidError

from app.core.exceptions import ValidationException


def validate_email_list(emails: List[str]) -> List[str]:
    """
    Validate a list of email addresses
    
    Args:
        emails: List of email addresses to validate
        
    Returns:
        List of validated email addresses
        
    Raises:
        ValidationException: If any email is invalid
    """
    validated_emails = []
    
    for email in emails:
        try:
            valid_email = validate_email(email)
            validated_emails.append(valid_email.email)
        except EmailNotValidError as e:
            raise ValidationException(
                f"Invalid email address: {email} - {str(e)}",
                error_code="INVALID_EMAIL"
            )
    
    return validated_emails


def validate_datetime_range(start_time: str, end_time: str) -> Tuple[datetime, datetime]:
    """
    Validate a datetime range
    
    Args:
        start_time: Start datetime in ISO format
        end_time: End datetime in ISO format
        
    Returns:
        Tuple of (start_datetime, end_datetime)
        
    Raises:
        ValidationException: If datetime format is invalid or range is invalid
    """
    try:
        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)
    except ValueError as e:
        raise ValidationException(
            f"Invalid datetime format: {str(e)}",
            error_code="INVALID_DATETIME_FORMAT"
        )
    
    if start_dt >= end_dt:
        raise ValidationException(
            "Start time must be before end time",
            error_code="INVALID_DATETIME_RANGE"
        )
    
    # Check if times are in the past (optional warning)
    now = datetime.now()
    if end_dt < now:
        raise ValidationException(
            "End time cannot be in the past",
            error_code="DATETIME_IN_PAST"
        )
    
    return start_dt, end_dt


def validate_meeting_duration(duration_minutes: int) -> int:
    """
    Validate meeting duration
    
    Args:
        duration_minutes: Meeting duration in minutes
        
    Returns:
        Validated duration in minutes
        
    Raises:
        ValidationException: If duration is invalid
    """
    if not isinstance(duration_minutes, int):
        raise ValidationException(
            "Duration must be an integer",
            error_code="INVALID_DURATION_TYPE"
        )
    
    if duration_minutes < 15:
        raise ValidationException(
            "Meeting duration must be at least 15 minutes",
            error_code="DURATION_TOO_SHORT"
        )
    
    if duration_minutes > 480:  # 8 hours
        raise ValidationException(
            "Meeting duration cannot exceed 8 hours",
            error_code="DURATION_TOO_LONG"
        )
    
    return duration_minutes


def validate_priority(priority: str) -> str:
    """
    Validate meeting priority
    
    Args:
        priority: Meeting priority string
        
    Returns:
        Validated priority string
        
    Raises:
        ValidationException: If priority is invalid
    """
    valid_priorities = ["low", "medium", "high", "urgent"]
    
    if priority.lower() not in valid_priorities:
        raise ValidationException(
            f"Priority must be one of: {', '.join(valid_priorities)}",
            error_code="INVALID_PRIORITY"
        )
    
    return priority.lower()


def validate_participant_data(participant: dict) -> dict:
    """
    Validate participant data structure
    
    Args:
        participant: Participant data dictionary
        
    Returns:
        Validated participant data
        
    Raises:
        ValidationException: If participant data is invalid
    """
    required_fields = ["name", "email"]
    
    for field in required_fields:
        if field not in participant:
            raise ValidationException(
                f"Missing required field: {field}",
                error_code="MISSING_REQUIRED_FIELD"
            )
    
    # Validate email
    try:
        valid_email = validate_email(participant["email"])
        participant["email"] = valid_email.email
    except EmailNotValidError as e:
        raise ValidationException(
            f"Invalid email for participant {participant.get('name', 'Unknown')}: {str(e)}",
            error_code="INVALID_PARTICIPANT_EMAIL"
        )
    
    # Validate name
    if not participant["name"].strip():
        raise ValidationException(
            "Participant name cannot be empty",
            error_code="EMPTY_PARTICIPANT_NAME"
        )
    
    return participant 