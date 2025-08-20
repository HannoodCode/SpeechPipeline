from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional
import tempfile
import os

from app.services.tts.google_service import GoogleTTSService
from app.services.tts.elevenlabs_service import ElevenLabsService
from app.services.tts.edge_service import EdgeTTSService
from app.services.tts.gtts_service import GTTSService

router = APIRouter()

# Initialize services lazily
google_service = None
elevenlabs_service = None
edge_service = None
gtts_service = None

def get_google_service():
    global google_service
    if google_service is None:
        google_service = GoogleTTSService()
    return google_service

def get_elevenlabs_service():
    global elevenlabs_service
    if elevenlabs_service is None:
        elevenlabs_service = ElevenLabsService()
    return elevenlabs_service

def get_edge_service():
    global edge_service
    if edge_service is None:
        edge_service = EdgeTTSService()
    return edge_service

def get_gtts_service():
    global gtts_service
    if gtts_service is None:
        gtts_service = GTTSService()
    return gtts_service

@router.post("/synthesize")
async def synthesize_speech(
    text: str = Form(...),
    provider: str = Form(...),
    voice: Optional[str] = Form(None),
    language: Optional[str] = Form("en-US"),
    speed: Optional[float] = Form(1.0),
    pitch: Optional[float] = Form(0.0)
):
    """
    Synthesize speech from text using the specified provider
    
    - **text**: Text to convert to speech
    - **provider**: TTS provider (google, elevenlabs, edge, gtts)
    - **voice**: Voice ID/name (provider-specific)
    - **language**: Language code (e.g., 'en-US')
    - **speed**: Speech speed (0.5-2.0)
    - **pitch**: Voice pitch (-20.0 to 20.0)
    """
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        # Route to appropriate service
        if provider == "google":
            audio_file = await get_google_service().synthesize(
                text=text,
                voice=voice,
                language=language,
                speed=speed,
                pitch=pitch
            )
        elif provider == "elevenlabs":
            audio_file = await get_elevenlabs_service().synthesize(
                text=text,
                voice=voice,
                language=language,
                speed=speed
            )
        elif provider == "edge":
            audio_file = await get_edge_service().synthesize(
                text=text,
                voice=voice,
                language=language,
                speed=speed,
                pitch=pitch
            )
        elif provider == "gtts":
            audio_file = await get_gtts_service().synthesize(
                text=text,
                language=language,
                speed=speed
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unknown provider: {provider}")
        
        # Return the audio file
        return FileResponse(
            audio_file,
            media_type="audio/wav",
            filename=f"speech_{provider}.wav",
            headers={"X-Provider": provider}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech synthesis failed: {str(e)}")

@router.get("/providers")
async def get_tts_providers():
    """Get available TTS providers and their voices"""
    return {
        "providers": [
            {
                "name": "google",
                "display_name": "Google Text-to-Speech",
                "voices": [
                    {"name": "en-US-Neural2-A", "gender": "female", "language": "en-US"},
                    {"name": "en-US-Neural2-C", "gender": "female", "language": "en-US"},
                    {"name": "en-US-Neural2-D", "gender": "male", "language": "en-US"},
                    {"name": "en-US-Neural2-E", "gender": "female", "language": "en-US"}
                ],
                "languages": ["en-US", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-BR", "zh-CN", "ja-JP"],
                "description": "Google Cloud Text-to-Speech API"
            },
            {
                "name": "elevenlabs",
                "display_name": "ElevenLabs",
                "voices": [
                    {"name": "Rachel", "gender": "female", "language": "en-US"},
                    {"name": "Drew", "gender": "male", "language": "en-US"},
                    {"name": "Clyde", "gender": "male", "language": "en-US"},
                    {"name": "Paul", "gender": "male", "language": "en-US"}
                ],
                "languages": ["en-US", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-BR"],
                "description": "ElevenLabs AI voices"
            },
            {
                "name": "edge",
                "display_name": "Microsoft Edge TTS",
                "voices": [
                    {"name": "en-US-AriaNeural", "gender": "female", "language": "en-US"},
                    {"name": "en-US-JennyNeural", "gender": "female", "language": "en-US"},
                    {"name": "en-US-GuyNeural", "gender": "male", "language": "en-US"},
                    {"name": "en-US-DavisNeural", "gender": "male", "language": "en-US"}
                ],
                "languages": ["en-US", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-BR", "zh-CN", "ja-JP"],
                "description": "Microsoft Edge Text-to-Speech"
            },
            {
                "name": "gtts",
                "display_name": "Google Translate TTS",
                "voices": [
                    {"name": "default", "gender": "neutral", "language": "en-US"}
                ],
                "languages": ["en", "es", "fr", "de", "it", "pt", "zh", "ja"],
                "description": "Free Google Translate TTS"
            }
        ]
    }

@router.get("/voices/{provider}")
async def get_provider_voices(provider: str, language: Optional[str] = "en-US"):
    """Get available voices for a specific provider"""
    try:
        if provider == "google":
            voices = await get_google_service().get_voices(language)
        elif provider == "elevenlabs":
            voices = await get_elevenlabs_service().get_voices()
        elif provider == "edge":
            voices = await get_edge_service().get_voices(language)
        elif provider == "gtts":
            voices = await get_gtts_service().get_voices(language)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown provider: {provider}")
        
        return {"provider": provider, "voices": voices}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get voices: {str(e)}") 