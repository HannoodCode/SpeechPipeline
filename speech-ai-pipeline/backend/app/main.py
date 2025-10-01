from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
import logging
import sys
import time
import uuid

from app.api import stt, llm, tts, pipeline

# Load environment variables
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger("app")

# Normalize GOOGLE_APPLICATION_CREDENTIALS to absolute path if provided relatively
gcred = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if gcred:
    if not os.path.isabs(gcred):
        abs_path = os.path.abspath(os.path.join(BASE_DIR, gcred))
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = abs_path
        logger.info("Configured GOOGLE_APPLICATION_CREDENTIALS (relative → absolute)")
    else:
        logger.info("Configured GOOGLE_APPLICATION_CREDENTIALS (absolute)")
    try:
        exists = os.path.exists(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
        logger.info(f"GOOGLE_APPLICATION_CREDENTIALS file exists: {exists}")
    except Exception:
        pass

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

@app.middleware("http")
async def request_logging_middleware(request, call_next):
    request_id = str(uuid.uuid4())
    setattr(request.state, "request_id", request_id)
    start = time.time()
    logger.info(f"[{request_id}] → {request.method} {request.url.path}")
    try:
        response = await call_next(request)
        duration_ms = int((time.time() - start) * 1000)
        response.headers["X-Trace-Id"] = request_id
        logger.info(f"[{request_id}] ← {response.status_code} {request.url.path} ({duration_ms}ms)")
        return response
    except Exception as e:
        duration_ms = int((time.time() - start) * 1000)
        logger.exception(f"[{request_id}] ✖ Unhandled error after {duration_ms}ms: {e}")
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error", "trace_id": request_id}, headers={"X-Trace-Id": request_id})

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
                "models": ["claude-3-7-sonnet-20250219", "claude-sonnet-4-20250514", "claude-opus-4-20250514"],
                "default_model": "claude-3-7-sonnet-20250219",
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