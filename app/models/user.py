"""
User and participant-related Pydantic models

Contains models for users, participants, and their preferences.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field


class Participant(BaseModel):
    """Represents a meeting participant"""
    name: str
    email: EmailStr
    timezone: str = "UTC"
    preferences: Optional[Dict[str, Any]] = {}
    role: str = "attendee"  # "organizer", "attendee", "optional"


class UserPreferences(BaseModel):
    """User scheduling preferences"""
    work_start_hour: int = 9
    work_end_hour: int = 18
    preferred_meeting_days: List[str] = ["monday", "tuesday", "wednesday", "thursday", "friday"]
    buffer_time_minutes: int = 15
    timezone: str = "UTC"
    lunch_break_start: Optional[int] = 12
    lunch_break_duration: int = 60
    no_meetings_before: Optional[int] = None
    no_meetings_after: Optional[int] = None
    max_meetings_per_day: int = 8 