import os
import httpx
from typing import Dict, Optional, List
import asyncio

class OllamaService:
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.default_model = "llama2"
    
    async def generate(
        self,
        text: str,
        model: Optional[str] = None,
        max_tokens: int = 150,
        temperature: float = 0.7,
        system_prompt: str = "You are a helpful AI assistant."
    ) -> Dict:
        """
        Generate a response using Ollama local models
        """
        if not await self.is_available():
            raise Exception("Ollama service not available. Make sure Ollama is running.")
        
        try:
            async with httpx.AsyncClient() as client:
                # Combine system prompt and user text
                prompt = f"{system_prompt}\n\nUser: {text}\n\nAssistant:"
                
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": model or self.default_model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": temperature,
                            "num_predict": max_tokens
                        }
                    },
                    timeout=60.0
                )
                
                if response.status_code != 200:
                    raise Exception(f"Ollama API error: {response.status_code}")
                
                result = response.json()
                
                return {
                    "response": result.get("response", ""),
                    "model": result.get("model", model or self.default_model),
                    "tokens_used": result.get("eval_count", 0),
                    "finish_reason": "completed" if result.get("done") else "length"
                }
        
        except Exception as e:
            raise Exception(f"Ollama generation failed: {str(e)}")
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        max_tokens: int = 150,
        temperature: float = 0.7
    ) -> Dict:
        """
        Chat conversation with message history using Ollama
        """
        if not await self.is_available():
            raise Exception("Ollama service not available. Make sure Ollama is running.")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json={
                        "model": model or self.default_model,
                        "messages": messages,
                        "stream": False,
                        "options": {
                            "temperature": temperature,
                            "num_predict": max_tokens
                        }
                    },
                    timeout=60.0
                )
                
                if response.status_code != 200:
                    raise Exception(f"Ollama API error: {response.status_code}")
                
                result = response.json()
                message = result.get("message", {})
                
                return {
                    "response": message.get("content", ""),
                    "model": result.get("model", model or self.default_model),
                    "tokens_used": result.get("eval_count", 0),
                    "finish_reason": "completed" if result.get("done") else "length"
                }
        
        except Exception as e:
            raise Exception(f"Ollama chat failed: {str(e)}")
    
    async def is_available(self) -> bool:
        """Check if Ollama service is running"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/tags", timeout=5.0)
                return response.status_code == 200
        except:
            return False
    
    async def list_models(self) -> List[str]:
        """List available models in Ollama"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    data = response.json()
                    return [model["name"] for model in data.get("models", [])]
                return []
        except:
            return [] 