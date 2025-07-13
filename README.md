# AI-Scheduling-Assistant

### Introduction 

#### Overview:
Welcome to the Agentic AI Scheduling Assistant Hackathon! This challenge invites developers, AI enthusiasts, and innovators to build an intelligent scheduling system that leverages Agentic AI - a next-generation approach where AI acts autonomously to achieve complex goals. 

Your mission: Create an AI assistant that eliminates the back-and-forth of meeting coordination by autonomously scheduling, rescheduling, and optimizing calendars.

#### Why Agentic AI? 
Traditional scheduling tools rely on rule-based automation or human input. Your solution should go further by: 
- Reasoning like a human assistant (e.g., prioritizing attendees, resolving conflicts).
- Acting independently (e.g., sending follow-ups, adjusting for time zones).
- Learning from user preferences (e.g., preferred times, recurring meetings). 

#### Key Features to Consider:
##### Your solution should aim to include: <br>
✅ Autonomous Coordination: The AI initiates scheduling without human micromanagement. <br>
✅ Dynamic Adaptability: Handles last-minute changes or conflicting priorities. <br>
✅ Natural Language Interaction: Users may converse with the AI (e.g., “Schedule a meeting on Tuesday”).  <br>
✅	Calendar Integration: Syncs with Google Calendar <br>

#### Success Metrics: 
#### A winning solution will excel in: <br>
✅ Autonomy: Minimal human intervention needed.  <br>
✅ Accuracy: Few scheduling errors or conflicts. <br>
✅ User Experience: Intuitive and time-saving. <br>

#### Setup & Requirements:
- Tools/APIs Needed: LLM ( vLLM server running on MI300 GPU). 
- Calendar APIs (Google Calendar). 
- Framework – May use License free tools & packages 
- Development Environment: Python

----------------

### To Create MI300 Instance, follow the steps in : [AMD Developer Cloud Setup Readme](https://github.com/AMD-AI-HACKATHON/AI-Scheduling-Assistant/blob/main/AMD_Developer_Cloud_Setup.md)
#### In High Level : 
- Select ```GPU Droplets```
- Click on ```Create GPU Droplets```
- Select ```AMD MI300X```
- In Snapshots, select ```Ubuntu_AMD_Hackathon_AI_Scheduling_Assistant```
- Create & Add SSH Keys
- Create GPU Droplet
- Open Web Console 
- Copy Paste URL in Chrome & Paste the Jupyter Token

----------------
### Extracting Google Calendar Events :
#### The Notebook demonstrates how to programmatically retrieve and process Google Calendar events for a given user and date range.
#### You will be provided with Google Auth Tokens to pull Google Calendar Events.

##### Key Steps:
- Authentication: Load user credentials from a token file.
- API Call: Fetch events between specified start/end dates using the Google Calendar API.
- Data Processing: Extract event details (start/end times, attendees) and structure them into a clean format.
- Output: Return a list of events with attendee counts and time slots.

#### Follow the notebook for example usage : [Calendar_Event_Extraction](https://github.com/AMD-AI-HACKATHON/AI-Scheduling-Assistant/blob/main/Calendar_Event_Extraction.ipynb)

----------------

### Setting-Up vLLM Server with Large Language Models : 

vLLM is an open-source library designed to deliver high throughput and low latency for large language model (LLM) inference. It optimizes text generation workloads by efficiently batching requests and making full use of GPU resources, empowering developers to manage complex tasks like code generation and large-scale conversational AI.

#### Start the vLLM server with DeepSeek LLM 7B Chat Model

Open a new tab in this Jypyter server, click on the terminal icon to open a new terminal, then copy the following command to launch the vLLM server:

```bash
HIP_VISIBLE_DEVICES=0 vllm serve /home/user/Models/deepseek-ai/deepseek-llm-7b-chat \
        --gpu-memory-utilization 0.9 \
        --swap-space 16 \
        --disable-log-requests \
        --dtype float16 \
        --max-model-len 2048 \
        --tensor-parallel-size 1 \
        --host 0.0.0.0 \
        --port 3000 \
        --num-scheduler-steps 10 \
        --max-num-seqs 128 \
        --max-num-batched-tokens 2048 \
        --max-model-len 2048 \
        --distributed-executor-backend "mp"
```
#### For setting up vLLM server with DeepSeek Model & usage, please follow : [vLLM_Inference_Servering_DeepSeek](https://github.com/AMD-AI-HACKATHON/AI-Scheduling-Assistant/blob/main/vLLM_Inference_Servering_DeepSeek.ipynb)

#### Start the vLLM server with Meta-Llama-3.1-8B-Instruct Model

Open a new tab in this Jypyter server, click on the terminal icon to open a new terminal, then copy the following command to launch the vLLM server:

```bash
HIP_VISIBLE_DEVICES=0 vllm serve /home/user/Models/meta-llama/Meta-Llama-3.1-8B-Instruct \
        --gpu-memory-utilization 0.3 \
        --swap-space 16 \
        --disable-log-requests \
        --dtype float16 \
        --max-model-len 2048 \
        --tensor-parallel-size 1 \
        --host 0.0.0.0 \
        --port 4000 \
        --num-scheduler-steps 10 \
        --max-num-seqs 128 \
        --max-num-batched-tokens 2048 \
        --max-model-len 2048 \
        --distributed-executor-backend "mp"
```

