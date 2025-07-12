import json
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Callable

from app.models import (
    MeetingRequest, MeetingProposal, TimeSlot, CalendarEvent,
    EmailMessage, AvailabilityRequest, UserPreferences,
    ToolCall, FunctionCall, AgentResponse, AgentAction
)
from app.config import config
from app.services.google_service import GoogleService
from app.services.vllm_service import VLLMService
from app.core.logging import get_logger

logger = get_logger(__name__)

class SchedulingAgent:
    """AI Agent that uses vLLM DeepSeek for meeting scheduling with function calling"""
    
    def __init__(self):
        logger.info("Initializing SchedulAI Agent with vLLM DeepSeek...")
        
        # Initialize vLLM service
        logger.debug("Setting up vLLM service...")
        self.vllm_service = VLLMService()
        
        # Perform health check
        if not self.vllm_service.health_check():
            logger.warning("vLLM server health check failed - continuing anyway")
        
        # Initialize Google service
        logger.debug("Setting up Google services...")
        self.google_service = GoogleService()
        
        # Initialize proposal storage
        self.proposals: Dict[str, MeetingProposal] = {}
        
        # Define available tools/functions
        logger.debug("Setting up agent tools...")
        self.tools = self._define_tools()
        self.tool_functions = self._define_tool_functions()
        
        logger.info(f"SchedulAI Agent initialized with {len(self.tools)} tools")
        logger.debug(f"Available tools: {[tool['function']['name'] for tool in self.tools]}")
        logger.info(f"Using vLLM DeepSeek model: {self.vllm_service.model_path}")
    
    def _define_tools(self) -> List[Dict[str, Any]]:
        """Define vLLM function calling tools (compatible with standard format)"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_calendar_availability",
                    "description": "Get calendar availability for participants in a date range",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "participant_emails": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of participant email addresses"
                            },
                            "start_date": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Start date in ISO format"
                            },
                            "end_date": {
                                "type": "string", 
                                "format": "date-time",
                                "description": "End date in ISO format"
                            },
                            "duration_minutes": {
                                "type": "integer",
                                "description": "Required meeting duration in minutes"
                            }
                        },
                        "required": ["participant_emails", "start_date", "end_date", "duration_minutes"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_optimal_slots",
                    "description": "Analyze availability data and recommend optimal meeting slots",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "availability_data": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "participant_email": {"type": "string"},
                                        "free_slots": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "start_time": {"type": "string"},
                                                    "end_time": {"type": "string"},
                                                    "available": {"type": "boolean"}
                                                }
                                            }
                                        },
                                        "busy_slots": {
                                            "type": "array", 
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "start_time": {"type": "string"},
                                                    "end_time": {"type": "string"}
                                                }
                                            }
                                        }
                                    }
                                },
                                "description": "Availability data for all participants"
                            },
                            "meeting_requirements": {
                                "type": "object",
                                "properties": {
                                    "duration_minutes": {"type": "integer"},
                                    "priority": {"type": "string"},
                                    "preferred_days": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "user_preferences": {
                                        "type": "object",
                                        "properties": {
                                            "work_start_hour": {"type": "integer"},
                                            "work_end_hour": {"type": "integer"},
                                            "timezone": {"type": "string"},
                                            "buffer_time_minutes": {"type": "integer"}
                                        }
                                    }
                                },
                                "description": "Meeting requirements including priority, duration, preferences"
                            },
                            "max_suggestions": {
                                "type": "integer",
                                "default": 3,
                                "description": "Maximum number of slot suggestions to return"
                            }
                        },
                        "required": ["availability_data", "meeting_requirements"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_calendar_event",
                    "description": "Create a calendar event for confirmed meeting",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Meeting title"},
                            "description": {"type": "string", "description": "Meeting description"},
                            "start_time": {"type": "string", "format": "date-time"},
                            "end_time": {"type": "string", "format": "date-time"},
                            "attendees": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Attendee email addresses"
                            },
                            "location": {"type": "string", "description": "Meeting location"}
                        },
                        "required": ["title", "start_time", "end_time", "attendees"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "send_meeting_email",
                    "description": "Send meeting proposal or confirmation email",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "to": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Recipient email addresses"
                            },
                            "subject": {"type": "string", "description": "Email subject"},
                            "body": {"type": "string", "description": "Email body content"},
                            "html_body": {"type": "string", "description": "HTML version of email body"},
                            "email_type": {
                                "type": "string",
                                "enum": ["proposal", "confirmation", "cancellation", "reminder"],
                                "description": "Type of email being sent"
                            }
                        },
                        "required": ["to", "subject", "body", "email_type"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_email_responses",
                    "description": "Check for email responses related to meeting proposals",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "proposal_id": {"type": "string", "description": "Meeting proposal ID"},
                            "query": {"type": "string", "description": "Search query for emails"},
                            "max_results": {"type": "integer", "default": 10}
                        },
                        "required": ["proposal_id"]
                    }
                }
            }
        ]
    
    def _define_tool_functions(self) -> Dict[str, Callable]:
        """Map tool names to actual function implementations"""
        return {
            "get_calendar_availability": self._get_calendar_availability,
            "analyze_optimal_slots": self._analyze_optimal_slots,
            "create_calendar_event": self._create_calendar_event,
            "send_meeting_email": self._send_meeting_email,
            "check_email_responses": self._check_email_responses
        }
    
    def schedule_meeting(self, meeting_request: MeetingRequest, 
                         user_preferences: Optional[UserPreferences] = None) -> Dict[str, Any]:
        """Main agent method to schedule a meeting using function calling"""
        
        proposal_id = str(uuid.uuid4())
        
        # Create system message for the agent
        system_message = self._create_system_message(user_preferences)
        
        # Create user message with meeting request
        user_message = self._create_meeting_request_message(meeting_request)
        
        try:
            # Initial conversation with the agent using vLLM
            response = self.vllm_service.create_chat_completion(
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                tools=self.tools,
                tool_choice="auto",
                temperature=0.3
            )
            
            # Process the agent's response and execute tools
            result = self._process_agent_response(response, proposal_id, meeting_request)
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Agent error: {str(e)}",
                "proposal_id": None
            }
    
    def _process_agent_response(self, response, proposal_id: str, 
                                meeting_request: MeetingRequest) -> Dict[str, Any]:
        """Process the agent's response and execute any tool calls"""
        
        assistant_message = response.choices[0].message
        tool_calls = assistant_message.tool_calls
        
        if not tool_calls:
            # No tools called, just return the message
            return {
                "success": False,
                "error": "Agent didn't call any tools to schedule the meeting",
                "message": assistant_message.content
            }
        
        # Execute tool calls
        messages = [
            {"role": "assistant", "content": assistant_message.content, "tool_calls": tool_calls}
        ]
        
        suggested_slots = []
        reasoning = ""
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # Execute the function
            if function_name in self.tool_functions:
                try:
                    function_result = self.tool_functions[function_name](**function_args)
                    
                    # Add tool result to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(function_result)
                    })
                    
                    # Process specific results
                    if function_name == "analyze_optimal_slots":
                        suggested_slots = function_result.get("suggested_slots", [])
                        reasoning = function_result.get("reasoning", "")
                    
                except Exception as e:
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": f"Error: {str(e)}"
                    })
        
        # Get final response from agent using vLLM
        final_response = self.vllm_service.create_chat_completion(
            messages=messages,
            temperature=0.3
        )
        
        # Create and store proposal
        if suggested_slots:
            # Convert slot dictionaries to TimeSlot objects
            time_slots = []
            for slot in suggested_slots:
                time_slots.append(TimeSlot(
                    start_time=datetime.fromisoformat(slot["start_time"]),
                    end_time=datetime.fromisoformat(slot["end_time"]),
                    available=True
                ))
            
            proposal = MeetingProposal(
                id=proposal_id,
                meeting_request=meeting_request,
                suggested_slots=time_slots,
                reasoning=reasoning,
                confidence_scores=[0.9] * len(time_slots)  # Placeholder
            )
            
            self.proposals[proposal_id] = proposal
            
            return {
                "success": True,
                "proposal_id": proposal_id,
                "suggested_slots": [
                    {
                        "index": i,
                        "start_time": slot.start_time.isoformat(),
                        "end_time": slot.end_time.isoformat(),
                        "formatted": f"{slot.start_time.strftime('%A, %B %d at %I:%M %p')} - {slot.end_time.strftime('%I:%M %p')}"
                    }
                    for i, slot in enumerate(time_slots)
                ],
                "reasoning": reasoning,
                "agent_message": final_response.choices[0].message.content
            }
        else:
            return {
                "success": False,
                "error": "No suitable meeting slots found",
                "agent_message": final_response.choices[0].message.content
            }
    
    # Tool function implementations
    def _get_calendar_availability(self, participant_emails: List[str], 
                                   start_date: str, end_date: str, 
                                   duration_minutes: int) -> Dict[str, Any]:
        """Get calendar availability for participants"""
        try:
            start_dt = datetime.fromisoformat(start_date)
            end_dt = datetime.fromisoformat(end_date)
            
            availability_responses = self.google_service.get_calendar_availability(
                participant_emails, start_dt, end_dt
            )
            
            # Convert to JSON-serializable format
            result = []
            for response in availability_responses:
                result.append({
                    "participant_email": response.participant_email,
                    "free_slots": [
                        {
                            "start_time": slot.start_time.isoformat(),
                            "end_time": slot.end_time.isoformat(),
                            "duration_minutes": int((slot.end_time - slot.start_time).total_seconds() / 60)
                        }
                        for slot in response.free_slots
                        if (slot.end_time - slot.start_time).total_seconds() / 60 >= duration_minutes
                    ],
                    "busy_slots": [
                        {
                            "start_time": slot.start_time.isoformat(),
                            "end_time": slot.end_time.isoformat()
                        }
                        for slot in response.busy_slots
                    ]
                })
            
            return {"availability_data": result, "success": True}
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _analyze_optimal_slots(self, availability_data: List[Dict], 
                               meeting_requirements: Dict[str, Any],
                               max_suggestions: int = 3) -> Dict[str, Any]:
        """Analyze availability and suggest optimal slots"""
        try:
            # Find common free slots across all participants
            if not availability_data:
                return {"suggested_slots": [], "reasoning": "No availability data provided"}
            
            # Get first participant's free slots as starting point
            common_slots = availability_data[0]["free_slots"]
            
            # Find intersection with other participants
            for participant_data in availability_data[1:]:
                participant_slots = participant_data["free_slots"]
                new_common_slots = []
                
                for common_slot in common_slots:
                    for participant_slot in participant_slots:
                        # Check for overlap
                        overlap_start = max(
                            datetime.fromisoformat(common_slot["start_time"]),
                            datetime.fromisoformat(participant_slot["start_time"])
                        )
                        overlap_end = min(
                            datetime.fromisoformat(common_slot["end_time"]),
                            datetime.fromisoformat(participant_slot["end_time"])
                        )
                        
                        if overlap_start < overlap_end:
                            overlap_duration = (overlap_end - overlap_start).total_seconds() / 60
                            required_duration = meeting_requirements.get("duration_minutes", 30)
                            
                            if overlap_duration >= required_duration:
                                new_common_slots.append({
                                    "start_time": overlap_start.isoformat(),
                                    "end_time": (overlap_start + timedelta(minutes=required_duration)).isoformat(),
                                    "duration_minutes": required_duration
                                })
                
                common_slots = new_common_slots
            
            # Score and rank slots based on preferences
            scored_slots = []
            for slot in common_slots[:max_suggestions * 2]:  # Get more to rank
                score = self._score_time_slot(slot, meeting_requirements)
                scored_slots.append((slot, score))
            
            # Sort by score and take top suggestions
            scored_slots.sort(key=lambda x: x[1], reverse=True)
            suggested_slots = [slot for slot, score in scored_slots[:max_suggestions]]
            
            reasoning = f"Found {len(common_slots)} common free slots. Selected top {len(suggested_slots)} based on meeting priority, work hours, and participant preferences."
            
            return {
                "suggested_slots": suggested_slots,
                "reasoning": reasoning,
                "total_analyzed": len(common_slots)
            }
            
        except Exception as e:
            return {"error": str(e), "suggested_slots": []}
    
    def _score_time_slot(self, slot: Dict[str, Any], requirements: Dict[str, Any]) -> float:
        """Score a time slot based on various criteria"""
        score = 0.0
        start_time = datetime.fromisoformat(slot["start_time"])
        
        # Time of day scoring (prefer mid-morning and early afternoon)
        hour = start_time.hour
        if 9 <= hour <= 11:  # Morning
            score += 0.3
        elif 13 <= hour <= 15:  # Early afternoon
            score += 0.2
        elif 8 <= hour <= 16:  # General work hours
            score += 0.1
        
        # Day of week scoring (prefer Tuesday-Thursday)
        weekday = start_time.weekday()
        if weekday in [1, 2, 3]:  # Tue, Wed, Thu
            score += 0.2
        elif weekday in [0, 4]:  # Mon, Fri
            score += 0.1
        
        # Priority scoring
        priority = requirements.get("priority", "medium")
        if priority == "urgent":
            # Earlier is better for urgent meetings
            score += 0.3 if hour <= 12 else 0.1
        elif priority == "low":
            # Later in day is fine for low priority
            score += 0.2 if hour >= 14 else 0.0
        
        # Avoid lunch time
        if 12 <= hour <= 13:
            score -= 0.2
        
        return score
    
    def _create_calendar_event(self, title: str, description: str, 
                               start_time: str, end_time: str,
                               attendees: List[str], location: str = "") -> Dict[str, Any]:
        """Create a calendar event"""
        try:
            event = CalendarEvent(
                title=title,
                description=description,
                start_time=datetime.fromisoformat(start_time),
                end_time=datetime.fromisoformat(end_time),
                attendees=attendees,
                location=location
            )
            
            event_id = self.google_service.create_calendar_event(event)
            
            return {
                "success": True,
                "event_id": event_id,
                "message": "Calendar event created successfully"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _send_meeting_email(self, to: List[str], subject: str, body: str,
                            html_body: str = "", email_type: str = "proposal") -> Dict[str, Any]:
        """Send meeting-related email"""
        try:
            email_message = EmailMessage(
                to=to,
                subject=subject,
                body=body,
                html_body=html_body if html_body else None
            )
            
            success = self.google_service.send_email(email_message)
            
            return {
                "success": success,
                "message": f"Email {email_type} sent successfully" if success else "Failed to send email",
                "email_type": email_type
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _check_email_responses(self, proposal_id: str, query: str = "", 
                               max_results: int = 10) -> Dict[str, Any]:
        """Check for email responses to meeting proposals"""
        try:
            # Search for emails related to the proposal
            if not query:
                query = f"meeting proposal {proposal_id}"
            
            emails = self.google_service.get_recent_emails(query, max_results)
            
            # Parse responses for confirmations/rejections
            responses = []
            for email in emails:
                response_type = self._parse_email_response(email["body"])
                responses.append({
                    "email_id": email["id"],
                    "sender": email["sender"],
                    "subject": email["subject"],
                    "response_type": response_type,
                    "body_snippet": email["body"][:200]
                })
            
            return {
                "success": True,
                "responses": responses,
                "total_found": len(emails)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _parse_email_response(self, email_body: str) -> str:
        """Parse email body to determine response type"""
        body_lower = email_body.lower()
        
        # Simple keyword-based parsing
        if any(word in body_lower for word in ["yes", "confirm", "accept", "agree", "sounds good"]):
            return "confirmation"
        elif any(word in body_lower for word in ["no", "decline", "reject", "can't", "cannot"]):
            return "rejection"
        elif any(word in body_lower for word in ["reschedule", "different time", "another time"]):
            return "reschedule_request"
        else:
            return "unclear"
    
    def _create_system_message(self, user_preferences: Optional[UserPreferences]) -> str:
        """Create system message for the agent"""
        prefs = user_preferences or UserPreferences()
        
        return f"""You are SchedulAI, an intelligent meeting scheduling agent. Your job is to:

1. Analyze meeting requests and participant availability
2. Use available tools to gather calendar information
3. Suggest optimal meeting times based on multiple factors
4. Handle email communications professionally
5. Create calendar events when meetings are confirmed

Key scheduling principles:
- Work hours: {prefs.work_start_hour}:00 - {prefs.work_end_hour}:00
- Preferred days: {', '.join(prefs.preferred_meeting_days)}
- Buffer time: {prefs.buffer_time_minutes} minutes between meetings
- Avoid lunch: {prefs.lunch_break_start}:00 - {prefs.lunch_break_start + 1}:00

When scheduling:
- High/urgent priority: Prefer earlier slots, shorter delays
- Medium priority: Balance convenience and timing
- Low priority: Optimize for participant convenience

Always explain your reasoning and be proactive in resolving conflicts.
Use the available tools systematically to gather data and execute actions."""
    
    def _create_meeting_request_message(self, meeting_request: MeetingRequest) -> str:
        """Create user message describing the meeting request"""
        organizer = f"{meeting_request.organizer.name} ({meeting_request.organizer.email})"
        participants = [f"{p.name} ({p.email})" for p in meeting_request.participants]
        all_attendees = [organizer] + participants
        
        return f"""Please schedule the following meeting:

Title: {meeting_request.title}
Description: {meeting_request.description}
Duration: {meeting_request.duration_minutes} minutes
Priority: {meeting_request.priority.value}

Organizer: {organizer} [Meeting requester - their preferences take priority]
Additional Participants: {', '.join(participants) if participants else 'None'}
Total Attendees: {len(all_attendees)}

Additional requirements:
- Preferred days: {', '.join(meeting_request.preferred_days) if meeting_request.preferred_days else 'Any weekday'}
- Buffer time: {meeting_request.buffer_time_minutes} minutes

Scheduling hierarchy:
1. Organizer preferences have highest priority
2. Find slots that work for ALL attendees
3. Optimize based on meeting priority and work hours

Please:
1. Check availability for all {len(all_attendees)} attendees for the next 7 days
2. Analyze and suggest the best 3 time slots that work for everyone
3. Send meeting proposal emails to all participants (including organizer)
4. Explain your reasoning for the suggested times"""

    def confirm_meeting(self, proposal_id: str, slot_index: int) -> Dict[str, Any]:
        """Confirm a meeting proposal"""
        if proposal_id not in self.proposals:
            return {"success": False, "error": "Proposal not found"}
        
        proposal = self.proposals[proposal_id]
        if slot_index >= len(proposal.suggested_slots):
            return {"success": False, "error": "Invalid slot index"}
        
        selected_slot = proposal.suggested_slots[slot_index]
        
        # Get all attendee emails (organizer + participants)
        all_attendees = proposal.meeting_request.get_all_emails()
        
        # Create calendar event
        event_result = self._create_calendar_event(
            title=proposal.meeting_request.title,
            description=proposal.meeting_request.description,
            start_time=selected_slot.start_time.isoformat(),
            end_time=selected_slot.end_time.isoformat(),
            attendees=all_attendees
        )
        
        if event_result["success"]:
            # Send confirmation emails to all attendees
            self._send_meeting_email(
                to=all_attendees,
                subject=f"Meeting Confirmed: {proposal.meeting_request.title}",
                body=f"Your meeting '{proposal.meeting_request.title}' has been confirmed for {selected_slot.start_time.strftime('%A, %B %d at %I:%M %p')}.\n\nOrganizer: {proposal.meeting_request.organizer.name}\nAttendees: {len(all_attendees)} total",
                email_type="confirmation"
            )
            
            # Update proposal status
            proposal.status = "confirmed"
            
            return {
                "success": True,
                "event_id": event_result["event_id"],
                "confirmed_slot": {
                    "start_time": selected_slot.start_time.isoformat(),
                    "end_time": selected_slot.end_time.isoformat()
                },
                "total_attendees": len(all_attendees),
                "organizer": proposal.meeting_request.organizer.email
            }
        else:
            return {"success": False, "error": event_result["error"]} 