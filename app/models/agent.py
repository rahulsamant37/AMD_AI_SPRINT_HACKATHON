"""
AI Agent-related Pydantic models

Contains models for vLLM DeepSeek function calling and agent interactions.
"""

from typing import List, Dict, Any
from pydantic import BaseModel


class FunctionCall(BaseModel):
    """vLLM function call representation"""
    name: str
    arguments: Dict[str, Any]


class ToolCall(BaseModel):
    """vLLM tool call representation"""
    id: str
    type: str = "function"
    function: FunctionCall


class AgentResponse(BaseModel):
    """AI agent response model"""
    message: str
    tool_calls: List[ToolCall] = []
    reasoning: str
    confidence: float = 0.0


class AgentAction(BaseModel):
    """Agent action representation"""
    action_type: str  # "get_availability", "send_email", "create_event", etc.
    parameters: Dict[str, Any]
    reasoning: str 