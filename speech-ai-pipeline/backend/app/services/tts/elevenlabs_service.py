import os
from elevenlabs.client import ElevenLabs
from typing import List, Dict, Optional
import tempfile
import asyncio

class ElevenLabsService:
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        if self.api_key:
            os.environ["ELEVENLABS_API_KEY"] = self.api_key
        self.client = ElevenLabs(api_key=self.api_key) if self.api_key else None
    
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
                voice_name_to_id = {
                    "Rachel": "21m00Tcm4TlvDq8ikWAM",
                    "Drew": "29vD33N1CtxCmqQRPOHJ",
                    "Clyde": "2EiwWnXFnvU5JabPnv8n",
                    "Paul": "5Q0t7uMcjvnagumLfvZi",
                }
                selected = voice or "Rachel"
                voice_id = voice_name_to_id.get(selected, selected)

                audio = self.client.text_to_speech.convert(
                    text=text,
                    voice_id=voice_id,
                    model_id="eleven_multilingual_v2",
                    output_format="mp3_44100_128",
                )

                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                    if isinstance(audio, (bytes, bytearray)):
                        temp_file.write(audio)
                    else:
                        for chunk in audio:
                            if isinstance(chunk, (bytes, bytearray)):
                                temp_file.write(chunk)
                    return temp_file.name

            loop = asyncio.get_event_loop()
            audio_file = await loop.run_in_executor(None, _synthesize)
            return audio_file
        
        except Exception as e:
            raise Exception(f"ElevenLabs synthesis failed: {str(e)}")
    
    async def get_voices(self) -> List[Dict]:
        """Get available ElevenLabs voices"""
        if not self.is_available():
            return []
        
        try:
            def _get_voices():
                response = self.client.voices.search()
                return getattr(response, "voices", response)

            loop = asyncio.get_event_loop()
            voice_list = await loop.run_in_executor(None, _get_voices)

            return [
                {
                    "name": getattr(v, "name", getattr(v, "voice", "")),
                    "voice_id": getattr(v, "voice_id", ""),
                    "category": getattr(v, "category", ""),
                    "description": getattr(v, "description", ""),
                }
                for v in voice_list
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
        return self.client is not None 