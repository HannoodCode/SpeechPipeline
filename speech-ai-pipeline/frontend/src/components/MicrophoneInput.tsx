import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Button,
  Typography,
  LinearProgress,
  Alert,
  Chip,
} from '@mui/material';
import {
  Mic,
  MicOff,
  Send,
  Stop,
} from '@mui/icons-material';
import { processFullPipeline } from '../api';
import { SelectedProviders, SelectedModels } from '../types';

interface MicrophoneInputProps {
  selectedProviders: SelectedProviders;
  selectedModels: SelectedModels;
  loading: boolean;
  onProcessingStart: () => void;
  onProcessingComplete: (audioUrl: string, metadata: any) => void;
  onProcessingError: (error: string) => void;
}

export const MicrophoneInput: React.FC<MicrophoneInputProps> = ({
  selectedProviders,
  selectedModels,
  loading,
  onProcessingStart,
  onProcessingComplete,
  onProcessingError,
}) => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [recordingDuration, setRecordingDuration] = useState(0);
  const [hasAudio, setHasAudio] = useState(false);
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    };
  }, [audioUrl]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];
      
      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };
      
      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        const url = URL.createObjectURL(audioBlob);
        setAudioUrl(url);
        setHasAudio(true);
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop());
      };
      
      mediaRecorderRef.current.start();
      setIsRecording(true);
      setRecordingDuration(0);
      
      // Start timer
      intervalRef.current = setInterval(() => {
        setRecordingDuration(prev => prev + 1);
      }, 1000);
      
    } catch (error) {
      console.error('Error accessing microphone:', error);
      onProcessingError('Failed to access microphone. Please check permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    }
  };

  const processAudio = async () => {
    if (!audioUrl) return;
    
    try {
      onProcessingStart();
      
      // Convert blob URL back to File
      const response = await fetch(audioUrl);
      const blob = await response.blob();
      const audioFile = new File([blob], 'recording.wav', { type: 'audio/wav' });
      
      const result = await processFullPipeline(audioFile, {
        stt_provider: selectedProviders.stt,
        llm_provider: selectedProviders.llm,
        tts_provider: selectedProviders.tts,
        stt_language: selectedModels.stt_language,
        llm_model: selectedModels.llm,
        tts_language: selectedModels.tts_language,
        tts_voice: selectedModels.tts_voice,
        llm_system_prompt: "You are a helpful AI assistant. Provide clear, concise responses.",
        llm_max_tokens: 150,
        llm_temperature: 0.7,
        tts_speed: 1.0,
        tts_pitch: 0.0,
      });
      
      const responseAudioUrl = URL.createObjectURL(result.blob);
      
      const metadata = {
        transcribedText: result.headers['x-transcribed-text'],
        responseText: result.headers['x-response-text'],
        sttProvider: result.headers['x-stt-provider'],
        llmProvider: result.headers['x-llm-provider'],
        ttsProvider: result.headers['x-tts-provider'],
        sttConfidence: parseFloat(result.headers['x-stt-confidence'] || '0'),
      };
      
      onProcessingComplete(responseAudioUrl, metadata);
      
      // Clear the recorded audio
      setAudioUrl(null);
      setHasAudio(false);
      setRecordingDuration(0);
      
    } catch (error) {
      console.error('Processing failed:', error);
      onProcessingError(error instanceof Error ? error.message : 'Processing failed');
    }
  };

  const clearRecording = () => {
    if (audioUrl) {
      URL.revokeObjectURL(audioUrl);
    }
    setAudioUrl(null);
    setHasAudio(false);
    setRecordingDuration(0);
  };

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Recording Status */}
      <Box sx={{ mb: 2 }}>
        {isRecording && (
          <Alert severity="info" sx={{ mb: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Typography>Recording...</Typography>
              <Chip 
                label={formatDuration(recordingDuration)} 
                color="primary" 
                size="small" 
              />
            </Box>
          </Alert>
        )}
        
        {hasAudio && (
          <Alert severity="success" sx={{ mb: 2 }}>
            Audio recorded ({formatDuration(recordingDuration)}) - Ready to process
          </Alert>
        )}
      </Box>

      {/* Audio Preview */}
      {audioUrl && (
        <Box sx={{ mb: 2 }}>
          <audio controls style={{ width: '100%' }}>
            <source src={audioUrl} type="audio/wav" />
            Your browser does not support the audio element.
          </audio>
        </Box>
      )}

      {/* Recording Controls */}
      <Box sx={{ display: 'flex', gap: 2, mb: 2, flexWrap: 'wrap' }}>
        {!isRecording && !hasAudio && (
          <Button
            variant="contained"
            color="primary"
            onClick={startRecording}
            startIcon={<Mic />}
            disabled={loading}
            size="large"
          >
            Start Recording
          </Button>
        )}
        
        {isRecording && (
          <Button
            variant="contained"
            color="error"
            onClick={stopRecording}
            startIcon={<Stop />}
            size="large"
          >
            Stop Recording
          </Button>
        )}
        
        {hasAudio && !loading && (
          <>
            <Button
              variant="contained"
              color="success"
              onClick={processAudio}
              startIcon={<Send />}
              size="large"
            >
              Process Audio
            </Button>
            <Button
              variant="outlined"
              onClick={clearRecording}
              startIcon={<MicOff />}
            >
              Clear
            </Button>
          </>
        )}
      </Box>

      {/* Processing Status */}
      {loading && (
        <Box sx={{ mt: 2 }}>
          <Typography variant="body2" gutterBottom>
            Processing audio through pipeline...
          </Typography>
          <LinearProgress />
        </Box>
      )}

      {/* Instructions */}
      <Box sx={{ mt: 'auto', pt: 2 }}>
        <Typography variant="body2" color="text.secondary">
          📱 Click "Start Recording" to begin capturing audio
          <br />
          🎯 The audio will be processed through your selected providers
          <br />
          🔊 You'll hear the AI's response when processing completes
        </Typography>
      </Box>
    </Box>
  );
}; 