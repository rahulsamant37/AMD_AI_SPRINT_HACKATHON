"""
Calendar API Routes

Enhanced calendar endpoints with multi-user authentication support:
1. Get current user email from Google APIs
2. Get upcoming meetings with multi-user access control
3. Check availability for participants with access validation
4. Manage authenticated users (list, add, remove)

Supports both legacy single-user and new multi-user authentication.
"""

from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_agent_service, get_google_service
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/current-user")
async def get_current_user():
    """
    Get the current user's email address from Google APIs
    
    For multi-user system, returns the primary authenticated user.
    For legacy system, returns the single authenticated user.
    """
    try:
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials
        import pickle
        import os
        
        # Load credentials from token file
        token_file = "token.pickle"
        if not os.path.exists(token_file):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No credentials found. Please run authentication first."
            )
        
        with open(token_file, 'rb') as token:
            credentials = pickle.load(token)
        
        # Get user info from Google
        service = build('oauth2', 'v2', credentials=credentials)
        user_info = service.userinfo().get().execute()
        
        email = user_info.get('email', '')
        name = user_info.get('name', '')
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not retrieve user email from Google"
            )
        
        return {
            "email": email,
            "name": name,
            "message": f"Current user: {name} ({email})"
        }
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Error getting current user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get current user: {str(e)}"
        )


@router.get("/authenticated-users")
async def get_authenticated_users(google_service = Depends(get_google_service)):
    """
    Get list of all authenticated users
    
    Returns all users who have valid Google API credentials.
    """
    try:
        authenticated_users = google_service.get_authenticated_users()
        current_user = google_service.get_authenticated_email()
        
        return {
            "authenticated_users": authenticated_users,
            "current_user": current_user,
            "total_count": len(authenticated_users),
            "note": "All these users' calendars can be accessed"
        }
        
    except Exception as e:
        logger.error(f"Error getting authenticated users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get authenticated users: {str(e)}"
        )


@router.post("/authenticate-user")
async def authenticate_new_user(google_service = Depends(get_google_service)):
    """
    Authenticate a new user using OAuth2 flow
    
    Starts the Google OAuth2 authentication process for a new user.
    Returns the authenticated user's email if successful.
    """
    try:
        logger.info("Starting authentication flow for new user...")
        
        authenticated_email = google_service.authenticate_new_user()
        
        if authenticated_email:
            authenticated_users = google_service.get_authenticated_users()
            return {
                "success": True,
                "message": f"Successfully authenticated user: {authenticated_email}",
                "authenticated_email": authenticated_email,
                "total_authenticated_users": len(authenticated_users),
                "all_authenticated_users": authenticated_users
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to authenticate new user. Please check your credentials and try again."
            )
            
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Error authenticating new user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to authenticate new user: {str(e)}"
        )


@router.delete("/authenticated-user/{email}")
async def remove_authenticated_user(email: str, google_service = Depends(get_google_service)):
    """
    Remove an authenticated user
    
    Removes the user's credentials and access permissions.
    """
    try:
        logger.info(f"Removing authentication for user: {email}")
        
        # Check if user is currently authenticated
        if not google_service.is_user_authenticated(email):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User '{email}' is not currently authenticated"
            )
        
        success = google_service.remove_user_authentication(email)
        
        if success:
            remaining_users = google_service.get_authenticated_users()
            return {
                "success": True,
                "message": f"Successfully removed authentication for user: {email}",
                "removed_email": email,
                "remaining_authenticated_users": remaining_users,
                "remaining_count": len(remaining_users)
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to remove authentication for user: {email}"
            )
            
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Error removing authenticated user {email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to remove authenticated user: {str(e)}"
        )


