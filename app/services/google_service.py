"""
Google API Service for Calendar and Gmail integration

Handles authentication and operations with Google Calendar and Gmail APIs.
Supports multiple authenticated users through AuthenticationManager.
"""

import pickle
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import email.mime.text as mime_text
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.credentials import Credentials
from googleapiclient.errors import HttpError
from fastapi import HTTPException

from app.models import CalendarEvent, EmailMessage, TimeSlot, AvailabilityResponse
from app.config import config
from app.core.logging import get_logger
from app.core.exceptions import GoogleServiceException, CalendarException, EmailException
from app.services.auth_manager import get_auth_manager

logger = get_logger(__name__)

class GoogleService:
    """Unified Google service for Calendar and Gmail APIs with multi-user support"""
    
    def __init__(self):
        logger.info("Initializing Google Service...")
        # Legacy single-user support
        self.credentials = None
        self.calendar_service = None
        self.gmail_service = None
        
        # Multi-user authentication manager
        self.auth_manager = get_auth_manager()
        
        # Try to initialize with legacy method for backwards compatibility
        self._legacy_authenticate()
    
    def _legacy_authenticate(self):
        """Legacy authentication method for backwards compatibility"""
        logger.info("Attempting legacy authentication for backwards compatibility...")
        creds = None
        
        # Load existing token
        if os.path.exists(config.GOOGLE_TOKEN_FILE):
            logger.debug(f"Loading existing token from: {config.GOOGLE_TOKEN_FILE}")
            try:
                with open(config.GOOGLE_TOKEN_FILE, 'rb') as token:
                    creds = pickle.load(token)
                logger.debug("Legacy token loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load legacy token: {str(e)}")
        else:
            logger.info("No legacy token found")
        
        # If there are no valid credentials, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("Refreshing expired legacy credentials...")
                try:
                    creds.refresh(Request())
                    logger.info("Legacy credentials refreshed successfully")
                except Exception as e:
                    logger.error(f"Failed to refresh legacy credentials: {str(e)}")
                    creds = None
            
            if not creds or not creds.valid:
                logger.info("Starting new OAuth2 flow for legacy compatibility...")
                if os.path.exists(config.GOOGLE_CREDENTIALS_FILE):
                    logger.debug(f"Using credentials file: {config.GOOGLE_CREDENTIALS_FILE}")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        config.GOOGLE_CREDENTIALS_FILE, 
                        config.GOOGLE_SCOPES
                    )
                    logger.info("Starting local server for OAuth2...")
                    creds = flow.run_local_server(port=0)
                    logger.info("OAuth2 flow completed successfully")
                else:
                    logger.warning(f"Google credentials file not found: {config.GOOGLE_CREDENTIALS_FILE}")
                    logger.info("Legacy authentication skipped - will use multi-user system only")
                    return
            
            # Save the credentials for the next run
            if creds:
                logger.debug(f"Saving legacy credentials to: {config.GOOGLE_TOKEN_FILE}")
                try:
                    with open(config.GOOGLE_TOKEN_FILE, 'wb') as token:
                        pickle.dump(creds, token)
                    logger.debug("Legacy credentials saved successfully")
                except Exception as e:
                    logger.warning(f"Failed to save legacy credentials: {str(e)}")
        
        # Build legacy services if we have credentials
        if creds and creds.valid:
            logger.info("Building legacy Google API services...")
            try:
                self.credentials = creds
                self.calendar_service = build('calendar', 'v3', credentials=creds)
                self.gmail_service = build('gmail', 'v1', credentials=creds)
                
                logger.info("Legacy Google services authenticated successfully")
                logger.debug(f"Available scopes: {', '.join(config.GOOGLE_SCOPES)}")
            except Exception as e:
                logger.error(f"Failed to build legacy Google services: {str(e)}")
                self.credentials = None
                self.calendar_service = None
                self.gmail_service = None
        else:
            logger.info("No legacy credentials available - using multi-user system only")
    
    def get_user_service(self, email: str, service_type: str = 'calendar'):
        """Get Google API service for a specific authenticated user"""
        try:
            credentials = self.auth_manager.get_user_credentials(email)
            if not credentials:
                logger.error(f"No valid credentials found for user: {email}")
                return None
            
            if service_type == 'calendar':
                return build('calendar', 'v3', credentials=credentials)
            elif service_type == 'gmail':
                return build('gmail', 'v1', credentials=credentials)
            else:
                logger.error(f"Unknown service type: {service_type}")
                return None
        except Exception as e:
            logger.error(f"Failed to build {service_type} service for {email}: {e}")
            return None
    
    def is_user_authenticated(self, email: str) -> bool:
        """Check if a user is authenticated"""
        return self.auth_manager.is_user_authenticated(email)
    
    def get_authenticated_users(self) -> List[str]:
        """Get list of all authenticated users"""
        return self.auth_manager.get_authenticated_users()
    
    def authenticate_new_user(self) -> Optional[str]:
        """Authenticate a new user"""
        return self.auth_manager.authenticate_new_user()
    
    def remove_user_authentication(self, email: str) -> bool:
        """Remove user authentication"""
        return self.auth_manager.remove_user_authentication(email)
    
    # Calendar Methods
    def get_calendar_availability(self, participant_emails: List[str], 
                                start_date: datetime, end_date: datetime) -> List[AvailabilityResponse]:
        """Get availability for participants using multi-user authentication"""
        try:
            availability_responses = []
            
            for email in participant_emails:
                logger.debug(f"Checking availability for: {email}")
                
                # Check if user is authenticated
                if self.is_user_authenticated(email):
                    # Get user-specific calendar service
                    calendar_service = self.get_user_service(email, 'calendar')
                    if not calendar_service:
                        logger.error(f"Failed to get calendar service for {email}")
                        availability_responses.append(AvailabilityResponse(
                            participant_email=email,
                            free_slots=[],
                            busy_slots=[]
                        ))
                        continue
                    
                    # Get busy times for authenticated user
                    body = {
                        'timeMin': start_date.isoformat() + 'Z' if not start_date.tzinfo else start_date.isoformat(),
                        'timeMax': end_date.isoformat() + 'Z' if not end_date.tzinfo else end_date.isoformat(),
                        'items': [{'id': 'primary'}]  # Use primary calendar
                    }
                    
                    try:
                        freebusy_result = calendar_service.freebusy().query(body=body).execute()
                        busy_times = freebusy_result['calendars'].get('primary', {}).get('busy', [])
                        
                        # Convert busy times to TimeSlot objects
                        busy_slots = []
                        for busy_period in busy_times:
                            start_time = datetime.fromisoformat(busy_period['start'].replace('Z', '+00:00'))
                            end_time = datetime.fromisoformat(busy_period['end'].replace('Z', '+00:00'))
                            busy_slots.append(TimeSlot(
                                start_time=start_time,
                                end_time=end_time,
                                available=False
                            ))
                        
                        # Calculate free slots
                        free_slots = self._calculate_free_slots(start_date, end_date, busy_slots)
                        
                        availability_responses.append(AvailabilityResponse(
                            participant_email=email,
                            free_slots=free_slots,
                            busy_slots=busy_slots
                        ))
                        
                        logger.info(f"Successfully retrieved availability for authenticated user: {email}")
                        
                    except HttpError as e:
                        logger.error(f"Error getting availability for {email}: {e}")
                        availability_responses.append(AvailabilityResponse(
                            participant_email=email,
                            free_slots=[],
                            busy_slots=[]
                        ))
                else:
                    # External user - return empty availability
                    logger.info(f"External user {email} - returning empty availability (not authenticated)")
                    availability_responses.append(AvailabilityResponse(
                        participant_email=email,
                        free_slots=[],
                        busy_slots=[]
                    ))
            
            return availability_responses
            
        except HttpError as error:
            logger.error(f'Calendar API error: {error}')
            return []
    
    def _calculate_free_slots(self, start_date: datetime, end_date: datetime, 
                             busy_slots: List[TimeSlot]) -> List[TimeSlot]:
        """Calculate free time slots from busy periods"""
        free_slots = []
        
        # Ensure all datetime objects have the same timezone info
        if start_date.tzinfo is None:
            start_date = start_date.replace(tzinfo=None)
        if end_date.tzinfo is None:
            end_date = end_date.replace(tzinfo=None)
        
        # Normalize busy slots to match timezone info
        normalized_busy_slots = []
        for slot in busy_slots:
            start_time = slot.start_time
            end_time = slot.end_time
            
            # Convert timezone-aware to naive if our dates are naive
            if start_date.tzinfo is None:
                if start_time.tzinfo is not None:
                    start_time = start_time.replace(tzinfo=None)
                if end_time.tzinfo is not None:
                    end_time = end_time.replace(tzinfo=None)
            
            normalized_busy_slots.append(TimeSlot(
                start_time=start_time,
                end_time=end_time,
                available=False
            ))
        
        # Sort busy slots by start time
        normalized_busy_slots.sort(key=lambda x: x.start_time)
        
        current_time = start_date
        
        for busy_slot in normalized_busy_slots:
            # If there's a gap before this busy slot, it's free time
            if current_time < busy_slot.start_time:
                free_slots.append(TimeSlot(
                    start_time=current_time,
                    end_time=busy_slot.start_time,
                    available=True
                ))
            
            # Move current time to end of busy slot
            current_time = max(current_time, busy_slot.end_time)
        
        # Add final free slot if there's time remaining
        if current_time < end_date:
            free_slots.append(TimeSlot(
                start_time=current_time,
                end_time=end_date,
                available=True
            ))
        
        return free_slots
    
    def create_calendar_event(self, event: CalendarEvent, user_email: str = None) -> Optional[str]:
        """Create a calendar event for a specific user or primary user"""
        try:
            # Determine which user to create the event for
            if user_email and self.is_user_authenticated(user_email):
                calendar_service = self.get_user_service(user_email, 'calendar')
                logger.info(f"Creating calendar event for authenticated user: {user_email}")
            elif self.calendar_service:
                calendar_service = self.calendar_service
                logger.info("Creating calendar event using legacy service")
            else:
                # Try to use the first authenticated user
                authenticated_users = self.get_authenticated_users()
                if authenticated_users:
                    user_email = authenticated_users[0]
                    calendar_service = self.get_user_service(user_email, 'calendar')
                    logger.info(f"Creating calendar event for first authenticated user: {user_email}")
                else:
                    logger.error("No authenticated users available for calendar event creation")
                    return None
            
            if not calendar_service:
                logger.error("Failed to get calendar service for event creation")
                return None
            
            # Prepare attendees
            attendees = [{'email': email} for email in event.attendees]
            
            # Create event body
            event_body = {
                'summary': event.title,
                'description': event.description,
                'start': {
                    'dateTime': event.start_time.isoformat(),
                    'timeZone': event.timezone,
                },
                'end': {
                    'dateTime': event.end_time.isoformat(),
                    'timeZone': event.timezone,
                },
                'attendees': attendees,
                'sendUpdates': 'all'
            }
            
            if event.location:
                event_body['location'] = event.location
            
            # Create the event
            created_event = calendar_service.events().insert(
                calendarId='primary', 
                body=event_body,
                sendUpdates='all'
            ).execute()
            
            logger.info(f"✅ Calendar event created: {created_event.get('id')}")
            return created_event.get('id')
            
        except HttpError as error:
            logger.error(f'Error creating calendar event: {error}')
            return None
    
    def get_calendar_events(self, start_date: datetime, end_date: datetime, user_email: str = None) -> List[CalendarEvent]:
        """Get calendar events in date range for specified user"""
        try:
            logger.info(f"Requested user email: {user_email}")
            
            # Determine which user's calendar to access
            if user_email:
                # Check if requested user is authenticated
                if self.is_user_authenticated(user_email):
                    calendar_service = self.get_user_service(user_email, 'calendar')
                    calendar_id = 'primary'
                    logger.info(f"Accessing calendar for authenticated user: {user_email}")
                else:
                    logger.warning(f"User {user_email} is not authenticated")
                    raise HTTPException(
                        status_code=403,
                        detail=f"User '{user_email}' is not authenticated. Please authenticate first."
                    )
            else:
                # No user specified - try legacy service first, then first authenticated user
                if self.calendar_service:
                    calendar_service = self.calendar_service
                    calendar_id = 'primary'
                    user_email = self.get_authenticated_email()  # For legacy compatibility
                    logger.info(f"Using legacy calendar service for user: {user_email}")
                else:
                    # Use first authenticated user
                    authenticated_users = self.get_authenticated_users()
                    if authenticated_users:
                        user_email = authenticated_users[0]
                        calendar_service = self.get_user_service(user_email, 'calendar')
                        calendar_id = 'primary'
                        logger.info(f"Using first authenticated user: {user_email}")
                    else:
                        logger.error("No authenticated users available")
                        raise HTTPException(
                            status_code=401,
                            detail="No authenticated users found. Please authenticate first."
                        )
            
            if not calendar_service:
                logger.error(f"Failed to get calendar service for user: {user_email}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to access calendar service for user: {user_email}"
                )
            
            logger.info(f"Final calendar service initialized for user: {user_email}")
            logger.info(f"Final calendar ID: {calendar_id}")
            
            # Ensure proper timezone formatting
            time_min = start_date.isoformat() + 'Z' if not start_date.tzinfo else start_date.isoformat()
            time_max = end_date.isoformat() + 'Z' if not end_date.tzinfo else end_date.isoformat()
            
            logger.debug(f"Fetching calendar events from {time_min} to {time_max} for user: {user_email}")
            
            events_result = calendar_service.events().list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            logger.info(f"Found {len(events)} calendar events for user: {user_email}")
            
            calendar_events = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                
                start_time = datetime.fromisoformat(start.replace('Z', '+00:00'))
                end_time = datetime.fromisoformat(end.replace('Z', '+00:00'))
                
                attendees = []
                if 'attendees' in event:
                    attendees = [attendee['email'] for attendee in event['attendees']]
                
                calendar_events.append(CalendarEvent(
                    id=event['id'],
                    title=event.get('summary', 'No title'),
                    description=event.get('description', ''),
                    start_time=start_time,
                    end_time=end_time,
                    attendees=attendees,
                    location=event.get('location', ''),
                    timezone=event.get('start', {}).get('timeZone', 'UTC')
                ))
            
            return calendar_events
            
        except HttpError as error:
            logger.error(f'Error fetching calendar events for {user_email}: {error}')
            # Re-raise the error so the API endpoint can handle it properly
            raise error
    
    # Gmail Methods
    def send_email(self, email_message: EmailMessage, user_email: str = None) -> bool:
        """Send email using Gmail API for specified user"""
        try:
            # Determine which user to send email from
            if user_email and self.is_user_authenticated(user_email):
                gmail_service = self.get_user_service(user_email, 'gmail')
                logger.info(f"Sending email from authenticated user: {user_email}")
            elif self.gmail_service:
                gmail_service = self.gmail_service
                logger.info("Sending email using legacy service")
            else:
                # Try to use the first authenticated user
                authenticated_users = self.get_authenticated_users()
                if authenticated_users:
                    user_email = authenticated_users[0]
                    gmail_service = self.get_user_service(user_email, 'gmail')
                    logger.info(f"Sending email from first authenticated user: {user_email}")
                else:
                    logger.error("No authenticated users available for email sending")
                    return False
            
            if not gmail_service:
                logger.error("Failed to get Gmail service for email sending")
                return False
            
            # Create message
            message = MIMEMultipart('alternative')
            message['To'] = ', '.join(email_message.to)
            message['Subject'] = email_message.subject
            
            # Add plain text part
            text_part = MIMEText(email_message.body, 'plain')
            message.attach(text_part)
            
            # Add HTML part if provided
            if email_message.html_body:
                html_part = MIMEText(email_message.html_body, 'html')
                message.attach(html_part)
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Send message
            send_message = {
                'raw': raw_message
            }
            
            # Add thread ID if provided (for replies)
            if email_message.thread_id:
                send_message['threadId'] = email_message.thread_id
            
            result = gmail_service.users().messages().send(
                userId='me',
                body=send_message
            ).execute()
            
            logger.info(f"✅ Email sent successfully: {result.get('id')}")
            return True
            
        except HttpError as error:
            logger.error(f'Error sending email: {error}')
            return False
    
    def get_recent_emails(self, query: str = '', max_results: int = 10, user_email: str = None) -> List[Dict[str, Any]]:
        """Get recent emails matching query for specified user"""
        try:
            # Determine which user to get emails from
            if user_email and self.is_user_authenticated(user_email):
                gmail_service = self.get_user_service(user_email, 'gmail')
            elif self.gmail_service:
                gmail_service = self.gmail_service
            else:
                # Use first authenticated user
                authenticated_users = self.get_authenticated_users()
                if authenticated_users:
                    user_email = authenticated_users[0]
                    gmail_service = self.get_user_service(user_email, 'gmail')
                else:
                    logger.error("No authenticated users available for email retrieval")
                    return []
            
            if not gmail_service:
                logger.error("Failed to get Gmail service for email retrieval")
                return []
            
            results = gmail_service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            email_list = []
            
            for message in messages:
                msg = gmail_service.users().messages().get(
                    userId='me',
                    id=message['id']
                ).execute()
                
                # Extract email details
                headers = msg['payload'].get('headers', [])
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
                date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
                
                # Get body (simplified)
                body = ''
                if 'parts' in msg['payload']:
                    for part in msg['payload']['parts']:
                        if part['mimeType'] == 'text/plain':
                            body = base64.urlsafe_b64decode(
                                part['body']['data']
                            ).decode('utf-8')
                            break
                
                email_list.append({
                    'id': message['id'],
                    'thread_id': msg['threadId'],
                    'subject': subject,
                    'sender': sender,
                    'date': date,
                    'body': body
                })
            
            return email_list
            
        except HttpError as error:
            logger.error(f'Error fetching emails: {error}')
            return []
    
    def get_authenticated_email(self) -> str:
        """Get the email of the currently authenticated user (backwards compatibility)"""
        try:
            # Try legacy service first
            if self.gmail_service:
                profile = self.gmail_service.users().getProfile(userId='me').execute()
                return profile.get('emailAddress', '')
            
            # Use first authenticated user
            authenticated_users = self.get_authenticated_users()
            if authenticated_users:
                return authenticated_users[0]
            
            logger.warning("No authenticated users found")
            return ''
        except Exception as e:
            logger.error(f"Failed to get authenticated email: {e}")
            return ''
    
    def validate_services(self) -> Dict[str, bool]:
        """Validate that services are working for authenticated users"""
        calendar_working = False
        gmail_working = False
        authenticated_users = self.get_authenticated_users()
        
        if authenticated_users:
            # Test with first authenticated user
            test_user = authenticated_users[0]
            
            try:
                # Test Calendar API
                calendar_service = self.get_user_service(test_user, 'calendar')
                if calendar_service:
                    calendar_service.calendarList().list().execute()
                    calendar_working = True
            except Exception as e:
                logger.error(f"Calendar API validation failed for {test_user}: {e}")
            
            try:
                # Test Gmail API
                gmail_service = self.get_user_service(test_user, 'gmail')
                if gmail_service:
                    gmail_service.users().getProfile(userId='me').execute()
                    gmail_working = True
            except Exception as e:
                logger.error(f"Gmail API validation failed for {test_user}: {e}")
        
        # Also test legacy services if available
        legacy_calendar = False
        legacy_gmail = False
        
        if self.calendar_service:
            try:
                self.calendar_service.calendarList().list().execute()
                legacy_calendar = True
            except Exception as e:
                logger.error(f"Legacy Calendar API validation failed: {e}")
        
        if self.gmail_service:
            try:
                self.gmail_service.users().getProfile(userId='me').execute()
                legacy_gmail = True
            except Exception as e:
                logger.error(f"Legacy Gmail API validation failed: {e}")
        
        return {
            'calendar': calendar_working or legacy_calendar,
            'gmail': gmail_working or legacy_gmail,
            'authenticated': (calendar_working and gmail_working) or (legacy_calendar and legacy_gmail),
            'multi_user_calendar': calendar_working,
            'multi_user_gmail': gmail_working,
            'legacy_calendar': legacy_calendar,
            'legacy_gmail': legacy_gmail,
            'authenticated_users_count': len(authenticated_users)
        } 