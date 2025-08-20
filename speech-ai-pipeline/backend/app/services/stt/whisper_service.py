import os
from openai import OpenAI
from typing import Dict, Optional
import aiofiles

class WhisperService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def transcribe(self, audio_file_path: str, language: Optional[str] = None) -> Dict:
        """
        Transcribe audio using OpenAI Whisper
        
        Args:
            audio_file_path: Path to the audio file
            language: Language code (optional, Whisper auto-detects)
        
        Returns:
            Dict with transcription text and confidence
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                # Use Whisper API
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language if language and language != "auto-detect" else None,
                    response_format="verbose_json"
                )
            
            return {
                "text": transcript.text,
                "confidence": 0.95,  # Whisper doesn't provide confidence scores
                "language": transcript.language if hasattr(transcript, 'language') else language,
                "duration": getattr(transcript, 'duration', None)
            }
        
        except Exception as e:
            raise Exception(f"Whisper transcription failed: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if the service is properly configured"""
        return bool(os.getenv("OPENAI_API_KEY")) 