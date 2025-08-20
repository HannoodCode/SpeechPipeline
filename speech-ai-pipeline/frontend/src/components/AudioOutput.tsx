import React, { useEffect, useRef } from 'react';
import {
  Box,
  Typography,
  Paper,
  Chip,
  Alert,
  Button,
  IconButton,
} from '@mui/material';
import {
  PlayArrow,
  Pause,
  Download,
  VolumeUp,
} from '@mui/icons-material';

interface AudioOutputProps {
  audioUrl: string | null;
  metadata: any;
  loading: boolean;
}

export const AudioOutput: React.FC<AudioOutputProps> = ({
  audioUrl,
  metadata,
  loading,
}) => {
  const audioRef = useRef<HTMLAudioElement>(null);

  useEffect(() => {
    // Auto-play the audio when it's available
    if (audioUrl && audioRef.current) {
      audioRef.current.play().catch(error => {
        console.warn('Auto-play failed:', error);
      });
    }
  }, [audioUrl]);

  const downloadAudio = () => {
    if (audioUrl) {
      const link = document.createElement('a');
      link.href = audioUrl;
      link.download = `ai_response_${Date.now()}.mp3`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  if (loading) {
    return (
      <Box sx={{ textAlign: 'center', py: 4 }}>
        <Typography variant="h6" gutterBottom>
          Processing your request...
        </Typography>
        <Typography variant="body2" color="text.secondary">
          This may take a few moments
        </Typography>
      </Box>
    );
  }

  if (!audioUrl) {
    return (
      <Box sx={{ textAlign: 'center', py: 4 }}>
        <VolumeUp sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
        <Typography variant="h6" color="text.secondary" gutterBottom>
          No audio response yet
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Process some audio or text to hear the AI response
        </Typography>
      </Box>
    );
  }

  return (
    <Box>
      {/* Audio Player */}
      <Paper sx={{ p: 3, mb: 3, bgcolor: 'primary.main', color: 'primary.contrastText' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h6">
            🎵 AI Response
          </Typography>
          <Button
            variant="outlined"
            onClick={downloadAudio}
            startIcon={<Download />}
            sx={{ color: 'inherit', borderColor: 'inherit' }}
          >
            Download
          </Button>
        </Box>
        
        <audio
          ref={audioRef}
          controls
          style={{ width: '100%' }}
          preload="auto"
        >
          <source src={audioUrl} type="audio/mpeg" />
          Your browser does not support the audio element.
        </audio>
      </Paper>

      {/* Metadata Display */}
      {metadata && (
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          {/* Input/Transcribed Text */}
          {(metadata.transcribedText || metadata.inputText) && (
            <Alert severity="info">
              <Typography variant="subtitle2" gutterBottom>
                {metadata.transcribedText ? '🎤 Transcribed Text:' : '✏️ Input Text:'}
              </Typography>
              <Typography variant="body2">
                "{metadata.transcribedText || metadata.inputText}"
              </Typography>
              {metadata.sttConfidence && (
                <Box sx={{ mt: 1 }}>
                  <Chip 
                    label={`Confidence: ${(metadata.sttConfidence * 100).toFixed(1)}%`}
                    size="small"
                    color={metadata.sttConfidence > 0.8 ? "success" : metadata.sttConfidence > 0.6 ? "warning" : "error"}
                  />
                </Box>
              )}
            </Alert>
          )}

          {/* AI Response Text */}
          {metadata.responseText && (
            <Alert severity="success">
              <Typography variant="subtitle2" gutterBottom>
                🤖 AI Response:
              </Typography>
              <Typography variant="body2">
                "{metadata.responseText}"
              </Typography>
            </Alert>
          )}

          {/* Provider Information */}
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            {metadata.sttProvider && (
              <Chip 
                label={`STT: ${metadata.sttProvider}`} 
                color="primary" 
                variant="outlined" 
                size="small"
              />
            )}
            {metadata.llmProvider && (
              <Chip 
                label={`LLM: ${metadata.llmProvider}`} 
                color="secondary" 
                variant="outlined" 
                size="small"
              />
            )}
            {metadata.ttsProvider && (
              <Chip 
                label={`TTS: ${metadata.ttsProvider}`} 
                color="success" 
                variant="outlined" 
                size="small"
              />
            )}
          </Box>
        </Box>
      )}
    </Box>
  );
}; 