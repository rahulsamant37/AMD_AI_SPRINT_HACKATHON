# SchedulAI API Schema Documentation

## Overview

The SchedulAI API has been updated to exactly match the JSON schema format provided in the `JSON_Samples/` directory. The API supports a complete three-stage workflow with comprehensive metadata tracking:

1. **Input Request** - Matches `1_Input_Request.json` format exactly
2. **Processed Input** - Matches `2_Processed_Input.json` format exactly  
3. **Output Event** - Matches `3_Output_Event.json` format exactly with MetaData

All functionality from the original application has been preserved while adding rich metadata tracking for communication details and processing information.

## API Endpoints

### Primary Endpoint (New Schema)

**POST** `/api/meetings/schedule`

Uses the new JSON schema format that exactly matches the samples in `JSON_Samples/` directory.

### Legacy Endpoint (Backward Compatibility)

**POST** `/api/meetings/schedule-legacy`

Maintains the original API format for existing clients.

### Health Check Endpoint

**GET** `/api/health`

Returns API health status and service availability.

### Calendar Availability Endpoint

**GET** `/api/calendar/availability`

Returns calendar availability data for attendees.

## JSON Schema Formats

### 1. Input Request Format (ScheduleMeetingRequest)

Exactly matches `JSON_Samples/1_Input_Request.json`:

```json
{
    "Request_id": "6118b54f-907b-4451-8d48-dd13d76033a5",
    "Datetime": "09-07-2025T12:34:55",
    "Location": "IIT Mumbai",
    "From": "userone.amd@gmail.com",
    "Attendees": [
        {
            "email": "usertwo.amd@gmail.com"
        },
        {
            "email": "userthree.amd@gmail.com"
        }
    ],
    "Subject": "Agentic AI Project Status Update",
    "EmailContent": "Hi team, let's meet on Thursday for 30 minutes to discuss the status of Agentic AI Project."
}
```

#### Field Descriptions:

- **Request_id**: Unique identifier for the request (auto-generated if not provided)
- **Datetime**: Request timestamp in format "DD-MM-YYYYTHH:MM:SS"
- **Location**: Optional meeting location
- **From**: Organizer's email address
- **Attendees**: List of attendee objects with email addresses
- **Subject**: Meeting title/subject
- **EmailContent**: Meeting description with natural language scheduling preferences

### 2. Processed Input Format (ProcessedMeetingInput)

Exactly matches `JSON_Samples/2_Processed_Input.json`:

```json
{
    "Request_id": "6118b54f-907b-4451-8d48-dd13d76033a5",
    "Datetime": "09-07-2025T12:34:55",
    "Location": "IIT Mumbai",
    "From": "userone.amd@gmail.com",
    "Attendees": [
        {
            "email": "usertwo.amd@gmail.com"
        },
        {
            "email": "userthree.amd@gmail.com"
        }
    ],
    "Subject": "Agentic AI Project Status Update",
    "EmailContent": "Hi team, let's meet on Thursday for 30 minutes to discuss the status of Agentic AI Project.",
    "Start": "2025-07-17T00:00:00+05:30",
    "End": "2025-07-17T23:59:59+05:30",
    "Duration_mins": "30"
}
```

#### Additional Fields:

- **Start**: Processed start date range in ISO format with timezone (+05:30)
- **End**: Processed end date range in ISO format with timezone (+05:30)
- **Duration_mins**: Extracted meeting duration from EmailContent as string

### 3. Output Event Format (MeetingOutputEvent)

Exactly matches `JSON_Samples/3_Output_Event.json` including the **MetaData** field:

```json
{
    "Request_id": "6118b54f-907b-4451-8d48-dd13d76033a5",
    "Datetime": "09-07-2025T12:34:55",
    "Location": "IIT Mumbai",
    "From": "userone.amd@gmail.com",
    "Attendees": [
        {
            "email": "userone.amd@gmail.com",
            "events": [
                {
                    "StartTime": "2025-07-17T10:30:00+05:30",
                    "EndTime": "2025-07-17T11:00:00+05:30",
                    "NumAttendees": 3,
                    "Attendees": [
                        "userone.amd@gmail.com",
                        "usertwo.amd@gmail.com",
                        "userthree.amd@gmail.com"
                    ],
                    "Summary": "Agentic AI Project Status Update"
                }
            ]
        }
    ],
    "Subject": "Agentic AI Project Status Update",
    "EmailContent": "Hi team, let's meet on Thursday for 30 minutes to discuss the status of Agentic AI Project.",
    "EventStart": "2025-07-17T10:30:00+05:30",
    "EventEnd": "2025-07-17T11:00:00+05:30",
    "Duration_mins": "30",
    "MetaData": {}
}
```

## MetaData Field Details

The **MetaData** field contains comprehensive tracking information about the request processing:

### Structure

```json
{
    "MetaData": {
        "processing_timestamp": "2025-07-13T14:30:00+05:30",
        "agent_processing_time_ms": 150,
        "communication_details": {
            "request_source": "api_endpoint",
            "processing_method": "ai_agent_with_vllm",
            "model_used": "deepseek-llm-7b-chat",
            "calendar_integration": "google_calendar",
            "scheduling_confidence": 0.85,
            "conflicts_detected": 0,
            "alternative_slots_generated": 3
        },
        "workflow_stages": {
            "input_received": true,
            "input_processed": true,
            "calendar_checked": true,
            "slots_generated": true,
            "output_created": true
        },
        "calendar_sources": ["google_calendar"],
        "request_processing_method": "fastapi_agent_service"
    }
}
```

