import os
from google.cloud import speech
from typing import Dict, Optional
import io

class GoogleSTTService:
    def __init__(self):
        # Initialize Google Cloud Speech client
        # Requires GOOGLE_APPLICATION_CREDENTIALS environment variable
        self.client = speech.SpeechClient() if os.getenv("GOOGLE_APPLICATION_CREDENTIALS") else None
    
    async def transcribe(self, audio_file_path: str, language: str = "en-US") -> Dict:
        """
        Transcribe audio using Google Cloud Speech-to-Text
        
        Args:
            audio_file_path: Path to the audio file
            language: Language code (e.g., 'en-US')
        
        Returns:
            Dict with transcription text and confidence
        """
        if not self.client:
            raise Exception("Google Speech-to-Text not configured. Set GOOGLE_APPLICATION_CREDENTIALS.")
        
        try:
            # Read audio file
            with io.open(audio_file_path, "rb") as audio_file:
                content = audio_file.read()
            
            # Configure recognition
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                language_code=language,
                enable_automatic_punctuation=True,
                enable_word_confidence=True,
                model="latest_long"
            )
            
            # Perform recognition
            response = self.client.recognize(config=config, audio=audio)
            
            if not response.results:
                return {"text": "", "confidence": 0.0}
            
            # Get the best result
            result = response.results[0]
            alternative = result.alternatives[0]
            
            return {
                "text": alternative.transcript,
                "confidence": alternative.confidence,
                "language": language
            }
        
        except Exception as e:
            raise Exception(f"Google Speech-to-Text failed: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if the service is properly configured"""
        return self.client is not None 