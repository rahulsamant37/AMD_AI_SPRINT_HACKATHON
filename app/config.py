import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration management"""
    
    # ===== API Configuration =====
    API_HOST: str = os.getenv("API_HOST", "localhost")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # ===== vLLM DeepSeek Configuration =====
    VLLM_BASE_URL: str = os.getenv("VLLM_BASE_URL", "http://localhost:3000")
    VLLM_MODEL_PATH: str = os.getenv("VLLM_MODEL_PATH", "/home/user/Models/deepseek-ai/deepseek-llm-7b-chat")
    VLLM_TEMPERATURE: float = float(os.getenv("VLLM_TEMPERATURE", "0.3"))
    VLLM_MAX_TOKENS: int = int(os.getenv("VLLM_MAX_TOKENS", "2000"))
    
    # ===== Google APIs Configuration =====
    GOOGLE_CREDENTIALS_FILE: str = os.getenv(
        "GOOGLE_CREDENTIALS_FILE", 
        "credentials.json"
    )
    GOOGLE_TOKEN_FILE: str = os.getenv(
        "GOOGLE_TOKEN_FILE", 
        "token.pickle"
    )
    
    # Legacy support (backwards compatibility)
    GOOGLE_CALENDAR_CREDENTIALS_FILE: str = os.getenv(
        "GOOGLE_CALENDAR_CREDENTIALS_FILE", 
        os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
    )
    GOOGLE_CALENDAR_TOKEN_FILE: str = os.getenv(
        "GOOGLE_CALENDAR_TOKEN_FILE", 
        os.getenv("GOOGLE_TOKEN_FILE", "token.pickle")
    )
    
    # Google API Scopes
    GOOGLE_SCOPES: list = [
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/userinfo.email',
        'openid'
    ]
    
    # ===== Scheduling Configuration =====
    DEFAULT_MEETING_DURATION: int = int(os.getenv("DEFAULT_MEETING_DURATION", "30"))
    DEFAULT_BUFFER_TIME: int = int(os.getenv("DEFAULT_BUFFER_TIME", "15"))
    DEFAULT_WORK_START_HOUR: int = int(os.getenv("DEFAULT_WORK_START_HOUR", "9"))
    DEFAULT_WORK_END_HOUR: int = int(os.getenv("DEFAULT_WORK_END_HOUR", "18"))
    DEFAULT_TIMEZONE: str = os.getenv("DEFAULT_TIMEZONE", "UTC")
    
    # ===== Agent Configuration =====
    AGENT_MAX_RETRIES: int = int(os.getenv("AGENT_MAX_RETRIES", "3"))
    AGENT_TIMEOUT_SECONDS: int = int(os.getenv("AGENT_TIMEOUT_SECONDS", "30"))
    MAX_MEETING_SUGGESTIONS: int = int(os.getenv("MAX_MEETING_SUGGESTIONS", "3"))
    
    # ===== Email Configuration =====
    EMAIL_SENDER_NAME: str = os.getenv("EMAIL_SENDER_NAME", "SchedulAI")
    EMAIL_REPLY_TO: Optional[str] = os.getenv("EMAIL_REPLY_TO")
    
    # ===== Calendar Configuration =====
    CALENDAR_LOOKAHEAD_DAYS: int = int(os.getenv("CALENDAR_LOOKAHEAD_DAYS", "14"))
    CALENDAR_MAX_EVENTS_PER_REQUEST: int = int(os.getenv("CALENDAR_MAX_EVENTS_PER_REQUEST", "100"))
    
    # ===== Security Configuration =====
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    # ===== Feature Flags =====
    ENABLE_EMAIL_SENDING: bool = os.getenv("ENABLE_EMAIL_SENDING", "true").lower() == "true"
    ENABLE_CALENDAR_CREATION: bool = os.getenv("ENABLE_CALENDAR_CREATION", "true").lower() == "true"
    ENABLE_AI_REASONING: bool = os.getenv("ENABLE_AI_REASONING", "true").lower() == "true"
    
    # ===== Logging Configuration =====
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv(
        "LOG_FORMAT", 
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    @classmethod
    def validate_required_config(cls) -> list[str]:
        """Validate that all required configuration is present"""
        missing_configs = []
        
        # Required configurations for vLLM
        required_configs = {
            "VLLM_BASE_URL": cls.VLLM_BASE_URL,
            "VLLM_MODEL_PATH": cls.VLLM_MODEL_PATH,
            "GOOGLE_CREDENTIALS_FILE": cls.GOOGLE_CREDENTIALS_FILE,
        }
        
        for config_name, config_value in required_configs.items():
            if not config_value:
                missing_configs.append(config_name)
        
        # Check if credentials file exists
        if cls.GOOGLE_CREDENTIALS_FILE and not Path(cls.GOOGLE_CREDENTIALS_FILE).exists():
            missing_configs.append(f"GOOGLE_CREDENTIALS_FILE (file not found: {cls.GOOGLE_CREDENTIALS_FILE})")
        
        return missing_configs
    
    @classmethod
    def get_environment_info(cls) -> dict:
        """Get current environment configuration info"""
        return {
            "api_host": cls.API_HOST,
            "api_port": cls.API_PORT,
            "debug_mode": cls.DEBUG,
            "vllm_base_url": cls.VLLM_BASE_URL,
            "vllm_model_path": cls.VLLM_MODEL_PATH,
            "vllm_temperature": cls.VLLM_TEMPERATURE,
            "credentials_file": cls.GOOGLE_CREDENTIALS_FILE,
            "token_file": cls.GOOGLE_TOKEN_FILE,
            "default_timezone": cls.DEFAULT_TIMEZONE,
            "feature_flags": {
                "email_sending": cls.ENABLE_EMAIL_SENDING,
                "calendar_creation": cls.ENABLE_CALENDAR_CREATION,
                "ai_reasoning": cls.ENABLE_AI_REASONING,
            }
        }

# Create global config instance
config = Config()

# Validation on import
missing_configs = config.validate_required_config()
if missing_configs and not os.getenv("SKIP_CONFIG_VALIDATION"):
    print("⚠️  Missing required configuration:")
    for missing in missing_configs:
        print(f"   - {missing}")
    print("\nPlease check your .env file and ensure all required values are set.")
    print("Set SKIP_CONFIG_VALIDATION=true to bypass this check during setup.") 