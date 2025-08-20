import os
import azure.cognitiveservices.speech as speechsdk
from typing import Dict, Optional
import asyncio

class AzureSTTService:
    def __init__(self):
        self.speech_key = os.getenv("AZURE_SPEECH_KEY")
        self.service_region = os.getenv("AZURE_SPEECH_REGION", "eastus")
    
    async def transcribe(self, audio_file_path: str, language: str = "en-US") -> Dict:
        """
        Transcribe audio using Azure Speech Services
        
        Args:
            audio_file_path: Path to the audio file
            language: Language code (e.g., 'en-US')
        
        Returns:
            Dict with transcription text and confidence
        """
        if not self.speech_key:
            raise Exception("Azure Speech Services not configured. Set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION.")
        
        try:
            # Configure speech recognition
            speech_config = speechsdk.SpeechConfig(
                subscription=self.speech_key,
                region=self.service_region
            )
            speech_config.speech_recognition_language = language
            
            # Configure audio input
            audio_input = speechsdk.AudioConfig(filename=audio_file_path)
            
            # Create speech recognizer
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config,
                audio_config=audio_input
            )
            
            # Perform recognition
            def recognize():
                result = speech_recognizer.recognize_once_async().get()
                return result
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, recognize)
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                return {
                    "text": result.text,
                    "confidence": 0.9,  # Azure doesn't provide detailed confidence in this API
                    "language": language
                }
            elif result.reason == speechsdk.ResultReason.NoMatch:
                return {"text": "", "confidence": 0.0}
            else:
                raise Exception(f"Azure recognition failed: {result.reason}")
        
        except Exception as e:
            raise Exception(f"Azure Speech Services failed: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if the service is properly configured"""
        return bool(self.speech_key) 