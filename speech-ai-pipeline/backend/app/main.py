from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

from app.api import stt, llm, tts, pipeline

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Speech Pipeline API",
    description="Modular Speech-to-Text, LLM, and Text-to-Speech pipeline",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "https://localhost:3000", 
        "https://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(stt.router, prefix="/api/stt", tags=["Speech-to-Text"])
app.include_router(llm.router, prefix="/api/llm", tags=["Language Models"])
app.include_router(tts.router, prefix="/api/tts", tags=["Text-to-Speech"])
app.include_router(pipeline.router, prefix="/api/pipeline", tags=["Full Pipeline"])

@app.get("/")
async def root():
    return {"message": "AI Speech Pipeline API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/providers")
async def get_providers():
    """Get available providers for each service"""
    return {
        "stt": [
            {
                "name": "whisper",
                "display_name": "OpenAI Whisper",
                "languages": ["en-US", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-BR", "ja-JP", "ko-KR", "zh-CN"],
                "description": "Industry-leading speech recognition"
            },
            {
                "name": "google",
                "display_name": "Google Speech-to-Text",
                "languages": ["en-US", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-BR", "ja-JP", "ko-KR", "zh-CN"],
                "description": "Enterprise-grade cloud API"
            },
            {
                "name": "azure",
                "display_name": "Azure Speech Services",
                "languages": ["en-US", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-BR", "ja-JP", "ko-KR", "zh-CN"],
                "description": "Microsoft's speech recognition"
            }
        ],
        "llm": [
            {
                "name": "openai",
                "display_name": "OpenAI GPT",
                "models": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"],
                "default_model": "gpt-3.5-turbo",
                "description": "OpenAI's GPT models"
            },
            {
                "name": "anthropic",
                "display_name": "Anthropic Claude",
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
        ],
        "tts": [
            {
                "name": "google",
                "display_name": "Google Cloud TTS",
                "voices": [],
                "languages": ["en-US", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-BR", "ja-JP", "ko-KR", "zh-CN"],
                "description": "High-quality neural voices"
            },
            {
                "name": "elevenlabs",
                "display_name": "ElevenLabs",
                "voices": [],
                "languages": ["en-US", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-BR", "ja-JP", "ko-KR", "zh-CN"],
                "description": "Premium AI voices with emotion"
            },
            {
                "name": "edge",
                "display_name": "Microsoft Edge TTS",
                "voices": [],
                "languages": ["en-US", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-BR", "ja-JP", "ko-KR", "zh-CN"],
                "description": "Free neural voices"
            },
            {
                "name": "gtts",
                "display_name": "Google Translate TTS",
                "voices": [],
                "languages": ["en-US", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-BR", "ja-JP", "ko-KR", "zh-CN"],
                "description": "Free basic voice synthesis"
            }
        ]
    } 