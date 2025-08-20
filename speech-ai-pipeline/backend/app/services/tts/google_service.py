import os
from google.cloud import texttospeech
from typing import List, Dict, Optional
import tempfile
import asyncio

class GoogleTTSService:
    def __init__(self):
        # Initialize Google Cloud TTS client
        self.client = texttospeech.TextToSpeechClient() if os.getenv("GOOGLE_APPLICATION_CREDENTIALS") else None
    
    async def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        language: str = "en-US",
        speed: float = 1.0,
        pitch: float = 0.0
    ) -> str:
        """
        Synthesize speech using Google Cloud Text-to-Speech
        
        Returns:
            Path to the generated audio file
        """
        if not self.client:
            raise Exception("Google Cloud TTS not configured. Set GOOGLE_APPLICATION_CREDENTIALS.")
        
        try:
            def _synthesize():
                # Set the text input
                synthesis_input = texttospeech.SynthesisInput(text=text)
                
                # Build the voice request
                voice_selection = texttospeech.VoiceSelectionParams(
                    language_code=language,
                    name=voice if voice else None,
                    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
                )
                
                # Select the audio file type
                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3,
                    speaking_rate=speed,
                    pitch=pitch
                )
                
                # Perform synthesis
                response = self.client.synthesize_speech(
                    input=synthesis_input,
                    voice=voice_selection,
                    audio_config=audio_config
                )
                
                return response.audio_content
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            audio_content = await loop.run_in_executor(None, _synthesize)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(audio_content)
                return temp_file.name
        
        except Exception as e:
            raise Exception(f"Google TTS synthesis failed: {str(e)}")
    
    async def get_voices(self, language_code: str = "en-US") -> List[Dict]:
        """Get available voices for the specified language"""
        if not self.client:
            return []
        
        try:
            def _get_voices():
                voices = self.client.list_voices(language_code=language_code)
                return voices.voices
            
            loop = asyncio.get_event_loop()
            voices = await loop.run_in_executor(None, _get_voices)
            
            return [
                {
                    "name": voice.name,
                    "language": voice.language_codes[0] if voice.language_codes else language_code,
                    "gender": voice.ssml_gender.name.lower()
                }
                for voice in voices
            ]
        
        except Exception as e:
            print(f"Failed to get Google TTS voices: {e}")
            return []
    
    def is_available(self) -> bool:
        """Check if the service is properly configured"""
        return self.client is not None 