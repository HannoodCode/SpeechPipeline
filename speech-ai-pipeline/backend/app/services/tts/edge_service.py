import edge_tts
from typing import List, Dict, Optional
import tempfile
import asyncio

class EdgeTTSService:
    def __init__(self):
        pass  # Edge TTS is free and requires no API key
    
    async def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        language: str = "en-US",
        speed: float = 1.0,
        pitch: float = 0.0
    ) -> str:
        """
        Synthesize speech using Microsoft Edge TTS
        
        Returns:
            Path to the generated audio file
        """
        try:
            # Use default voice if none specified
            voice_to_use = voice or "en-US-AriaNeural"
            
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_file.close()
            
            # Build SSML with speed and pitch
            rate = f"{int((speed - 1) * 100):+d}%" if speed != 1.0 else "+0%"
            pitch_value = f"{int(pitch):+d}Hz" if pitch != 0.0 else "+0Hz"
            
            ssml_text = f"""
            <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{language}">
                <voice name="{voice_to_use}">
                    <prosody rate="{rate}" pitch="{pitch_value}">
                        {text}
                    </prosody>
                </voice>
            </speak>
            """
            
            # Create TTS communication
            communicate = edge_tts.Communicate(ssml_text, voice_to_use)
            
            # Generate and save audio
            await communicate.save(temp_file.name)
            
            return temp_file.name
        
        except Exception as e:
            raise Exception(f"Edge TTS synthesis failed: {str(e)}")
    
    async def get_voices(self, language: str = "en-US") -> List[Dict]:
        """Get available Edge TTS voices"""
        try:
            voices = await edge_tts.list_voices()
            
            # Filter by language if specified
            filtered_voices = [
                voice for voice in voices
                if language.split('-')[0] in voice['Locale'] or language in voice['Locale']
            ] if language else voices
            
            return [
                {
                    "name": voice['ShortName'],
                    "display_name": voice['FriendlyName'],
                    "gender": voice['Gender'],
                    "locale": voice['Locale']
                }
                for voice in filtered_voices[:10]  # Limit to first 10 voices
            ]
        
        except Exception as e:
            print(f"Failed to get Edge TTS voices: {e}")
            # Return some default voices
            return [
                {"name": "en-US-AriaNeural", "display_name": "Aria", "gender": "Female", "locale": "en-US"},
                {"name": "en-US-JennyNeural", "display_name": "Jenny", "gender": "Female", "locale": "en-US"},
                {"name": "en-US-GuyNeural", "display_name": "Guy", "gender": "Male", "locale": "en-US"},
                {"name": "en-US-DavisNeural", "display_name": "Davis", "gender": "Male", "locale": "en-US"}
            ]
    
    def is_available(self) -> bool:
        """Edge TTS is always available (no API key required)"""
        return True 