"""
vLLM Service for DeepSeek LLM Integration

This service provides interface for communicating with vLLM server
running DeepSeek models for AI-powered function calling.
"""

import json
import requests
import re
from typing import List, Dict, Any, Optional
from app.config import config
from app.core.logging import get_logger

logger = get_logger(__name__)

class MockMessage:
    """Mock message class to mimic chat completion response structure"""
    def __init__(self, content: str, tool_calls: Optional[List] = None):
        self.content = content
        self.tool_calls = tool_calls or []

class MockChoice:
    """Mock choice class to mimic chat completion response structure"""
    def __init__(self, message: MockMessage):
        self.message = message

class MockResponse:
    """Mock response class to mimic chat completion response structure"""
    def __init__(self, choices: List[MockChoice]):
        self.choices = choices

class VLLMService:
    """Service for communicating with vLLM server running DeepSeek models"""
    
    def __init__(self):
        self.base_url = config.VLLM_BASE_URL
        self.model_path = config.VLLM_MODEL_PATH
        self.temperature = config.VLLM_TEMPERATURE
        self.max_tokens = config.VLLM_MAX_TOKENS
        
        logger.info(f"Initializing vLLM service with base URL: {self.base_url}")
        logger.debug(f"Model path: {self.model_path}")
        
    def create_chat_completion(self, 
                             messages: List[Dict[str, str]], 
                             tools: Optional[List[Dict[str, Any]]] = None,
                             tool_choice: Optional[str] = None,
                             temperature: Optional[float] = None,
                             max_tokens: Optional[int] = None,
                             stream: bool = False) -> Any:
        """
        Create a chat completion using vLLM server.
        Compatible with standard chat completions API format.
        """
        
        # If tools are provided, we need to handle function calling
        if tools and tool_choice == "auto":
            return self._handle_function_calling(messages, tools, temperature, max_tokens)
        
        # Standard completion without function calling
        return self._create_standard_completion(messages, temperature, max_tokens, stream)
    
    def _create_standard_completion(self, 
                                  messages: List[Dict[str, str]], 
                                  temperature: Optional[float] = None,
                                  max_tokens: Optional[int] = None,
                                  stream: bool = False) -> Dict[str, Any]:
        """Create a standard completion without function calling"""
        
        url = f"{self.base_url}/v1/chat/completions"
        headers = {"Content-Type": "application/json"}
        
        # Prepare the request data
        data = {
            "model": self.model_path,
            "messages": messages,
            "stream": stream,
            "temperature": temperature or self.temperature,
            "max_tokens": max_tokens or self.max_tokens
        }
                
        logger.debug(f"Sending request to vLLM server: {url}")
        logger.debug(f"Request data: {json.dumps(data, indent=2)}")
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            logger.debug(f"vLLM response: {json.dumps(result, indent=2)}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error communicating with vLLM server: {e}")
            raise Exception(f"vLLM server communication error: {e}")
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing vLLM response: {e}")
            raise Exception(f"Invalid JSON response from vLLM server: {e}")
    
    def _handle_function_calling(self, 
                               messages: List[Dict[str, str]], 
                               tools: List[Dict[str, Any]],
                               temperature: Optional[float] = None,
                               max_tokens: Optional[int] = None) -> MockResponse:
        """
        Handle function calling by instructing the model to respond with function calls.
        Since vLLM might not support native function calling, we use prompt engineering.
        """
        
        # Create a system message that instructs the model about available functions
        function_descriptions = []
        for tool in tools:
            func = tool["function"]
            function_descriptions.append(f"""
Function: {func["name"]}
Description: {func["description"]}
Parameters: {json.dumps(func["parameters"], indent=2)}
""")
        
        function_prompt = f"""
You are an AI agent with access to the following functions. When you need to call a function, respond with a JSON object in this exact format:

{{
  "function_calls": [
    {{
      "id": "call_123",
      "function": {{
        "name": "function_name",
        "arguments": "{{\"param1\": \"value1\", \"param2\": \"value2\"}}"
      }}
    }}
  ]
}}

Available functions:
{chr(10).join(function_descriptions)}

Important: 
1. Always call the appropriate functions to help with scheduling meetings
2. Start by calling get_calendar_availability to check participant availability
3. Then call analyze_optimal_slots to find the best meeting times
4. Always respond with valid JSON when calling functions
5. Include reasoning for your choices
"""
        
        # Add the function calling instruction to the system message
        enhanced_messages = []
        for msg in messages:
            if msg["role"] == "system":
                enhanced_messages.append({
                    "role": "system",
                    "content": msg["content"] + "\n\n" + function_prompt
                })
            else:
                enhanced_messages.append(msg)
        
        # If no system message exists, add one
        if not any(msg["role"] == "system" for msg in enhanced_messages):
            enhanced_messages.insert(0, {
                "role": "system", 
                "content": function_prompt
            })
        
        # Get response from vLLM
        raw_response = self._create_standard_completion(
            enhanced_messages, 
            temperature, 
            max_tokens or 1000
        )
        
        # Parse the response and extract function calls
        content = raw_response["choices"][0]["message"]["content"]
        logger.debug(f"Raw model response: {content}")
        
        # Try to extract function calls from the response
        tool_calls = self._extract_function_calls(content)
        
        # Create mock response in standard format
        mock_message = MockMessage(content=content, tool_calls=tool_calls)
        mock_choice = MockChoice(message=mock_message)
        
        return MockResponse(choices=[mock_choice])
    
    def _extract_function_calls(self, content: str) -> List[Any]:
        """Extract function calls from model response"""
        
        class MockFunction:
            def __init__(self, name: str, arguments: str):
                self.name = name
                self.arguments = arguments
                
        class MockToolCall:
            def __init__(self, call_id: str, function: MockFunction):
                self.id = call_id
                self.function = function
        
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                parsed = json.loads(json_str)
                
                if "function_calls" in parsed:
                    tool_calls = []
                    for call in parsed["function_calls"]:
                        mock_func = MockFunction(
                            name=call["function"]["name"],
                            arguments=call["function"]["arguments"]
                        )
                        mock_call = MockToolCall(
                            call_id=call.get("id", f"call_{len(tool_calls)}"),
                            function=mock_func
                        )
                        tool_calls.append(mock_call)
                    
                    logger.debug(f"Extracted {len(tool_calls)} function calls")
                    return tool_calls
            
            # If no function calls found, try to infer from content
            # This is a fallback for when the model doesn't follow the exact format
            if "get_calendar_availability" in content.lower():
                logger.info("Detected calendar availability request, creating function call")
                # Create a default function call for calendar availability
                mock_func = MockFunction(
                    name="get_calendar_availability",
                    arguments='{"participant_emails": [], "start_date": "", "end_date": "", "duration_minutes": 60}'
                )
                mock_call = MockToolCall(call_id="call_1", function=mock_func)
                return [mock_call]
                
        except Exception as e:
            logger.warning(f"Error extracting function calls: {e}")
        
        logger.warning("No function calls detected in model response")
        return []
    
    def health_check(self) -> bool:
        """Check if vLLM server is healthy and responding"""
        try:
            # Try a simple request to check server status
            test_messages = [
                {"role": "user", "content": "Hello"}
            ]
            
            response = self._create_standard_completion(
                messages=test_messages,
                max_tokens=10,
                temperature=0.1
            )
            
            # Check if response has expected structure
            if "choices" in response and len(response["choices"]) > 0:
                logger.info("vLLM server health check: OK")
                return True
            else:
                logger.warning("vLLM server health check: Unexpected response format")
                return False
                
        except Exception as e:
            logger.error(f"vLLM server health check failed: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        return {
            "base_url": self.base_url,
            "model_path": self.model_path,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "service_type": "vLLM DeepSeek"
        }