#### For setting up vLLM server with LLama Model & usage, please follow : [vLLM_Inference_Servering_LLaMA](https://gitenterprise.xilinx.com/asirra/AI-Scheduling-Assistant/blob/main/vLLM_Inference_Servering_LLaMA.ipynb)
----------------

### Setting-Up AI Agent :


#### Start the vLLM server with DeepSeek Model

Open a new tab in this Jypyter server, click on the terminal icon to open a new terminal, then copy the following command to launch the vLLM server:

```bash
HIP_VISIBLE_DEVICES=0 vllm serve /home/user/Models/deepseek-ai/deepseek-llm-7b-chat \
        --gpu-memory-utilization 0.9 \
        --swap-space 16 \
        --disable-log-requests \
        --dtype float16 \
        --max-model-len 2048 \
        --tensor-parallel-size 1 \
        --host 0.0.0.0 \
        --port 3000 \
        --num-scheduler-steps 10 \
        --max-num-seqs 128 \
        --max-num-batched-tokens 2048 \
        --max-model-len 2048 \
        --distributed-executor-backend "mp"
```

#### Sample AI Agent that parse Email Input & Output the Processed JSON
```
class AI_AGENT:
    def __init__(self, client, MODEL_PATH):
        self.base_url = BASE_URL
        self.model_path = MODEL_PATH

    def parse_email(self, email_text):
        response = client.chat.completions.create(
            model=self.model_path,
            temperature=0.0,
            messages=[{
                "role": "user",
                "content": f"""
                Yor are an Agent that helps in scheduling meetings.
                Your job is to extracts Email ID's and Meeting Duration.
                You should return :
                1. List of email id's of participants (comma-separated).
                2. Meeting duration in minutes.
                3. Time constraints (e.g., 'next week').
                If the List of email id's of participants are just names, then append @amd.com at the end and return. 
                Return as json with 'participants', 'time_constraints' & 'meeting_duration'.
                Stricty follow the instructions. Strictly return dict with participents email id's, time constraints & meeting duration in minutes only. 
                Don not add any other instrctions or information. 
                
                Email: {email_text}
                
                """
            }]
        )
        return json.loads(response.choices[0].message.content)
```


#### Follow the Notebook for setting-up an example AI Agent : [Sample_AI_Agent](https://github.com/AMD-AI-HACKATHON/AI-Scheduling-Assistant/blob/main/Sample_AI_Agent.ipynb)

The Notebook demonstrates how to create a simple AI Agent that uses vLLM & OpenAI API to communicate with LLM Model.

----------------

### FastAPI Application Schema

This project provides a complete FastAPI web application that implements the AI Scheduling Assistant with the exact schema matching the JSON samples. The API provides endpoints that support the full workflow from input processing to final output generation.

#### API Endpoints

The FastAPI application exposes the following main endpoints:

- **POST `/api/meetings/schedule`** - Main endpoint for scheduling meetings (new JSON schema)
- **POST `/api/meetings/schedule-legacy`** - Legacy endpoint for backward compatibility
- **GET `/api/health`** - Health check endpoint
- **GET `/api/calendar/availability`** - Calendar availability endpoint

#### Schema Objects

The API defines the following Pydantic models that exactly match the JSON sample formats:

##### 1. Input Request Schema (`ScheduleMeetingRequest`)
Matches `1_Input_Request.json` format:
```python
{
    "Request_id": "string (UUID)",
    "Datetime": "string (DD-MM-YYYYTHH:MM:SS format)",
    "Location": "string (optional)",
    "From": "string (email)",
    "Attendees": [{"email": "string"}],
    "Subject": "string",
    "EmailContent": "string"
}
```

##### 2. Processed Input Schema (`ProcessedMeetingInput`)
Matches `2_Processed_Input.json` format:
```python
{
    "Request_id": "string (UUID)",
    "Datetime": "string (DD-MM-YYYYTHH:MM:SS)",
    "Location": "string (optional)",
    "From": "string (email)",
    "Attendees": [{"email": "string"}],
    "Subject": "string", 
    "EmailContent": "string",
    "Start": "string (YYYY-MM-DDTHH:MM:SS+05:30)",
    "End": "string (YYYY-MM-DDTHH:MM:SS+05:30)",
    "Duration_mins": "string"
}
```