### MetaData Field Descriptions

#### Top-Level Fields
- **processing_timestamp**: When the request was processed
- **agent_processing_time_ms**: Time taken for AI processing in milliseconds

#### communication_details
- **request_source**: Source of the request (e.g., "api_endpoint")
- **processing_method**: Method used for processing (e.g., "ai_agent_with_vllm")
- **model_used**: AI model used for processing (e.g., "deepseek-llm-7b-chat")
- **calendar_integration**: Calendar service used (e.g., "google_calendar")
- **scheduling_confidence**: AI confidence score (0.0 to 1.0)
- **conflicts_detected**: Number of calendar conflicts found
- **alternative_slots_generated**: Number of alternative time slots suggested

#### workflow_stages
- **input_received**: Whether input was successfully received
- **input_processed**: Whether input was successfully processed
- **calendar_checked**: Whether calendar availability was checked
- **slots_generated**: Whether time slots were generated
- **output_created**: Whether final output was created

## API Response Format

The API returns a comprehensive response that includes:

```json
{
    "success": true,
    "proposal_id": "unique-proposal-id",
    "suggested_slots": [
        {
            "start_time": "2025-07-17T10:30:00+05:30",
            "end_time": "2025-07-17T11:00:00+05:30",
            "confidence": 0.85
        }
    ],
    "reasoning": "Found optimal time slot with no conflicts",
    "agent_message": "Meeting successfully scheduled for Thursday",
    "processed_input": {
        // ProcessedMeetingInput object
    },
    "output_event": {
        // MeetingOutputEvent object with MetaData
    }
}
```

## Usage Examples

### Basic Meeting Request

```python
import requests
import json

url = "http://localhost:8000/api/meetings/schedule"
data = {
    "Request_id": "unique-request-id",
    "Datetime": "13-07-2025T14:30:00",
    "Location": "Conference Room A", 
    "From": "organizer@company.com",
    "Attendees": [
        {"email": "participant1@company.com"},
        {"email": "participant2@company.com"}
    ],
    "Subject": "Project Review Meeting",
    "EmailContent": "Let's meet tomorrow for 1 hour to review the project status."
}

response = requests.post(url, json=data)
result = response.json()

if result.get("success"):
    print(f"Meeting scheduled: {result['proposal_id']}")
    print(f"Suggested time: {result['output_event']['EventStart']}")
    print(f"Processing time: {result['output_event']['MetaData']['agent_processing_time_ms']}ms")
    print(f"Confidence: {result['output_event']['MetaData']['communication_details']['scheduling_confidence']}")
else:
    print(f"Error: {result.get('error')}")
```

### Accessing MetaData Information

```python
output_event = result['output_event']
metadata = output_event['MetaData']

# Get processing information
processing_time = metadata['agent_processing_time_ms']
confidence = metadata['communication_details']['scheduling_confidence']
model_used = metadata['communication_details']['model_used']

# Check workflow completion
all_stages_complete = all(metadata['workflow_stages'].values())

print(f"Processed in {processing_time}ms using {model_used}")
print(f"Scheduling confidence: {confidence * 100}%")
print(f"All workflow stages completed: {all_stages_complete}")
```

## Features

### Core Functionality Preserved
- ✅ **Autonomous Coordination**: AI agent initiates scheduling without human micromanagement
- ✅ **Dynamic Adaptability**: Handles last-minute changes and conflicting priorities
- ✅ **Natural Language Processing**: Extracts scheduling preferences from EmailContent field
- ✅ **Calendar Integration**: Syncs with Google Calendar when properly configured
- ✅ **vLLM Integration**: Uses DeepSeek AI models for intelligent processing

### Enhanced with MetaData
- ✅ **Communication Tracking**: Full audit trail of to-and-fro communications
- ✅ **Processing Metrics**: Performance monitoring and optimization data
- ✅ **Workflow Validation**: Stage-by-stage completion tracking
- ✅ **AI Model Information**: Details about which models were used
- ✅ **Confidence Scoring**: AI confidence levels for scheduling decisions
- ✅ **Conflict Detection**: Detailed information about calendar conflicts

## Testing

Test files are provided in the `JSON_Samples/` directory:

1. `1_Input_Request.json` - Sample input request
2. `2_Processed_Input.json` - Expected processed format
3. `3_Output_Event.json` - Expected output format with MetaData

Use these files to test the API endpoints and validate the schema transformations including MetaData population.

## Error Handling

Common error scenarios:

1. **Invalid Email Format**: Returns 400 with validation error
2. **Missing Required Fields**: Returns 400 with field requirements
3. **Invalid DateTime Format**: Returns 400 with format requirements
4. **Server Errors**: Returns 500 with error details

Error responses may include MetaData with error tracking information.

## Migration Guide

For existing clients migrating to the new schema:

1. **Update Request Format**: Change field names to match new schema
2. **Handle New Response**: Process the additional `processed_input` and `output_event` fields
3. **Utilize MetaData**: Extract communication and processing details from MetaData
4. **Test Both Endpoints**: Verify functionality with both legacy and new endpoints
5. **Gradual Migration**: Use legacy endpoint during transition period

The new schema provides richer data and better integration capabilities while maintaining full backward compatibility and adding comprehensive metadata tracking for enhanced monitoring and debugging.
