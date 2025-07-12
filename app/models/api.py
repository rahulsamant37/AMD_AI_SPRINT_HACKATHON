"""
API request and response models

Contains Pydantic models for API endpoint requests and responses.
"""

from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime
import uuid


class AttendeeModel(BaseModel):
    """Attendee model for input requests - matches JSON format"""
    email: str = Field(..., description="Email address of the attendee")


class ScheduleMeetingRequest(BaseModel):
    """API request model for scheduling meetings - exactly matches 1_Input_Request.json format"""
    Request_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique request identifier")
    Datetime: str = Field(..., description="Request datetime in format 'DD-MM-YYYYTHH:MM:SS'")
    Location: Optional[str] = Field(None, description="Meeting location")
    From: str = Field(..., description="Organizer email address")
    Attendees: List[AttendeeModel] = Field(..., description="List of meeting attendees")
    Subject: str = Field(..., min_length=1, max_length=200, description="Meeting subject/title")
    EmailContent: str = Field(..., description="Meeting description or email content")
    
    # Optional legacy fields for backward compatibility
    title: Optional[str] = Field(None, description="Legacy: Meeting title (will map to Subject)")
    description: Optional[str] = Field(None, description="Legacy: Meeting description (will map to EmailContent)")
    duration_minutes: Optional[int] = Field(None, ge=15, le=480, description="Legacy: Duration in minutes")
    organizer: Optional[Dict[str, str]] = Field(None, description="Legacy: Meeting organizer details")
    participants: Optional[List[Dict[str, str]]] = Field(None, description="Legacy: Additional participants")
    priority: Optional[str] = Field("medium", description="Legacy: Meeting priority: low, medium, high, urgent")
    preferred_days: Optional[List[str]] = Field(None, description="Legacy: Organizer's preferred days")
    user_preferences: Optional[Dict[str, Any]] = Field(None, description="Legacy: Organizer's scheduling preferences")
    
    @validator('priority')
    def validate_priority(cls, v):
        if v is not None:
            valid_priorities = ["low", "medium", "high", "urgent"]
            if v not in valid_priorities:
                raise ValueError(f"Priority must be one of: {valid_priorities}")
        return v
    
    @validator('Datetime')
    def validate_datetime_format(cls, v):
        """Validate datetime format matches DD-MM-YYYYTHH:MM:SS"""
        try:
            datetime.strptime(v, "%d-%m-%YT%H:%M:%S")
        except ValueError:
            raise ValueError("Datetime must be in format 'DD-MM-YYYYTHH:MM:SS' (e.g., '09-07-2025T12:34:55')")
        return v


class ProcessedMeetingInput(BaseModel):
    """Processed input model - exactly matches 2_Processed_Input.json format"""
    Request_id: str = Field(..., description="Unique request identifier")
    Datetime: str = Field(..., description="Original request datetime in format 'DD-MM-YYYYTHH:MM:SS'")
    Location: Optional[str] = Field(None, description="Meeting location")
    From: str = Field(..., description="Organizer email address")
    Attendees: List[AttendeeModel] = Field(..., description="List of meeting attendees")
    Subject: str = Field(..., description="Meeting subject/title")
    EmailContent: str = Field(..., description="Meeting description or email content")
    Start: str = Field(..., description="Processed start date range in ISO format with timezone (YYYY-MM-DDTHH:MM:SS+05:30)")
    End: str = Field(..., description="Processed end date range in ISO format with timezone (YYYY-MM-DDTHH:MM:SS+05:30)")
    Duration_mins: str = Field(..., description="Extracted duration in minutes as string")
    
    @validator('Start', 'End')
    def validate_iso_format(cls, v):
        """Validate ISO datetime format with timezone"""
        try:
            # Check if it matches the expected format with timezone
            if not v.endswith('+05:30'):
                raise ValueError("Datetime must include timezone '+05:30'")
            datetime.fromisoformat(v.replace('+05:30', '+0530'))
        except ValueError:
            raise ValueError("Datetime must be in ISO format with timezone (YYYY-MM-DDTHH:MM:SS+05:30)")
        return v


class CalendarEventModel(BaseModel):
    """Calendar event model for output - matches event structure in 3_Output_Event.json"""
    StartTime: str = Field(..., description="Event start time in ISO format with timezone (YYYY-MM-DDTHH:MM:SS+05:30)")
    EndTime: str = Field(..., description="Event end time in ISO format with timezone (YYYY-MM-DDTHH:MM:SS+05:30)")
    NumAttendees: int = Field(..., description="Number of attendees")
    Attendees: List[str] = Field(..., description="List of attendee emails or 'SELF' for personal events")
    Summary: str = Field(..., description="Event summary/title")
    
    @validator('StartTime', 'EndTime')
    def validate_event_time_format(cls, v):
        """Validate event time format with timezone"""
        try:
            if not v.endswith('+05:30'):
                raise ValueError("Event time must include timezone '+05:30'")
            datetime.fromisoformat(v.replace('+05:30', '+0530'))
        except ValueError:
            raise ValueError("Event time must be in ISO format with timezone (YYYY-MM-DDTHH:MM:SS+05:30)")
        return v


