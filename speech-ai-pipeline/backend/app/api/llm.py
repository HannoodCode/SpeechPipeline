from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any

from app.services.llm.openai_service import OpenAIService
from app.services.llm.anthropic_service import AnthropicService
from app.services.llm.ollama_service import OllamaService

router = APIRouter()

# Initialize services lazily
openai_service = None
anthropic_service = None
ollama_service = None

def get_openai_service():
    global openai_service
    if openai_service is None:
        openai_service = OpenAIService()
    return openai_service

def get_anthropic_service():
    global anthropic_service
    if anthropic_service is None:
        anthropic_service = AnthropicService()
    return anthropic_service

def get_ollama_service():
    global ollama_service
    if ollama_service is None:
        ollama_service = OllamaService()
    return ollama_service

@router.post("/generate")
async def generate_response(
    text: str = Form(...),
    provider: str = Form(...),
    model: Optional[str] = Form(None),
    max_tokens: Optional[int] = Form(150),
    temperature: Optional[float] = Form(0.7),
    system_prompt: Optional[str] = Form("You are a helpful AI assistant. Provide clear, concise responses.")
):
    """
    Generate a response using the specified LLM provider
    
    - **text**: Input text/prompt
    - **provider**: LLM provider (openai, anthropic, ollama)
    - **model**: Specific model to use (optional, uses default)
    - **max_tokens**: Maximum tokens in response
    - **temperature**: Response creativity (0.0-1.0)
    - **system_prompt**: System/instruction prompt
    """
    
    try:
        # Route to appropriate service
        if provider == "openai":
            result = await get_openai_service().generate(
                text=text,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system_prompt=system_prompt
            )
        elif provider == "anthropic":
            result = await get_anthropic_service().generate(
                text=text,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system_prompt=system_prompt
            )
        elif provider == "ollama":
            result = await get_ollama_service().generate(
                text=text,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system_prompt=system_prompt
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unknown provider: {provider}")
        
        return JSONResponse(content={
            "response": result.get("response", ""),
            "provider": provider,
            "model": result.get("model", model),
            "tokens_used": result.get("tokens_used", 0),
            "finish_reason": result.get("finish_reason", "completed")
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM generation failed: {str(e)}")

@router.get("/providers")
async def get_llm_providers():
    """Get available LLM providers and their models"""
    return {
        "providers": [
            {
                "name": "openai",
                "display_name": "OpenAI",
                "models": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"],
                "default_model": "gpt-3.5-turbo",
                "description": "OpenAI's GPT models"
            },
            {
                "name": "anthropic",
                "display_name": "Anthropic",
                "models": ["claude-3-haiku-20240307", "claude-3-sonnet-20240229", "claude-3-opus-20240229"],
                "default_model": "claude-3-haiku-20240307",
                "description": "Anthropic's Claude models"
            },
            {
                "name": "ollama",
                "display_name": "Ollama (Local)",
                "models": ["llama2", "mistral", "codellama", "neural-chat"],
                "default_model": "llama2",
                "description": "Local models via Ollama"
            }
        ]
    }

@router.post("/chat")
async def chat_conversation(
    messages: list = Form(...),
    provider: str = Form(...),
    model: Optional[str] = Form(None),
    max_tokens: Optional[int] = Form(150),
    temperature: Optional[float] = Form(0.7)
):
    """
    Chat conversation with message history
    
    - **messages**: List of message objects with 'role' and 'content'
    - **provider**: LLM provider (openai, anthropic, ollama)
    - **model**: Specific model to use
    - **max_tokens**: Maximum tokens in response
    - **temperature**: Response creativity (0.0-1.0)
    """
    
    try:
        # Route to appropriate service
        if provider == "openai":
            result = await get_openai_service().chat(
                messages=messages,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature
            )
        elif provider == "anthropic":
            result = await get_anthropic_service().chat(
                messages=messages,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature
            )
        elif provider == "ollama":
            result = await get_ollama_service().chat(
                messages=messages,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unknown provider: {provider}")
        
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}") 