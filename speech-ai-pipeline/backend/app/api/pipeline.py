from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from typing import Optional
import tempfile
import os

from app.services.stt.whisper_service import WhisperService
from app.services.stt.google_service import GoogleSTTService
from app.services.stt.azure_service import AzureSTTService

from app.services.llm.openai_service import OpenAIService
from app.services.llm.anthropic_service import AnthropicService
from app.services.llm.ollama_service import OllamaService

from app.services.tts.google_service import GoogleTTSService
from app.services.tts.elevenlabs_service import ElevenLabsService
from app.services.tts.edge_service import EdgeTTSService
from app.services.tts.gtts_service import GTTSService

router = APIRouter()

# Initialize all services lazily
stt_services = {}
llm_services = {}
tts_services = {}

def get_stt_service(provider: str):
    if provider not in stt_services:
        if provider == "whisper":
            stt_services[provider] = WhisperService()
        elif provider == "google":
            stt_services[provider] = GoogleSTTService()
        elif provider == "azure":
            stt_services[provider] = AzureSTTService()
    return stt_services.get(provider)

def get_llm_service(provider: str):
    if provider not in llm_services:
        if provider == "openai":
            llm_services[provider] = OpenAIService()
        elif provider == "anthropic":
            llm_services[provider] = AnthropicService()
        elif provider == "ollama":
            llm_services[provider] = OllamaService()
    return llm_services.get(provider)

def get_tts_service(provider: str):
    if provider not in tts_services:
        if provider == "google":
            tts_services[provider] = GoogleTTSService()
        elif provider == "elevenlabs":
            tts_services[provider] = ElevenLabsService()
        elif provider == "edge":
            tts_services[provider] = EdgeTTSService()
        elif provider == "gtts":
            tts_services[provider] = GTTSService()
    return tts_services.get(provider)