##### 3. Output Event Schema (`MeetingOutputEvent`)
Matches `3_Output_Event.json` format:
```python
{
    "Request_id": "string (UUID)",
    "Datetime": "string (DD-MM-YYYYTHH:MM:SS)",
    "Location": "string (optional)",
    "From": "string (email)",
    "Attendees": [
        {
            "email": "string",
            "events": [
                {
                    "StartTime": "string (YYYY-MM-DDTHH:MM:SS+05:30)",
                    "EndTime": "string (YYYY-MM-DDTHH:MM:SS+05:30)",
                    "NumAttendees": "integer",
                    "Attendees": ["string"],
                    "Summary": "string"
                }
            ]
        }
    ],
    "Subject": "string",
    "EmailContent": "string",
    "EventStart": "string (YYYY-MM-DDTHH:MM:SS+05:30)",
    "EventEnd": "string (YYYY-MM-DDTHH:MM:SS+05:30)",
    "Duration_mins": "string",
    "MetaData": {
        "processing_timestamp": "string",
        "communication_details": {
            "request_source": "string",
            "processing_method": "string",
            "model_used": "string",
            "calendar_integration": "string",
            "scheduling_confidence": "number",
            "conflicts_detected": "integer"
        },
        "workflow_stages": {
            "input_received": "boolean",
            "input_processed": "boolean",
            "calendar_checked": "boolean",
            "slots_generated": "boolean",
            "output_created": "boolean"
        }
    }
}
```

#### API Response Format

The API returns a comprehensive response that includes:
```python
{
    "success": "boolean",
    "proposal_id": "string (optional)",
    "suggested_slots": "array (optional)",
    "reasoning": "string (optional)",
    "agent_message": "string (optional)",
    "processed_input": "ProcessedMeetingInput object",
    "output_event": "MeetingOutputEvent object"
}
```

#### Running the FastAPI Application

To start the FastAPI server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000
```

The server will be available at:
- API: `http://localhost:5000`
- Swagger UI: `http://localhost:5000/docs`
- ReDoc: `http://localhost:5000/redoc`

#### Features Maintained

All functionality from the original README has been preserved:
- ✅ Autonomous Coordination: AI initiates scheduling without human micromanagement
- ✅ Dynamic Adaptability: Handles last-minute changes and conflicting priorities
- ✅ Natural Language Interaction: Processes natural language requests from EmailContent
- ✅ Calendar Integration: Syncs with Google Calendar (when configured)
- ✅ vLLM Integration: Uses DeepSeek AI models for intelligent processing
- ✅ Backward Compatibility: Supports legacy API format alongside new schema

#### Schema Validation

The API includes comprehensive validation:
- Date format validation for `Datetime` field (DD-MM-YYYYTHH:MM:SS)
- ISO datetime with timezone validation for processed times (+05:30)
- Email format validation for attendee emails
- Required field validation for all mandatory fields

----------------

### Inputs & Outputs : 
#### Input JSON : 

The input to your code will be in JSON format in the below structure. 
```
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

#### Processed JSON : 
Your AI Agent takes the Input JSON & process it to output another JSON in the below format. <br>
##### Note : This output will be graded for quallifying & scoring. 

```
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

#### Final Output JSON : 
Your Final Output JSON should follow below structure.  <br>
##### Note : This output will be graded for quallifying & scoring. 
```
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
        },
        {
            "email": "usertwo.amd@gmail.com",
            "events": [
                {
                    "StartTime": "2025-07-17T10:00:00+05:30",
                    "EndTime": "2025-07-17T10:30:00+05:30",
                    "NumAttendees": 3,
                    "Attendees": [
                        "userone.amd@gmail.com",
                        "usertwo.amd@gmail.com",
                        "userthree.amd@gmail.com"
                    ],
                    "Summary": "Team Meet"
                },
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
        },
        {
            "email": "userthree.amd@gmail.com",
            "events": [
                {
                    "StartTime": "2025-07-17T10:00:00+05:30",
                    "EndTime": "2025-07-17T10:30:00+05:30",
                    "NumAttendees": 3,
                    "Attendees": [
                        "userone.amd@gmail.com",
                        "usertwo.amd@gmail.com",
                        "userthree.amd@gmail.com"
                    ],
                    "Summary": "Team Meet"
                },
                {
                    "StartTime": "2025-07-17T13:00:00+05:30",
                    "EndTime": "2025-07-17T14:00:00+05:30",
                    "NumAttendees": 1,
                    "Attendees": [
                        "SELF"
                    ],
                    "Summary": "Lunch with Customers"
                },
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
    "Duration_mins": "30"
}
```
---------
### Submission :

#### Please follow : [Submission Notebook](https://github.com/AMD-AI-HACKATHON/AI-Scheduling-Assistant/blob/main/Submission.ipynb)
##### ```def your_meeting_assistant( )``` takes Meeting request JSON as Input
##### ```your_meeting_assistant( )``` returns with two New Fields : 
- processed 
- output
#### At the end of the Hackathon time ( at 2:00 P.M), you must execute this code
#### We will send JSONs at Port 5000 & will receive your AI Assistant Response
#### Make sure that your Output strictly follows the specified format. 

---------

### Evaluation Criteria for Scoring & Ranking :
- Correctness of Output – Accuracy and precision of the results 
- Roundtrip Latency – Speed and efficiency of processing and response 
- Maintenance of GitHub Repository – Code organization, documentation, and commit hygiene 
- Creativeness in Approach – Innovation, originality, and problem-solving uniqueness 
- Scoring Based on Performance – Combined assessment of correctness, latency, repo quality, and creativity 
- Ranking Methodology – Comparative evaluation to determine the best-performing solution