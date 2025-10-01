import os
from google.cloud import speech
from typing import Dict, Optional
import io
import logging
import tempfile

from pydub import AudioSegment

def _detect_audio_encoding(file_path: str) -> speech.RecognitionConfig.AudioEncoding:
    try:
        with open(file_path, "rb") as f:
            header = f.read(16)
        # WAV: 'RIFF' .... 'WAVE'
        if header.startswith(b"RIFF") and header[8:12] == b"WAVE":
            return speech.RecognitionConfig.AudioEncoding.LINEAR16
        # WebM/EBML magic
        if header.startswith(b"\x1A\x45\xDF\xA3"):
            return speech.RecognitionConfig.AudioEncoding.WEBM_OPUS
        # OGG magic
        if header.startswith(b"OggS"):
            return speech.RecognitionConfig.AudioEncoding.OGG_OPUS
    except Exception:
        pass
    return speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED

class GoogleSTTService:
    def __init__(self):
        # Initialize Google Cloud Speech client
        # Requires GOOGLE_APPLICATION_CREDENTIALS environment variable
        self.client = speech.SpeechClient() if os.getenv("GOOGLE_APPLICATION_CREDENTIALS") else None
        self.logger = logging.getLogger("stt.google")
    
    def _convert_to_wav_16k_mono(self, src_path: str) -> Optional[str]:
        try:
            audio = AudioSegment.from_file(src_path)
            audio = audio.set_frame_rate(16000).set_channels(1)
            fd, out_path = tempfile.mkstemp(suffix=".wav")
            os.close(fd)
            audio.export(out_path, format="wav")
            return out_path
        except Exception as e:
            self.logger.warning(f"FFmpeg/pydub conversion failed: {e}")
            return None

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
            
            # Detect encoding from file header
            encoding = _detect_audio_encoding(audio_file_path)
            try:
                size = os.path.getsize(audio_file_path)
            except Exception:
                size = len(content) if content else 0
            self.logger.info(f"Detected encoding={encoding.name}, size={size} bytes, lang={language}")
            
            # Configure recognition (short utterances)
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=encoding,
                language_code=language,
                enable_automatic_punctuation=True,
                enable_word_confidence=True,
                model="latest_short"
            )
            
            # Perform recognition
            response = self.client.recognize(config=config, audio=audio)
            
            if response.results:
                result = response.results[0]
                alternative = result.alternatives[0]
                return {
                    "text": alternative.transcript,
                    "confidence": alternative.confidence,
                    "language": language
                }
            
            # Fallback: convert to 16kHz mono WAV and retry with LINEAR16 if Opus container
            if encoding in (
                speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
                speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
            ):
                self.logger.info("Empty result with Opus. Converting to WAV (16k mono) and retrying...")
                wav_path = self._convert_to_wav_16k_mono(audio_file_path)
                if wav_path and os.path.exists(wav_path):
                    try:
                        with io.open(wav_path, "rb") as f:
                            wav_content = f.read()
                        audio2 = speech.RecognitionAudio(content=wav_content)
                        config2 = speech.RecognitionConfig(
                            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                            language_code=language,
                            enable_automatic_punctuation=True,
                            enable_word_confidence=True,
                            sample_rate_hertz=16000,
                            model="latest_short",
                        )
                        response2 = self.client.recognize(config=config2, audio=audio2)
                        if response2.results:
                            result2 = response2.results[0]
                            alt2 = result2.alternatives[0]
                            return {
                                "text": alt2.transcript,
                                "confidence": alt2.confidence,
                                "language": language,
                            }
                        else:
                            self.logger.info("Retry after conversion still returned empty results")
                    finally:
                        try:
                            os.unlink(wav_path)
                        except Exception:
                            pass
            
            return {"text": "", "confidence": 0.0}
         
        except Exception as e:
            raise Exception(f"Google Speech-to-Text failed: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if the service is properly configured"""
        return self.client is not None 