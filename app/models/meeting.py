"""
Meeting-related Pydantic models

Contains all models related to meetings, calendar events, and scheduling.
"""

from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from enum import Enum
import uuid

from .user import Participant


class MeetingPriority(str, Enum):
    """Meeting priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TimeSlot(BaseModel):
    """Represents a time slot with availability information"""
    start_time: datetime
    end_time: datetime
    available: bool = True
    timezone: str = "UTC"


class MeetingRequest(BaseModel):
    """Meeting request with organizer and participants"""
    title: str = Field(..., min_length=1, max_length=200, description="Meeting title")
    description: Optional[str] = Field("", max_length=1000, description="Meeting description")
    duration_minutes: int = Field(30, ge=15, le=480, description="Duration in minutes (15-480)")
    organizer: Participant = Field(..., description="Meeting organizer (the user making the request)")
    participants: List[Participant] = Field(default_factory=list, max_items=19, description="Additional meeting participants")
    priority: MeetingPriority = Field(MeetingPriority.MEDIUM, description="Meeting priority level")
    preferred_days: Optional[List[str]] = Field([], description="Organizer's preferred days of week")
    earliest_start: Optional[datetime] = Field(None, description="Earliest possible start time")
    latest_end: Optional[datetime] = Field(None, description="Latest possible end time")
    buffer_time_minutes: int = Field(15, ge=0, le=60, description="Buffer time between meetings")
    
    @validator('preferred_days')
    def validate_preferred_days(cls, v):
        if v:
            valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            for day in v:
                if day.lower() not in valid_days:
                    raise ValueError(f"Invalid day: {day}. Must be one of {valid_days}")
        return [day.lower() for day in v] if v else []
    
    @validator('organizer')
    def set_organizer_role(cls, v):
        if hasattr(v, 'role'):
            v.role = "organizer"
        return v
    
    def get_all_participants(self) -> List[Participant]:
        """Get all participants including organizer"""
        return [self.organizer] + self.participants
    
    def get_all_emails(self) -> List[str]:
        """Get all participant emails including organizer"""
        return [p.email for p in self.get_all_participants()]


class CalendarEvent(BaseModel):
    """Calendar event representation"""
    id: Optional[str] = None
    title: str
    description: Optional[str] = ""
    start_time: datetime
    end_time: datetime
    attendees: List[str] = []
    location: Optional[str] = ""
    timezone: str = "UTC"


class EmailMessage(BaseModel):
    """Email message representation"""
    to: List[str]
    subject: str
    body: str
    html_body: Optional[str] = None
    thread_id: Optional[str] = None


class AvailabilityRequest(BaseModel):
    """Request for checking availability"""
    start_date: datetime
    end_date: datetime
    participants: List[str] = []
    duration_minutes: int = 30


class AvailabilityResponse(BaseModel):
    """Response with availability data"""
    participant_email: str
    free_slots: List[TimeSlot]
    busy_slots: List[TimeSlot]


class MeetingProposal(BaseModel):
    """Meeting proposal with suggested time slots"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique proposal ID")
    meeting_request: MeetingRequest = Field(..., description="Original meeting request")
    suggested_slots: List[TimeSlot] = Field(..., description="AI-suggested time slots")
    reasoning: str = Field(..., description="AI reasoning for slot selection")
    confidence_scores: List[float] = Field(default_factory=list, description="Confidence scores for each slot")
    created_at: datetime = Field(default_factory=datetime.now, description="Proposal creation time")
    status: str = Field("pending", pattern="^(pending|confirmed|cancelled)$", description="Proposal status")
    
    @validator('confidence_scores')
    def validate_confidence_scores(cls, v, values):
        if 'suggested_slots' in values and v:
            if len(v) != len(values['suggested_slots']):
                raise ValueError("Number of confidence scores must match number of suggested slots")
        return v 