class AttendeeCalendarModel(BaseModel):
    """Attendee calendar model with events"""
    email: str = Field(..., description="Attendee email address")
    events: List[CalendarEventModel] = Field(..., description="List of calendar events")


class MeetingOutputEvent(BaseModel):
    """Meeting output event model - exactly matches 3_Output_Event.json format"""
    Request_id: str = Field(..., description="Original request identifier")
    Datetime: str = Field(..., description="Original request datetime in format 'DD-MM-YYYYTHH:MM:SS'")
    Location: Optional[str] = Field(None, description="Meeting location")
    From: str = Field(..., description="Organizer email address")
    Attendees: List[AttendeeCalendarModel] = Field(..., description="Attendees with their calendar events")
    Subject: str = Field(..., description="Meeting subject/title")
    EmailContent: str = Field(..., description="Meeting description or email content")
    EventStart: str = Field(..., description="Final scheduled event start time in ISO format with timezone (YYYY-MM-DDTHH:MM:SS+05:30)")
    EventEnd: str = Field(..., description="Final scheduled event end time in ISO format with timezone (YYYY-MM-DDTHH:MM:SS+05:30)")
    Duration_mins: str = Field(..., description="Event duration in minutes as string")
    MetaData: Dict[str, Any] = Field(default_factory=dict, description="Metadata containing communication details, agent processing info, or other contextual data")
    
    @validator('EventStart', 'EventEnd')
    def validate_event_datetime_format(cls, v):
        """Validate final event datetime format with timezone"""
        try:
            if not v.endswith('+05:30'):
                raise ValueError("Event datetime must include timezone '+05:30'")
            datetime.fromisoformat(v.replace('+05:30', '+0530'))
        except ValueError:
            raise ValueError("Event datetime must be in ISO format with timezone (YYYY-MM-DDTHH:MM:SS+05:30)")
        return v


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    services: Dict[str, bool]
    agent_tools_count: Optional[int] = None
    config: Optional[Dict[str, Any]] = None
    timestamp: str
    error: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standard error response model"""
    detail: str
    error_code: Optional[str] = None
    timestamp: Optional[str] = None


class MeetingProposalResponse(BaseModel):
    """Meeting proposal API response"""
    success: bool
    proposal_id: Optional[str] = None
    suggested_slots: Optional[List[Dict[str, Any]]] = None
    reasoning: Optional[str] = None
    agent_message: Optional[str] = None
    error: Optional[str] = None
    # Include processed input and output event for full workflow
    processed_input: Optional[ProcessedMeetingInput] = None
    output_event: Optional[MeetingOutputEvent] = None


class ProposalStatusResponse(BaseModel):
    """Proposal status API response"""
    proposal_id: str
    status: str
    meeting_title: str
    participants: List[str]
    suggested_slots: List[Dict[str, Any]]
    reasoning: str
    created_at: str
    # Include full event data
    output_event: Optional[MeetingOutputEvent] = None


class CalendarAvailabilityResponse(BaseModel):
    """Calendar availability API response"""
    success: bool
    availability_data: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None


# Legacy support models for backward compatibility
class LegacyScheduleMeetingRequest(BaseModel):
    """Legacy API request model for backward compatibility"""
    title: str = Field(..., min_length=1, max_length=200, description="Meeting title")
    description: str = Field("", max_length=1000, description="Meeting description")
    duration_minutes: int = Field(30, ge=15, le=480, description="Duration in minutes")
    organizer: Optional[Dict[str, str]] = Field(None, description="Meeting organizer details")
    participants: List[Dict[str, str]] = Field(default_factory=list, description="Additional participants")
    priority: str = Field("medium", description="Meeting priority: low, medium, high, urgent")
    preferred_days: List[str] = Field(default_factory=list, description="Organizer's preferred days")
    user_preferences: Optional[Dict[str, Any]] = Field(None, description="Organizer's scheduling preferences")
    
    @validator('priority')
    def validate_priority(cls, v):
        valid_priorities = ["low", "medium", "high", "urgent"]
        if v not in valid_priorities:
            raise ValueError(f"Priority must be one of: {valid_priorities}")
        return v 
