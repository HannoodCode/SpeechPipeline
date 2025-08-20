import os
from openai import OpenAI
from typing import Dict, Optional, List, Any
import asyncio

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.default_model = "gpt-3.5-turbo"
    
    async def generate(
        self,
        text: str,
        model: Optional[str] = None,
        max_tokens: int = 150,
        temperature: float = 0.7,
        system_prompt: str = "You are a helpful AI assistant."
    ) -> Dict:
        """
        Generate a response using OpenAI's API
        """
        if not self.is_available():
            raise Exception("OpenAI API key not configured")
        
        try:
            def _generate():
                response = self.client.chat.completions.create(
                    model=model or self.default_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": text}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, _generate)
            
            message = response.choices[0].message
            
            return {
                "response": message.content,
                "model": response.model,
                "tokens_used": response.usage.total_tokens if response.usage else 0,
                "finish_reason": response.choices[0].finish_reason
            }
        
        except Exception as e:
            raise Exception(f"OpenAI generation failed: {str(e)}")
    
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
            raise Exception("OpenAI API key not configured")
        
        try:
            def _chat():
                response = self.client.chat.completions.create(
                    model=model or self.default_model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, _chat)
            
            message = response.choices[0].message
            
            return {
                "response": message.content,
                "model": response.model,
                "tokens_used": response.usage.total_tokens if response.usage else 0,
                "finish_reason": response.choices[0].finish_reason
            }
        
        except Exception as e:
            raise Exception(f"OpenAI chat failed: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if the service is properly configured"""
        return bool(os.getenv("OPENAI_API_KEY")) 