@router.post("/process")
async def process_full_pipeline(
    audio: UploadFile = File(...),
    stt_provider: str = Form(...),
    llm_provider: str = Form(...),
    tts_provider: str = Form(...),
    stt_language: Optional[str] = Form("en-US"),
    llm_model: Optional[str] = Form(None),
    llm_system_prompt: Optional[str] = Form("You are a helpful AI assistant. Provide clear, concise responses."),
    llm_max_tokens: Optional[int] = Form(150),
    llm_temperature: Optional[float] = Form(0.7),
    tts_voice: Optional[str] = Form(None),
    tts_language: Optional[str] = Form("en-US"),
    tts_speed: Optional[float] = Form(1.0),
    tts_pitch: Optional[float] = Form(0.0)
):
    """
    Process the full speech-to-speech pipeline:
    Audio → STT → LLM → TTS → Audio Response
    
    - **audio**: Input audio file
    - **stt_provider**: Speech-to-text provider (whisper, google, azure)
    - **llm_provider**: Language model provider (openai, anthropic, ollama)
    - **tts_provider**: Text-to-speech provider (google, elevenlabs, edge, gtts)
    - Additional parameters for each service...
    """
    
    if not audio.content_type.startswith('audio/'):
        raise HTTPException(status_code=400, detail="File must be an audio file")
    
    # Save uploaded audio file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio.filename.split('.')[-1]}") as temp_audio:
        content = await audio.read()
        temp_audio.write(content)
        temp_audio_path = temp_audio.name
    
    try:
        # Step 1: Speech-to-Text
        stt_service = get_stt_service(stt_provider)
        if not stt_service:
            raise HTTPException(status_code=400, detail=f"Unknown STT provider: {stt_provider}")
        
        stt_result = await stt_service.transcribe(temp_audio_path, stt_language)
        transcribed_text = stt_result.get("text", "")
        
        if not transcribed_text.strip():
            raise HTTPException(status_code=400, detail="No speech detected in audio")
        
        # Step 2: Language Model Processing
        llm_service = get_llm_service(llm_provider)
        if not llm_service:
            raise HTTPException(status_code=400, detail=f"Unknown LLM provider: {llm_provider}")
        
        llm_result = await llm_service.generate(
            text=transcribed_text,
            model=llm_model,
            max_tokens=llm_max_tokens,
            temperature=llm_temperature,
            system_prompt=llm_system_prompt
        )
        response_text = llm_result.get("response", "")
        
        if not response_text.strip():
            raise HTTPException(status_code=500, detail="LLM generated empty response")
        
        # Step 3: Text-to-Speech
        tts_service = get_tts_service(tts_provider)
        if not tts_service:
            raise HTTPException(status_code=400, detail=f"Unknown TTS provider: {tts_provider}")
        
        if tts_provider == "gtts":
            # gTTS doesn't support voice/pitch parameters
            audio_file = await tts_service.synthesize(
                text=response_text,
                language=tts_language,
                speed=tts_speed
            )
        else:
            audio_file = await tts_service.synthesize(
                text=response_text,
                voice=tts_voice,
                language=tts_language,
                speed=tts_speed,
                pitch=tts_pitch
            )
        
        # Return the generated audio with metadata
        return FileResponse(
            audio_file,
            media_type="audio/mp3",
            filename=f"response_{tts_provider}.mp3",
            headers={
                "X-Transcribed-Text": transcribed_text,
                "X-Response-Text": response_text,
                "X-STT-Provider": stt_provider,
                "X-LLM-Provider": llm_provider,
                "X-TTS-Provider": tts_provider,
                "X-STT-Confidence": str(stt_result.get("confidence", 0.0))
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline processing failed: {str(e)}")
    
    finally:
        # Clean up temporary audio file
        if os.path.exists(temp_audio_path):
            os.unlink(temp_audio_path)

@router.post("/process-text")
async def process_text_pipeline(
    text: str = Form(...),
    llm_provider: str = Form(...),
    tts_provider: str = Form(...),
    llm_model: Optional[str] = Form(None),
    llm_system_prompt: Optional[str] = Form("You are a helpful AI assistant. Provide clear, concise responses."),
    llm_max_tokens: Optional[int] = Form(150),
    llm_temperature: Optional[float] = Form(0.7),
    tts_voice: Optional[str] = Form(None),
    tts_language: Optional[str] = Form("en-US"),
    tts_speed: Optional[float] = Form(1.0),
    tts_pitch: Optional[float] = Form(0.0)
):
    """
    Process text-only pipeline: Text → LLM → TTS → Audio Response
    
    - **text**: Input text
    - **llm_provider**: Language model provider (openai, anthropic, ollama)
    - **tts_provider**: Text-to-speech provider (google, elevenlabs, edge, gtts)
    """
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty")
    
    try:
        # Step 1: Language Model Processing
        llm_service = get_llm_service(llm_provider)
        if not llm_service:
            raise HTTPException(status_code=400, detail=f"Unknown LLM provider: {llm_provider}")
        
        llm_result = await llm_service.generate(
            text=text,
            model=llm_model,
            max_tokens=llm_max_tokens,
            temperature=llm_temperature,
            system_prompt=llm_system_prompt
        )
        response_text = llm_result.get("response", "")
        
        if not response_text.strip():
            raise HTTPException(status_code=500, detail="LLM generated empty response")
        
        # Step 2: Text-to-Speech
        tts_service = get_tts_service(tts_provider)
        if not tts_service:
            raise HTTPException(status_code=400, detail=f"Unknown TTS provider: {tts_provider}")
        
        if tts_provider == "gtts":
            # gTTS doesn't support voice/pitch parameters
            audio_file = await tts_service.synthesize(
                text=response_text,
                language=tts_language,
                speed=tts_speed
            )
        else:
            audio_file = await tts_service.synthesize(
                text=response_text,
                voice=tts_voice,
                language=tts_language,
                speed=tts_speed,
                pitch=tts_pitch
            )
        
        # Return the generated audio with metadata
        return FileResponse(
            audio_file,
            media_type="audio/mp3",
            filename=f"response_{tts_provider}.mp3",
            headers={
                "X-Input-Text": text,
                "X-Response-Text": response_text,
                "X-LLM-Provider": llm_provider,
                "X-TTS-Provider": tts_provider
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline processing failed: {str(e)}")

@router.get("/status")
async def get_pipeline_status():
    """Get the status of all pipeline services"""
    status = {
        "stt": {},
        "llm": {},
        "tts": {}
    }
    
    # Check STT services
    for name in ["whisper", "google", "azure"]:
        try:
            service = get_stt_service(name)
            if service:
                status["stt"][name] = service.is_available()
            else:
                status["stt"][name] = False
        except:
            status["stt"][name] = False
    
    # Check LLM services
    for name in ["openai", "anthropic", "ollama"]:
        try:
            service = get_llm_service(name)
            if service and hasattr(service, 'is_available'):
                if name == "ollama":
                    status["llm"][name] = await service.is_available()
                else:
                    status["llm"][name] = service.is_available()
            else:
                status["llm"][name] = False
        except:
            status["llm"][name] = False
    
    # Check TTS services
    for name in ["google", "elevenlabs", "edge", "gtts"]:
        try:
            service = get_tts_service(name)
            if service:
                status["tts"][name] = service.is_available()
            else:
                status["tts"][name] = False
        except:
            status["tts"][name] = False
    
    return status 