@router.get("/upcoming")
async def get_upcoming_meetings(
    user_email: Optional[str] = None,  # Optional: specify which authenticated user's calendar to access
    days_ahead: int = 7,
    agent = Depends(get_agent_service)
):
    """
    Get upcoming meetings from calendar with multi-user support
    
    **Parameters:**
    - user_email: Email of authenticated user whose calendar to access (optional)
    - days_ahead: Number of days ahead to fetch (1-30, default: 7)
    
    **Access Control:**
    - If user_email is provided, that user must be authenticated
    - If user_email is not provided, uses the first available authenticated user
    """
    
    try:
        if days_ahead < 1 or days_ahead > 30:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="days_ahead must be between 1 and 30"
            )
        
        # Check authenticated users
        authenticated_users = agent.google_service.get_authenticated_users()
        if not authenticated_users:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No authenticated users found. Please authenticate at least one user first."
            )
        
        # Determine which user's calendar to access
        if user_email:
            if not agent.google_service.is_user_authenticated(user_email):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"User '{user_email}' is not authenticated. Available authenticated users: {authenticated_users}"
                )
            target_user = user_email
        else:
            # Use first authenticated user if none specified
            target_user = authenticated_users[0]
        
        logger.info(f"Fetching upcoming meetings for authenticated user: {target_user}")
        
        start_date = datetime.now()
        end_date = start_date.replace(hour=23, minute=59, second=59) + timedelta(days=days_ahead)
        
        # Call Google Calendar API for the specific authenticated user
        try:
            events = agent.google_service.get_calendar_events(start_date, end_date, target_user)
        except Exception as e:
            # Check if it's a Google API error indicating access denied
            error_str = str(e).lower()
            if 'forbidden' in error_str or 'access denied' in error_str or '403' in str(e):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied to calendar for user '{target_user}'. The user may not be authenticated or you may not have permission to access their calendar."
                )
            elif 'not found' in error_str or '404' in str(e):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Calendar not found for user '{target_user}'. The user may not exist or their calendar may not be accessible."
                )
            elif 'unauthorized' in error_str or '401' in str(e):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Unauthorized access to calendar for user '{target_user}'. Authentication may have expired."
                )
            else:
                # Generic error
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to fetch calendar for user '{target_user}': {str(e)}"
                )
        
        meetings = [
            {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "start_time": event.start_time.isoformat(),
                "end_time": event.end_time.isoformat(),
                "attendees": event.attendees,
                "location": event.location,
                "formatted": f"{event.start_time.strftime('%A, %B %d at %I:%M %p')} - {event.end_time.strftime('%I:%M %p')}"
            }
            for event in events
        ]
        
        return {
            "meetings": meetings,
            "total_count": len(meetings),
            "queried_user": target_user,
            "authenticated_users": authenticated_users,
            "date_range": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
                "days": days_ahead
            },
            "access_control": {
                "requested_user": user_email,
                "accessed_user": target_user,
                "is_authenticated": True
            }
        }
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Error fetching upcoming meetings: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch upcoming meetings: {str(e)}"
        )


@router.get("/availability")
async def get_calendar_availability(
    participant_emails: str,  # Comma-separated emails
    days_ahead: int = 7,
    duration_minutes: int = 30,
    agent = Depends(get_agent_service)
):
    """
    Check calendar availability for participants with multi-user access control
    
    **Parameters:**
    - participant_emails: Comma-separated email addresses (e.g., "user1@gmail.com,user2@gmail.com")
    - days_ahead: Number of days ahead to check (1-30, default: 7)
    - duration_minutes: Meeting duration in minutes (15-480, default: 30)
    
    **Access Control:**
    - Only authenticated users' calendars will show real availability data
    - Non-authenticated users will show empty availability
    - Clear reporting of which users are accessible vs denied
    """
    
    try:
        if days_ahead < 1 or days_ahead > 30:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="days_ahead must be between 1 and 30"
            )
        
        if duration_minutes < 15 or duration_minutes > 480:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="duration_minutes must be between 15 and 480"
            )
        
        # Parse participant emails
        emails = [email.strip() for email in participant_emails.split(",") if email.strip()]
        if not emails:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one participant email is required"
            )
        
        logger.info(f"Checking availability for {len(emails)} participants: {emails}")
        
        # Get access control information
        authenticated_users = agent.google_service.get_authenticated_users()
        access_report = agent.google_service.auth_manager.validate_access(emails)
        
        logger.info(f"Access control - Accessible: {access_report['accessible_users']}, Denied: {access_report['denied_users']}")
        
        # Calculate date range
        start_date = datetime.now()
        end_date = start_date + timedelta(days=days_ahead)
        
        # Get availability data directly from Google Calendar with multi-user support
        availability_result = agent._get_calendar_availability(
            emails, 
            start_date.isoformat(), 
            end_date.isoformat(), 
            duration_minutes
        )
        
        if not availability_result.get("success", False):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=availability_result.get("error", "Failed to fetch availability")
            )
        
        return {
            "success": True,
            "availability_data": availability_result.get("availability_data", []),
            "participants": emails,
            "duration_minutes": duration_minutes,
            "date_range": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
                "days": days_ahead
            },
            "access_control": {
                **access_report,
                "authenticated_users": authenticated_users,
                "note": "Only authenticated users show real availability data"
            }
        }
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Error checking calendar availability: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check availability: {str(e)}"
        ) 