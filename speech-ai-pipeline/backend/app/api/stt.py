from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os
from typing import Optional

from app.services.stt.whisper_service import WhisperService
from app.services.stt.google_service import GoogleSTTService
from app.services.stt.azure_service import AzureSTTService

router = APIRouter()

# Initialize services lazily
whisper_service = None
google_service = None
azure_service = None

def get_whisper_service():
    global whisper_service
    if whisper_service is None:
        whisper_service = WhisperService()
    return whisper_service

def get_google_service():
    global google_service
    if google_service is None:
        google_service = GoogleSTTService()
    return google_service

def get_azure_service():
    global azure_service
    if azure_service is None:
        azure_service = AzureSTTService()
    return azure_service

@router.post("/transcribe")
async def transcribe_audio(
    audio: UploadFile = File(...),
    provider: str = Form(...),
    language: Optional[str] = Form("en-US")
):
    """
    Transcribe audio using the specified provider
    
    - **audio**: Audio file (wav, mp3, m4a, etc.)
    - **provider**: STT provider (whisper, google, azure)
    - **language**: Language code (default: en-US)
    """
    
    if not audio.content_type.startswith('audio/'):
        raise HTTPException(status_code=400, detail="File must be an audio file")
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio.filename.split('.')[-1]}") as temp_file:
        content = await audio.read()
        temp_file.write(content)
        temp_file_path = temp_file.name
    
    try:
        # Route to appropriate service
        if provider == "whisper":
            result = await get_whisper_service().transcribe(temp_file_path, language)
        elif provider == "google":
            result = await get_google_service().transcribe(temp_file_path, language)
        elif provider == "azure":
            result = await get_azure_service().transcribe(temp_file_path, language)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown provider: {provider}")
        
        return JSONResponse(content={
            "text": result.get("text", ""),
            "confidence": result.get("confidence", 0.0),
            "provider": provider,
            "language": language
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
    
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

@router.get("/providers")
async def get_stt_providers():
    """Get available STT providers and their capabilities"""
    return {
        "providers": [
            {
                "name": "whisper",
                "display_name": "OpenAI Whisper",
                "languages": ["auto-detect"],
                "description": "OpenAI's speech recognition model"
            },
            {
                "name": "google",
                "display_name": "Google Speech-to-Text",
                "languages": ["en-US", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-BR", "zh-CN", "ja-JP"],
                "description": "Google Cloud Speech-to-Text API"
            },
            {
                "name": "azure",
                "display_name": "Azure Speech Services",
                "languages": ["en-US", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-BR", "zh-CN", "ja-JP"],
                "description": "Microsoft Azure Speech Services"
            }
        ]
    } 