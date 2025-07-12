"""
Authentication Manager for Multi-User Google API Access

Manages multiple authenticated Google accounts with secure credential storage,
automatic validation, and refresh capabilities.
"""

import json
import os
import pickle
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.credentials import Credentials
from googleapiclient.errors import HttpError

from app.config import config
from app.core.logging import get_logger
from app.core.exceptions import GoogleServiceException

logger = get_logger(__name__)


@dataclass
class UserAuthInfo:
    """User authentication information"""
    email: str
    authenticated_at: datetime
    last_validated: datetime
    is_valid: bool
    credential_file: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'email': self.email,
            'authenticated_at': self.authenticated_at.isoformat(),
            'last_validated': self.last_validated.isoformat(),
            'is_valid': self.is_valid,
            'credential_file': self.credential_file
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'UserAuthInfo':
        """Create from dictionary"""
        return cls(
            email=data['email'],
            authenticated_at=datetime.fromisoformat(data['authenticated_at']),
            last_validated=datetime.fromisoformat(data['last_validated']),
            is_valid=data['is_valid'],
            credential_file=data['credential_file']
        )


class AuthenticationManager:
    """Manages multiple Google user authentications"""
    
    def __init__(self):
        self.user_tokens_dir = Path("user_tokens")
        self.auth_users_file = "authenticated_users.json"
        self.validation_cache_duration = timedelta(hours=1)  # Cache validation for 1 hour
        
        # Ensure directories exist
        self.user_tokens_dir.mkdir(exist_ok=True)
        
        # Load existing user data
        self._authenticated_users: Dict[str, UserAuthInfo] = {}
        self._load_authenticated_users()
        
        logger.info(f"AuthenticationManager initialized with {len(self._authenticated_users)} users")
    
    def _load_authenticated_users(self) -> None:
        """Load authenticated users from storage"""
        try:
            if os.path.exists(self.auth_users_file):
                with open(self.auth_users_file, 'r') as f:
                    data = json.load(f)
                    for email, user_data in data.items():
                        self._authenticated_users[email] = UserAuthInfo.from_dict(user_data)
                logger.info(f"Loaded {len(self._authenticated_users)} authenticated users from storage")
            else:
                logger.info("No existing authenticated users file found")
        except Exception as e:
            logger.error(f"Failed to load authenticated users: {e}")
            self._authenticated_users = {}
    
    def _save_authenticated_users(self) -> None:
        """Save authenticated users to storage"""
        try:
            data = {email: user_info.to_dict() for email, user_info in self._authenticated_users.items()}
            with open(self.auth_users_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.debug("Authenticated users saved to storage")
        except Exception as e:
            logger.error(f"Failed to save authenticated users: {e}")
    
    def _get_user_token_file(self, email: str) -> str:
        """Get the token file path for a user"""
        safe_email = email.replace('@', '_at_').replace('.', '_dot_')
        return str(self.user_tokens_dir / f"{safe_email}.pickle")
    
    def _load_user_credentials(self, email: str) -> Optional[Credentials]:
        """Load credentials for a specific user"""
        token_file = self._get_user_token_file(email)
        
        if not os.path.exists(token_file):
            logger.debug(f"No token file found for user: {email}")
            return None
        
        try:
            with open(token_file, 'rb') as f:
                creds = pickle.load(f)
            logger.debug(f"Loaded credentials for user: {email}")
            return creds
        except Exception as e:
            logger.error(f"Failed to load credentials for {email}: {e}")
            return None
    
    def _save_user_credentials(self, email: str, credentials: Credentials) -> bool:
        """Save credentials for a specific user"""
        token_file = self._get_user_token_file(email)
        
        try:
            with open(token_file, 'wb') as f:
                pickle.dump(credentials, f)
            logger.debug(f"Saved credentials for user: {email}")
            return True
        except Exception as e:
            logger.error(f"Failed to save credentials for {email}: {e}")
            return False
    
    def _validate_credentials(self, credentials: Credentials) -> bool:
        """Validate if credentials are still valid"""
        try:
            if not credentials.valid:
                if credentials.expired and credentials.refresh_token:
                    logger.debug("Refreshing expired credentials")
                    credentials.refresh(Request())
                    return credentials.valid
                return False
            return True
        except Exception as e:
            logger.error(f"Failed to validate credentials: {e}")
            return False
    
    def _get_user_email_from_credentials(self, credentials: Credentials) -> Optional[str]:
        """Get user email from credentials"""
        try:
            service = build('oauth2', 'v2', credentials=credentials)
            user_info = service.userinfo().get().execute()
            return user_info.get('email')
        except Exception as e:
            logger.error(f"Failed to get user email from credentials: {e}")
            return None
    
    def is_user_authenticated(self, email: str) -> bool:
        """Check if a user is authenticated with valid credentials"""
        if email not in self._authenticated_users:
            return False
        
        user_info = self._authenticated_users[email]
        
        # Check if we need to validate (cache expired)
        if datetime.now() - user_info.last_validated > self.validation_cache_duration:
            logger.debug(f"Validating credentials for {email} (cache expired)")
            credentials = self._load_user_credentials(email)
            
            if not credentials:
                user_info.is_valid = False
            else:
                user_info.is_valid = self._validate_credentials(credentials)
                if user_info.is_valid:
                    # Save refreshed credentials if they were updated
                    self._save_user_credentials(email, credentials)
            
            user_info.last_validated = datetime.now()
            self._save_authenticated_users()
        
        return user_info.is_valid
    
    def get_user_credentials(self, email: str) -> Optional[Credentials]:
        """Get valid credentials for a specific user"""
        if not self.is_user_authenticated(email):
            logger.warning(f"User {email} is not authenticated or has invalid credentials")
            return None
        
        credentials = self._load_user_credentials(email)
        if credentials and self._validate_credentials(credentials):
            # Save potentially refreshed credentials
            self._save_user_credentials(email, credentials)
            return credentials
        
        logger.error(f"Failed to get valid credentials for {email}")
        return None
    
    def authenticate_new_user(self, credentials_file: str = None) -> Optional[str]:
        """Authenticate a new user using OAuth2 flow"""
        creds_file = credentials_file or config.GOOGLE_CREDENTIALS_FILE
        
        if not os.path.exists(creds_file):
            logger.error(f"Credentials file not found: {creds_file}")
            raise FileNotFoundError(f"Credentials file not found: {creds_file}")
        
        try:
            logger.info("Starting OAuth2 flow for new user authentication...")
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, config.GOOGLE_SCOPES)
            credentials = flow.run_local_server(port=0)
            
            # Get user email
            email = self._get_user_email_from_credentials(credentials)
            logger.info(f"User email: {email}")
            if not email:
                logger.error("Failed to get user email from new credentials")
                return None
            
            # Save credentials
            if not self._save_user_credentials(email, credentials):
                logger.error(f"Failed to save credentials for new user: {email}")
                return None
            
            # Add to authenticated users
            user_info = UserAuthInfo(
                email=email,
                authenticated_at=datetime.now(),
                last_validated=datetime.now(),
                is_valid=True,
                credential_file=self._get_user_token_file(email)
            )
            
            self._authenticated_users[email] = user_info
            self._save_authenticated_users()
            
            logger.info(f"Successfully authenticated new user: {email}")
            return email
            
        except Exception as e:
            logger.error(f"Failed to authenticate new user: {e}")
            return None
    
    def add_existing_credentials(self, email: str, credentials: Credentials) -> bool:
        """Add existing credentials for a user (for migration)"""
        try:
            # Validate credentials
            if not self._validate_credentials(credentials):
                logger.error(f"Invalid credentials provided for {email}")
                return False
            
            # Save credentials
            if not self._save_user_credentials(email, credentials):
                logger.error(f"Failed to save credentials for {email}")
                return False
            
            # Add to authenticated users
            user_info = UserAuthInfo(
                email=email,
                authenticated_at=datetime.now(),
                last_validated=datetime.now(),
                is_valid=True,
                credential_file=self._get_user_token_file(email)
            )
            
            self._authenticated_users[email] = user_info
            self._save_authenticated_users()
            
            logger.info(f"Successfully added existing credentials for user: {email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add existing credentials for {email}: {e}")
            return False
    
    def remove_user_authentication(self, email: str) -> bool:
        """Remove a user's authentication and credentials"""
        try:
            # Remove credentials file
            token_file = self._get_user_token_file(email)
            if os.path.exists(token_file):
                os.remove(token_file)
                logger.debug(f"Removed credentials file for {email}")
            
            # Remove from authenticated users
            if email in self._authenticated_users:
                del self._authenticated_users[email]
                self._save_authenticated_users()
                logger.info(f"Removed authentication for user: {email}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to remove authentication for {email}: {e}")
            return False
    
    def get_authenticated_users(self) -> List[str]:
        """Get list of all authenticated user emails"""
        # Filter only valid users
        valid_users = [
            email for email, user_info in self._authenticated_users.items()
            if self.is_user_authenticated(email)
        ]
        return valid_users
    
    def get_accessible_emails(self, requested_emails: List[str]) -> Dict[str, bool]:
        """Check which emails from the list are accessible (authenticated)"""
        return {
            email: self.is_user_authenticated(email)
            for email in requested_emails
        }
    
    def validate_access(self, emails: List[str]) -> Dict[str, any]:
        """Validate access for multiple emails and return detailed report"""
        accessible = []
        denied = []
        
        for email in emails:
            if self.is_user_authenticated(email):
                accessible.append(email)
            else:
                denied.append(email)
        
        return {
            'total_requested': len(emails),
            'accessible_users': accessible,
            'denied_users': denied,
            'accessible_count': len(accessible),
            'denied_count': len(denied)
        }
    
    def get_current_primary_user(self) -> Optional[str]:
        """Get the first valid authenticated user (for backwards compatibility)"""
        authenticated_users = self.get_authenticated_users()
        return authenticated_users[0] if authenticated_users else None
    
    def migrate_legacy_token(self, legacy_token_file: str = "token.pickle") -> bool:
        """Migrate existing token.pickle to new multi-user system"""
        if not os.path.exists(legacy_token_file):
            logger.info("No legacy token file to migrate")
            return True
        
        try:
            # Load legacy credentials
            with open(legacy_token_file, 'rb') as f:
                credentials = pickle.load(f)
            
            # Get user email
            email = self._get_user_email_from_credentials(credentials)
            if not email:
                logger.error("Failed to get email from legacy credentials")
                return False
            
            # Add to new system
            success = self.add_existing_credentials(email, credentials)
            
            if success:
                logger.info(f"Successfully migrated legacy credentials for: {email}")
                # Optionally backup the legacy file
                backup_file = f"{legacy_token_file}.backup"
                os.rename(legacy_token_file, backup_file)
                logger.info(f"Legacy token file backed up as: {backup_file}")
                return True
            else:
                logger.error("Failed to migrate legacy credentials")
                return False
                
        except Exception as e:
            logger.error(f"Failed to migrate legacy token: {e}")
            return False


# Singleton instance
_auth_manager: Optional[AuthenticationManager] = None


def get_auth_manager() -> AuthenticationManager:
    """Get or create the authentication manager singleton"""
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthenticationManager()
        # Migrate legacy token on first initialization
        _auth_manager.migrate_legacy_token()
    return _auth_manager 