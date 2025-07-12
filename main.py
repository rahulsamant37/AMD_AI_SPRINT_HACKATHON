from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI(
    title="Scheduling Agent API",
    description="API for processing scheduling requests and managing attendee events",
    version="1.0.0"
)

# Input Schema Models
class Attendee(BaseModel):
    email: str

class SchedulingRequest(BaseModel):
    Request_id: str
    Datetime: str
    Location: str
    From: str
    Attendees: List[Attendee]
    Subject: str | None = None
    EmailContent: str

# Processed Schema Models (for internal processing)
class ProcessedSchedulingRequest(BaseModel):
    Request_id: str
    Datetime: str
    Location: str
    From: str
    Attendees: List[Attendee]
    Subject: str | None = None
    EmailContent: str
    Start: str
    End: str
    Duration_mins: str

# Output Schema Models
class Event(BaseModel):
    StartTime: str
    EndTime: str
    NumAttendees: int
    Attendees: List[str]
    Summary: str

class AttendeeWithEvents(BaseModel):
    email: str
    events: List[Event]

class SchedulingResponse(BaseModel):
    Request_id: str
    Datetime: str
    Location: str
    From: str
    Attendees: List[AttendeeWithEvents]
    Subject: str | None = None
    EmailContent: str
    EventStart: str
    EventEnd: str
    Duration_mins: str

@app.get("/")
async def root():
    """Root endpoint providing API information"""
    return {
        "message": "Scheduling Agent API",
        "version": "1.0.0",
        "endpoints": {
            "schedule": "/schedule - POST endpoint for processing scheduling requests",
            "receive": "/receive - POST endpoint for receiving scheduling requests (alias for /schedule)",
            "health": "/health - GET endpoint for health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/schedule", response_model=SchedulingResponse)
async def process_scheduling_request(request: SchedulingRequest):
    """
    Process a scheduling request and return the formatted response with attendee events.
    
    This endpoint takes a scheduling request and processes it to generate a response
    that includes events for each attendee.
    """
    try:
        # Process the request (this is where your scheduling logic would go)
        processed_request = process_scheduling_logic(request)
        
        # Generate the response with attendee events
        response = generate_scheduling_response(processed_request)
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing scheduling request: {str(e)}")

@app.post("/receive", response_model=SchedulingResponse)
async def receive_scheduling_request(request: SchedulingRequest):
    """
    Receive endpoint - alias for the schedule endpoint to match external API calls.
    
    This endpoint takes a scheduling request and processes it to generate a response
    that includes events for each attendee.
    """
    # Use the same logic as the schedule endpoint
    return await process_scheduling_request(request)

def process_scheduling_logic(request: SchedulingRequest) -> ProcessedSchedulingRequest:
    """
    Convert the input request to processed format with calculated start/end times.
    This is a simplified version - you would implement your actual scheduling logic here.
    """
    # For demonstration, using example values from your schema
    # In a real implementation, you would parse the email content and datetime to calculate actual times
    
    return ProcessedSchedulingRequest(
        Request_id=request.Request_id,
        Datetime=request.Datetime,
        Location=request.Location,
        From=request.From,
        Attendees=request.Attendees,
        Subject=request.Subject,
        EmailContent=request.EmailContent,
        Start="2025-07-17T00:00:00+05:30",  # This would be calculated based on your logic
        End="2025-07-17T23:59:59+05:30",    # This would be calculated based on your logic
        Duration_mins="30"                   # This would be extracted from email content
    )

def generate_scheduling_response(processed_request: ProcessedSchedulingRequest) -> SchedulingResponse:
    """
    Generate the final response with attendee events.
    This function creates mock events for demonstration - replace with your actual logic.
    """
    # Extract attendee emails
    attendee_emails = [attendee.email for attendee in processed_request.Attendees]
    all_attendees = [processed_request.From] + attendee_emails
    
    # Determine meeting subject/summary
    meeting_summary = processed_request.Subject or "Project Discussion Meeting"
    
    # Create mock events for each attendee
    attendees_with_events = []
    
    for i, email in enumerate(all_attendees):
        events = []
        
        # Main meeting event (common to all attendees)
        main_event = Event(
            StartTime="2025-07-17T10:30:00+05:30",
            EndTime="2025-07-17T11:00:00+05:30",
            NumAttendees=len(all_attendees),
            Attendees=all_attendees,
            Summary=meeting_summary
        )
        events.append(main_event)
        
        # Add some mock additional events for demonstration
        if i > 0:  # Add different events for different attendees
            if i == 1:  # Second attendee
                additional_event = Event(
                    StartTime="2025-07-17T10:00:00+05:30",
                    EndTime="2025-07-17T10:30:00+05:30",
                    NumAttendees=len(all_attendees),
                    Attendees=all_attendees,
                    Summary="Team Meet"
                )
                events.insert(0, additional_event)  # Add before main event
            
            elif i == 2:  # Third attendee
                pre_event = Event(
                    StartTime="2025-07-17T10:00:00+05:30",
                    EndTime="2025-07-17T10:30:00+05:30",
                    NumAttendees=len(all_attendees),
                    Attendees=all_attendees,
                    Summary="Team Meet"
                )
                lunch_event = Event(
                    StartTime="2025-07-17T13:00:00+05:30",
                    EndTime="2025-07-17T14:00:00+05:30",
                    NumAttendees=1,
                    Attendees=["SELF"],
                    Summary="Lunch with Customers"
                )
                events.insert(0, pre_event)
                events.append(lunch_event)
        
        attendee_with_events = AttendeeWithEvents(
            email=email,
            events=events
        )
        attendees_with_events.append(attendee_with_events)
    
    return SchedulingResponse(
        Request_id=processed_request.Request_id,
        Datetime=processed_request.Datetime,
        Location=processed_request.Location,
        From=processed_request.From,
        Attendees=attendees_with_events,
        Subject=processed_request.Subject,
        EmailContent=processed_request.EmailContent,
        EventStart="2025-07-17T10:30:00+05:30",  # Main event start time
        EventEnd="2025-07-17T11:00:00+05:30",    # Main event end time
        Duration_mins=processed_request.Duration_mins
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)