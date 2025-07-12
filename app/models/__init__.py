"""
SchedulAI Data Models Package

This package contains all Pydantic models used throughout the application.
Models are organized by domain for better maintainability.
"""

from .meeting import (
    MeetingPriority,
    TimeSlot,
    MeetingRequest,
    MeetingProposal,
    CalendarEvent,
    EmailMessage,
    AvailabilityRequest,
    AvailabilityResponse
)

from .user import (
    Participant,
    UserPreferences
)

from .api import (
    ScheduleMeetingRequest,
    ProcessedMeetingInput,
    MeetingOutputEvent,
    CalendarEventModel,
    AttendeeCalendarModel,
    AttendeeModel,
    MeetingProposalResponse,
    ProposalStatusResponse,
    CalendarAvailabilityResponse,
    LegacyScheduleMeetingRequest,
    HealthResponse,
    ErrorResponse
)

from .agent import (
    FunctionCall,
    ToolCall,
    AgentResponse,
    AgentAction
)

__all__ = [
    # Meeting models
    "MeetingPriority",
    "TimeSlot", 
    "MeetingRequest",
    "MeetingProposal",
    "CalendarEvent",
    "EmailMessage",
    "AvailabilityRequest",
    "AvailabilityResponse",
    
    # User models
    "Participant",
    "UserPreferences",
    
    # API models
    "ScheduleMeetingRequest",
    "ProcessedMeetingInput",
    "MeetingOutputEvent",
    "CalendarEventModel",
    "AttendeeCalendarModel",
    "AttendeeModel",
    "MeetingProposalResponse",
    "ProposalStatusResponse",
    "CalendarAvailabilityResponse",
    "LegacyScheduleMeetingRequest",
    "HealthResponse",
    "ErrorResponse",
    
    # Agent models
    "FunctionCall",
    "ToolCall", 
    "AgentResponse",
    "AgentAction"
] 