from gtts import gTTS
from typing import List, Dict, Optional
import tempfile
import asyncio

class GTTSService:
    def __init__(self):
        pass  # gTTS is free and requires no API key
    
    async def synthesize(
        self,
        text: str,
        language: str = "en",
        speed: float = 1.0
    ) -> str:
        """
        Synthesize speech using Google Translate TTS (gTTS)
        
        Returns:
            Path to the generated audio file
        """
        try:
            def _synthesize():
                # Convert language code format (en-US -> en)
                lang_code = language.split('-')[0] if '-' in language else language
                
                # Create gTTS object
                tts = gTTS(
                    text=text,
                    lang=lang_code,
                    slow=speed < 0.8  # Use slow speech for speeds below 0.8
                )
                
                # Create temporary file
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                temp_file.close()
                
                # Save audio
                tts.save(temp_file.name)
                
                return temp_file.name
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            audio_file = await loop.run_in_executor(None, _synthesize)
            
            return audio_file
        
        except Exception as e:
            raise Exception(f"gTTS synthesis failed: {str(e)}")
    
    async def get_voices(self, language: str = "en") -> List[Dict]:
        """Get available gTTS 'voices' (languages)"""
        # gTTS doesn't have different voices, just languages
        supported_languages = {
            "en": "English",
            "es": "Spanish", 
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "zh": "Chinese",
            "ja": "Japanese",
            "ko": "Korean",
            "ar": "Arabic",
            "hi": "Hindi",
            "ru": "Russian"
        }
        
        lang_code = language.split('-')[0] if '-' in language else language
        
        return [
            {
                "name": "default",
                "display_name": f"Default {supported_languages.get(lang_code, lang_code)} Voice",
                "language": lang_code,
                "gender": "neutral"
            }
        ]
    
    def is_available(self) -> bool:
        """gTTS is always available (no API key required)"""
        return True 