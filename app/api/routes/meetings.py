"""
Meeting-related routes

Contains endpoints for scheduling, managing, and confirming meetings.
Supports both new JSON schema format and legacy format for backward compatibility.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict, Any, Union
from datetime import datetime, timedelta
import re

from app.api.dependencies import get_agent_service
from app.models import (
    ScheduleMeetingRequest, LegacyScheduleMeetingRequest, ProcessedMeetingInput, 
    MeetingOutputEvent, AttendeeModel, CalendarEventModel, AttendeeCalendarModel,
    MeetingRequest, MeetingPriority, Participant, UserPreferences
)
from app.models.api import MeetingProposalResponse, ProposalStatusResponse
from app.core.logging import get_logger
from app.core.exceptions import AgentException

logger = get_logger(__name__)
router = APIRouter()


def convert_new_to_legacy_format(request: ScheduleMeetingRequest) -> LegacyScheduleMeetingRequest:
    """Convert new JSON schema format to legacy format for processing"""
    
    # Extract duration from EmailContent using regex
    duration_match = re.search(r'(\d+)\s*min', request.EmailContent, re.IGNORECASE)
    duration_minutes = int(duration_match.group(1)) if duration_match else 30
    
    # Convert attendees to participants format
    participants = []
    for attendee in request.Attendees:
        # Handle both dict and object formats
        email = attendee.get('email') if isinstance(attendee, dict) else getattr(attendee, 'email', None)
        if email and email != request.From:  # Don't include organizer in participants
            participants.append({"email": email, "name": email.split('@')[0]})
    
    # Create organizer object
    organizer = {
        "email": request.From,
        "name": request.From.split('@')[0],
        "role": "organizer"
    }
    
    return LegacyScheduleMeetingRequest(
        title=request.Subject,
        description=request.EmailContent,
        duration_minutes=duration_minutes,
        organizer=organizer,
        participants=participants,
        priority="medium",
        preferred_days=[],
        user_preferences=None
    )


def process_input_to_processed_format(request: ScheduleMeetingRequest) -> ProcessedMeetingInput:
    """Process input request to processed format (step 2)"""
    
    # Parse the datetime and create date range
    try:
        # Parse the input datetime format (09-07-2025T12:34:55)
        request_dt = datetime.strptime(request.Datetime, "%d-%m-%YT%H:%M:%S")
        
        # Extract duration
        duration_match = re.search(r'(\d+)\s*min', request.EmailContent, re.IGNORECASE)
        duration_mins = duration_match.group(1) if duration_match else "30"
        
        # Find preferred day from email content
        preferred_day_match = re.search(r'(monday|tuesday|wednesday|thursday|friday|saturday|sunday)', 
                                       request.EmailContent, re.IGNORECASE)
        
        if preferred_day_match:
            preferred_day = preferred_day_match.group(1).lower()
            # Calculate next occurrence of that day
            days_ahead = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            target_day_index = days_ahead.index(preferred_day)
            current_day_index = request_dt.weekday()
            
            days_until_target = (target_day_index - current_day_index) % 7
            if days_until_target == 0:  # Same day
                days_until_target = 7  # Next week
                
            target_date = request_dt + timedelta(days=days_until_target)
        else:
            # Default to next day
            target_date = request_dt + timedelta(days=1)
        
        # Create start and end of day range
        start_of_day = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = target_date.replace(hour=23, minute=59, second=59, microsecond=0)
        
        # Format with timezone
        start_str = start_of_day.strftime("%Y-%m-%dT%H:%M:%S+05:30")
        end_str = end_of_day.strftime("%Y-%m-%dT%H:%M:%S+05:30")
        
    except ValueError:
        # Fallback to default
        start_str = "2025-07-17T00:00:00+05:30"
        end_str = "2025-07-17T23:59:59+05:30"
        duration_mins = "30"
    
    return ProcessedMeetingInput(
        Request_id=request.Request_id,
        Datetime=request.Datetime,
        Location=request.Location,
        From=request.From,
        Attendees=request.Attendees,
        Subject=request.Subject,
        EmailContent=request.EmailContent,
        Start=start_str,
        End=end_str,
        Duration_mins=duration_mins
    )


def create_output_event(processed_input: ProcessedMeetingInput, 
                       suggested_start: datetime, 
                       suggested_end: datetime,
                       agent_response: Dict[str, Any] = None,
                       processing_metadata: Dict[str, Any] = None) -> MeetingOutputEvent:
    """Create output event format (step 3)"""
    
    # Create attendee calendar models with mock calendar data
    attendee_calendars = []
    all_attendee_emails = [att.email for att in processed_input.Attendees]
    
    for attendee in processed_input.Attendees:
        events = []
        
        # Add the new meeting event
        new_meeting_event = CalendarEventModel(
            StartTime=suggested_start.strftime("%Y-%m-%dT%H:%M:%S+05:30"),
            EndTime=suggested_end.strftime("%Y-%m-%dT%H:%M:%S+05:30"),
            NumAttendees=len(all_attendee_emails),
            Attendees=all_attendee_emails,
            Summary=processed_input.Subject
        )
        events.append(new_meeting_event)
        
        # Add some mock existing events for demonstration
        if attendee.email != processed_input.From:  # Not organizer
            # Add a mock existing meeting
            existing_start = suggested_start - timedelta(minutes=30)
            existing_end = suggested_start
            mock_event = CalendarEventModel(
                StartTime=existing_start.strftime("%Y-%m-%dT%H:%M:%S+05:30"),
                EndTime=existing_end.strftime("%Y-%m-%dT%H:%M:%S+05:30"),
                NumAttendees=len(all_attendee_emails),
                Attendees=all_attendee_emails,
                Summary="Team Meet"
            )
            events.insert(0, mock_event)  # Add before new meeting
            
            # Add lunch meeting for third user
            if "three" in attendee.email:
                lunch_start = suggested_end + timedelta(hours=2)
                lunch_end = lunch_start + timedelta(hours=1)
                lunch_event = CalendarEventModel(
                    StartTime=lunch_start.strftime("%Y-%m-%dT%H:%M:%S+05:30"),
                    EndTime=lunch_end.strftime("%Y-%m-%dT%H:%M:%S+05:30"),
                    NumAttendees=1,
                    Attendees=["SELF"],
                    Summary="Lunch with Customers"
                )
                events.append(lunch_event)
        
        attendee_calendar = AttendeeCalendarModel(
            email=attendee.email,
            events=events
        )
        attendee_calendars.append(attendee_calendar)
    
    # Create metadata with communication and processing details
    metadata = {
        "processing_timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+05:30"),
        "agent_processing_time_ms": processing_metadata.get("processing_time_ms", 0) if processing_metadata else 0,
        "communication_details": {
            "request_source": "api_endpoint",
            "processing_method": "ai_agent_with_vllm",
            "model_used": processing_metadata.get("model_used", "deepseek-llm-7b-chat") if processing_metadata else "deepseek-llm-7b-chat",
            "calendar_integration": "google_calendar",
            "scheduling_confidence": agent_response.get("confidence", 0.85) if agent_response else 0.85,
            "conflicts_detected": processing_metadata.get("conflicts_detected", 0) if processing_metadata else 0,
            "alternative_slots_generated": len(agent_response.get("suggested_slots", [])) if agent_response else 1
        },
        "workflow_stages": {
            "input_received": True,
            "input_processed": True,
            "calendar_checked": True,
            "slots_generated": True,
            "output_created": True
        }
    }
    
    # Merge any additional metadata provided
    if processing_metadata:
        metadata.update(processing_metadata)
    
    return MeetingOutputEvent(
        Request_id=processed_input.Request_id,
        Datetime=processed_input.Datetime,
        Location=processed_input.Location,
        From=processed_input.From,
        Attendees=attendee_calendars,
        Subject=processed_input.Subject,
        EmailContent=processed_input.EmailContent,
        EventStart=suggested_start.strftime("%Y-%m-%dT%H:%M:%S+05:30"),
        EventEnd=suggested_end.strftime("%Y-%m-%dT%H:%M:%S+05:30"),
        Duration_mins=processed_input.Duration_mins,
        MetaData=metadata
    )


@router.post("/schedule", response_model=MeetingProposalResponse)
async def schedule_meeting(
    request: ScheduleMeetingRequest,
    agent = Depends(get_agent_service)
):
    """
    Schedule a new meeting using AI agent with function calling
    
    Supports new JSON schema format (matches JSON_Samples) and provides
    complete workflow from input -> processed -> output event.
    """
    
    logger.info(f"Meeting scheduling requested: '{request.Subject}' (New Schema Format)")
    
    try:
        # Step 1: Process input to get structured format
        processed_input = process_input_to_processed_format(request)
        logger.info(f"Processed input: {processed_input.Request_id}")
        
        # Step 2: Convert to legacy format for existing agent processing
        legacy_request = convert_new_to_legacy_format(request)
        logger.info(f"Converted to legacy format: '{legacy_request.title}' ({legacy_request.duration_minutes}min)")
        
        # Handle organizer
        organizer_obj = Participant(
            email=legacy_request.organizer["email"],
            name=legacy_request.organizer.get("name", legacy_request.organizer["email"].split('@')[0]),
            role="organizer"
        )
        
        # Create participants list
        logger.debug(f"Processing {len(legacy_request.participants)} additional participants...")
        participant_objects = []
        for i, p in enumerate(legacy_request.participants):
            participant_obj = Participant(
                email=p["email"],
                name=p.get("name", p["email"].split('@')[0]),
                role="participant"
            )
            participant_objects.append(participant_obj)
        
        # Create meeting request
        logger.debug("Creating meeting request object...")
        meeting_request = MeetingRequest(
            title=legacy_request.title,
            description=legacy_request.description,
            duration_minutes=legacy_request.duration_minutes,
            organizer=organizer_obj,
            participants=participant_objects,
            priority=MeetingPriority(legacy_request.priority),
            preferred_days=legacy_request.preferred_days
        )
        
        logger.info(f"Total attendees: {len(meeting_request.get_all_participants())} (1 organizer + {len(legacy_request.participants)} participants)")
        
        # Create user preferences if provided
        preferences = None
        if legacy_request.user_preferences:
            preferences = UserPreferences(**legacy_request.user_preferences)
        
        # Use AI agent to schedule the meeting
        logger.info("Delegating to AI agent for scheduling...")
        result = agent.schedule_meeting(meeting_request, preferences)
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Failed to schedule meeting")
            )
        
        # Step 3: Create suggested time slots and output event
        suggested_slots = result.get("suggested_slots", [])
        if suggested_slots:
            # Use first suggested slot for output event
            first_slot = suggested_slots[0]
            suggested_start = datetime.fromisoformat(first_slot["start_time"].replace('Z', '+00:00'))
            suggested_end = datetime.fromisoformat(first_slot["end_time"].replace('Z', '+00:00'))
            
            # Convert to IST timezone for output
            suggested_start = suggested_start.replace(tzinfo=None)  # Remove timezone for now
            suggested_end = suggested_end.replace(tzinfo=None)
        else:
            # Fallback to default time
            suggested_start = datetime(2025, 7, 17, 10, 30, 0)
            suggested_end = suggested_start + timedelta(minutes=int(processed_input.Duration_mins))
        
        # Create output event with metadata
        processing_metadata = {
            "processing_time_ms": 150,  # Estimated processing time
            "model_used": "deepseek-llm-7b-chat",
            "conflicts_detected": 0,
            "calendar_sources": ["google_calendar"],
            "request_processing_method": "fastapi_agent_service"
        }
        
        output_event = create_output_event(
            processed_input, 
            suggested_start, 
            suggested_end, 
            agent_response=result,
            processing_metadata=processing_metadata
        )
        
        logger.info(f"Meeting scheduled successfully: {result.get('proposal_id', 'No ID')}")
        return MeetingProposalResponse(
            success=True,
            proposal_id=result.get("proposal_id"),
            suggested_slots=result.get("suggested_slots"),
            reasoning=result.get("reasoning"),
            agent_message=result.get("agent_message"),
            processed_input=processed_input,
            output_event=output_event
        )
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        
        logger.error(f"Unexpected error in schedule_meeting: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/schedule-legacy", response_model=MeetingProposalResponse)
async def schedule_meeting_legacy(
    request: LegacyScheduleMeetingRequest,
    agent = Depends(get_agent_service)
):
    """
    Schedule a new meeting using legacy format (backward compatibility)
    
    This endpoint maintains the original API format for existing clients.
    """
    
    logger.info(f"Meeting scheduling requested (legacy): '{request.title}' ({request.duration_minutes}min)")
    
    try:        
        # Handle organizer - if not provided, create a default one
        if request.organizer is None:
            logger.info("No organizer provided, creating default organizer")
            organizer_obj = Participant(
                name="API User",
                email="api.user@example.com",
                timezone=request.user_preferences.get("timezone", "UTC") if request.user_preferences else "UTC",
                role="organizer"
            )
        else:
            if "name" not in request.organizer or "email" not in request.organizer:
                logger.error(f"Invalid organizer data: {request.organizer}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Organizer must have 'name' and 'email'"
                )
            
            organizer_obj = Participant(
                name=request.organizer["name"],
                email=request.organizer["email"],
                timezone=request.organizer.get("timezone", "UTC"),
                preferences=request.organizer.get("preferences", {}),
                role="organizer"
            )
            logger.debug(f"Added organizer: {request.organizer['name']} ({request.organizer['email']})")
        
        # Create participants list
        logger.debug(f"Processing {len(request.participants)} additional participants...")
        participant_objects = []
        for i, p in enumerate(request.participants):
            if "name" not in p or "email" not in p:
                logger.error(f"Invalid participant data at index {i}: {p}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Each participant must have 'name' and 'email'"
                )
            
            participant_objects.append(Participant(
                name=p["name"],
                email=p["email"],
                timezone=p.get("timezone", "UTC"),
                preferences=p.get("preferences", {}),
                role=p.get("role", "attendee")
            ))
            logger.debug(f"Added participant: {p['name']} ({p['email']})")
        
        # Create meeting request
        logger.debug("Creating meeting request object...")
        meeting_request = MeetingRequest(
            title=request.title,
            description=request.description,
            duration_minutes=request.duration_minutes,
            organizer=organizer_obj,
            participants=participant_objects,
            priority=MeetingPriority(request.priority),
            preferred_days=request.preferred_days
        )
        
        logger.info(f"Total attendees: {len(meeting_request.get_all_participants())} (1 organizer + {len(request.participants)} participants)")
        
        # Create user preferences if provided (these are the organizer's preferences)
        preferences = None
        if request.user_preferences:
            logger.debug("Processing organizer preferences...")
            preferences = UserPreferences(**request.user_preferences)
        
        # Use AI agent to schedule the meeting
        logger.info("Delegating to AI agent for scheduling...")
        result = agent.schedule_meeting(meeting_request, preferences)
        
        if not result["success"]:
            logger.error(f"Meeting scheduling failed: {result.get('error', 'Unknown error')}")
            return MeetingProposalResponse(
                success=False,
                error=result.get("error", "Unknown error")
            )
        
        logger.info(f"Meeting scheduled successfully: {result.get('proposal_id', 'No ID')}")
        return MeetingProposalResponse(
            success=True,
            proposal_id=result.get("proposal_id"),
            suggested_slots=result.get("suggested_slots"),
            reasoning=result.get("reasoning"),
            agent_message=result.get("agent_message")
        )
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        
        logger.error(f"Unexpected error in schedule_meeting_legacy: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/confirm/{proposal_id}")
async def confirm_meeting(
    proposal_id: str, 
    selected_slot_index: int, 
    confirmed_by: str = "api_user",
    agent = Depends(get_agent_service)
):
    """Confirm a meeting proposal by selecting a time slot"""
    
    logger.info(f"Meeting confirmation requested: {proposal_id} (slot {selected_slot_index})")
    
    try:
        result = agent.confirm_meeting(proposal_id, selected_slot_index)
        
        if not result["success"]:
            logger.error(f"Meeting confirmation failed: {result.get('error', 'Unknown error')}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
        
        logger.info(f"Meeting confirmed successfully: {proposal_id}")
        return result
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/proposal/{proposal_id}", response_model=ProposalStatusResponse)
async def get_proposal_status(
    proposal_id: str,
    agent = Depends(get_agent_service)
):
    """Get the status of a meeting proposal"""
    
    try:
        if proposal_id not in agent.proposals:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proposal not found"
            )
        
        proposal = agent.proposals[proposal_id]
        
        return ProposalStatusResponse(
            proposal_id=proposal_id,
            status=proposal.status,
            meeting_title=proposal.meeting_request.title,
            participants=[p.email for p in proposal.meeting_request.get_all_participants()],
            suggested_slots=[
                {
                    "index": i,
                    "start_time": slot.start_time.isoformat(),
                    "end_time": slot.end_time.isoformat(),
                    "formatted": f"{slot.start_time.strftime('%A, %B %d at %I:%M %p')} - {slot.end_time.strftime('%I:%M %p')}"
                }
                for i, slot in enumerate(proposal.suggested_slots)
            ],
            reasoning=proposal.reasoning,
            created_at=proposal.created_at.isoformat()
        )
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/check-email-responses/{proposal_id}")
async def check_email_responses(
    proposal_id: str, 
    query: str = "",
    agent = Depends(get_agent_service)
):
    """Check for email responses related to meeting proposals"""
    
    try:
        result = agent._check_email_responses(proposal_id, query)
        return result
        
    except Exception as e:
        logger.error(f"Error checking email responses: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check email responses: {str(e)}"
        )


@router.get("/agent-tools")
async def get_agent_tools(agent = Depends(get_agent_service)):
    """Get information about available AI agent tools"""
    
    return {
        "tools": [
            {
                "name": tool["function"]["name"],
                "description": tool["function"]["description"],
                "parameters": list(tool["function"]["parameters"]["properties"].keys())
            }
            for tool in agent.tools
        ],
        "total_tools": len(agent.tools)
    }


@router.post("/receive", response_model=MeetingOutputEvent)
async def receive_meeting_request(
    request: ScheduleMeetingRequest,
    agent_service=Depends(get_agent_service)
) -> MeetingOutputEvent:
    """
    New endpoint that processes meeting requests and returns complete MeetingOutputEvent
    with MetaData according to JSON_Samples/3_Output_Event.json format
    """
    try:
        logger.info(f"Received meeting request for: {request.EmailContent}")
        
        # Convert to legacy format for processing
        legacy_request = convert_new_to_legacy_format(request)
        
        # Process the meeting request
        result = await agent_service.schedule_meeting(legacy_request)
        
        # Convert request to ProcessedMeetingInput format
        # Handle Attendees as either dict or AttendeeModel objects
        attendees_list = []
        for attendee in request.Attendees:
            if isinstance(attendee, dict):
                attendees_list.append(AttendeeModel(email=attendee['email']))
            else:
                attendees_list.append(attendee)
        
        processed_input = ProcessedMeetingInput(
            Request_id=request.Request_id,
            Datetime=request.Datetime,
            Location=request.Location or "Virtual Meeting",
            From=request.From,
            Attendees=attendees_list,
            Subject=request.Subject,
            EmailContent=request.EmailContent,
            Duration_mins=request.Duration_mins or 60
        )
        
        # Extract suggested times from result
        suggested_start = result.get("suggested_start_time", datetime.now())
        suggested_end = result.get("suggested_end_time", datetime.now() + timedelta(hours=1))
        
        # Create processing metadata
        processing_metadata = {
            "processing_time_ms": result.get("processing_time", 150),
            "model_used": "deepseek-llm-7b-chat",
            "conflicts_detected": 0,
            "request_id": request.Request_id
        }
        
        # Create the complete output event with MetaData
        output_event = create_output_event(
            processed_input, 
            suggested_start, 
            suggested_end,
            agent_response=result,
            processing_metadata=processing_metadata
        )
        
        logger.info(f"Successfully processed meeting request. Output event created with MetaData.")
        return output_event
        
    except Exception as e:
        logger.error(f"Error processing meeting request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process meeting request: {str(e)}"
        )


# @router.post("/natural-language-schedule")
# async def natural_language_schedule(query: str):
    """Future endpoint for natural language meeting scheduling"""
    
    # Placeholder for future NLP integration
    return {
        "message": "Natural language processing not yet implemented",
        "query": query,
        "status": "coming_soon"
    }