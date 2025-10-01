import os
from anthropic import Anthropic
from typing import Dict, Optional, List
import asyncio

class AnthropicService:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=api_key) if api_key else None
        # Default to a widely available recent model
        self.default_model = "claude-3-7-sonnet-20250219"
        # Map friendly names/aliases to exact API model IDs
        self.model_aliases: Dict[str, str] = {
            "sonnet-3.7": "claude-3-7-sonnet-20250219",
            "claude-3.7-sonnet": "claude-3-7-sonnet-20250219",
            "claude-3-7-sonnet": "claude-3-7-sonnet-20250219",
            "sonnet-4": "claude-sonnet-4-20250514",
            "claude-sonnet-4": "claude-sonnet-4-20250514",
            "opus-4": "claude-opus-4-20250514",
            "claude-opus-4": "claude-opus-4-20250514",
            "opus-4.1": "claude-opus-4-1-20250805",
            "claude-opus-4.1": "claude-opus-4-1-20250805",
            "haiku-3.5": "claude-3-5-haiku-20241022",
            "claude-3.5-haiku": "claude-3-5-haiku-20241022",
            # legacy
            "haiku-3": "claude-3-haiku-20240307",
            "claude-3-haiku": "claude-3-haiku-20240307",
        }

    def _resolve_model(self, model: Optional[str]) -> str:
        if not model:
            return self.default_model
        # exact string if provided
        if model in self.model_aliases:
            return self.model_aliases[model]
        return model
    
    async def generate(
        self,
        text: str,
        model: Optional[str] = None,
        max_tokens: int = 150,
        temperature: float = 0.7,
        system_prompt: str = "You are a helpful AI assistant."
    ) -> Dict:
        """
        Generate a response using Anthropic's Claude API
        """
        if not self.is_available():
            raise Exception("Anthropic API key not configured")
        
        try:
            def _generate():
                message = self.client.messages.create(
                    model=self._resolve_model(model),
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": text}
                    ]
                )
                return message
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, _generate)
            
            return {
                "response": response.content[0].text if response.content else "",
                "model": response.model,
                "tokens_used": response.usage.output_tokens + response.usage.input_tokens if response.usage else 0,
                "finish_reason": response.stop_reason or "completed"
            }
        
        except Exception as e:
            raise Exception(f"Anthropic generation failed: {str(e)}")
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        max_tokens: int = 150,
        temperature: float = 0.7
    ) -> Dict:
        """
        Chat conversation with message history
        """
        if not self.is_available():
            raise Exception("Anthropic API key not configured")
        
        try:
            # Convert messages format for Anthropic
            system_message = ""
            claude_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    claude_messages.append(msg)
            
            def _chat():
                message = self.client.messages.create(
                    model=self._resolve_model(model),
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=system_message or "You are a helpful AI assistant.",
                    messages=claude_messages
                )
                return message
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, _chat)
            
            return {
                "response": response.content[0].text if response.content else "",
                "model": response.model,
                "tokens_used": response.usage.output_tokens + response.usage.input_tokens if response.usage else 0,
                "finish_reason": response.stop_reason or "completed"
            }
        
        except Exception as e:
            raise Exception(f"Anthropic chat failed: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if the service is properly configured"""
        return self.client is not None 