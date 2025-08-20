import os
from elevenlabs import generate, voices, Voice
from typing import List, Dict, Optional
import tempfile
import asyncio

class ElevenLabsService:
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        if self.api_key:
            os.environ["ELEVENLABS_API_KEY"] = self.api_key
    
    async def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        language: str = "en-US",
        speed: float = 1.0
    ) -> str:
        """
        Synthesize speech using ElevenLabs
        
        Returns:
            Path to the generated audio file
        """
        if not self.is_available():
            raise Exception("ElevenLabs API key not configured. Set ELEVENLABS_API_KEY.")
        
        try:
            def _synthesize():
                # Use default voice if none specified
                voice_to_use = voice or "Rachel"
                
                # Generate audio
                audio = generate(
                    text=text,
                    voice=Voice(voice_id=voice_to_use) if voice_to_use in ["Rachel", "Drew", "Clyde", "Paul"] else voice_to_use,
                    model="eleven_multilingual_v2"
                )
                
                return audio
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            audio_content = await loop.run_in_executor(None, _synthesize)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(audio_content)
                return temp_file.name
        
        except Exception as e:
            raise Exception(f"ElevenLabs synthesis failed: {str(e)}")
    
    async def get_voices(self) -> List[Dict]:
        """Get available ElevenLabs voices"""
        if not self.is_available():
            return []
        
        try:
            def _get_voices():
                return voices()
            
            loop = asyncio.get_event_loop()
            voice_list = await loop.run_in_executor(None, _get_voices)
            
            return [
                {
                    "name": voice.name,
                    "voice_id": voice.voice_id,
                    "category": voice.category,
                    "description": getattr(voice, 'description', '')
                }
                for voice in voice_list
            ]
        
        except Exception as e:
            print(f"Failed to get ElevenLabs voices: {e}")
            return [
                {"name": "Rachel", "voice_id": "21m00Tcm4TlvDq8ikWAM", "category": "premade", "description": "Young American female"},
                {"name": "Drew", "voice_id": "29vD33N1CtxCmqQRPOHJ", "category": "premade", "description": "Middle-aged American male"},
                {"name": "Clyde", "voice_id": "2EiwWnXFnvU5JabPnv8n", "category": "premade", "description": "Middle-aged American male"},
                {"name": "Paul", "voice_id": "5Q0t7uMcjvnagumLfvZi", "category": "premade", "description": "Middle-aged American male"}
            ]
    
    def is_available(self) -> bool:
        """Check if the service is properly configured"""
        return bool(self.api_key) 