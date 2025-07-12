"""
SchedulAI Services Module

This module contains the core services for the SchedulAI application:
- GoogleService: Unified Google Calendar and Gmail API integration
- VLLMService: vLLM DeepSeek LLM service for AI capabilities
- SchedulingAgent: AI agent with vLLM function calling capabilities

The services follow a clean architecture pattern with proper separation of concerns.
"""

from app.services.google_service import GoogleService
from app.services.vllm_service import VLLMService
from app.services.agent_service import SchedulingAgent

__all__ = [
    "GoogleService",
    "VLLMService", 
    "SchedulingAgent"
]

# Service factory functions for dependency injection
def create_google_service() -> GoogleService:
    """Factory function to create GoogleService instance"""
    return GoogleService()

def create_scheduling_agent() -> SchedulingAgent:
    """Factory function to create SchedulingAgent instance"""
    return SchedulingAgent() 