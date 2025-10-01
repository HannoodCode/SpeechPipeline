import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  Alert,
  Chip,
  AppBar,
  Toolbar,
} from '@mui/material';
import { MicrophoneInput } from './components/MicrophoneInput';
import { ModelSelector } from './components/ModelSelector';
import { AudioOutput } from './components/AudioOutput';
import { StatusIndicator } from './components/StatusIndicator';
import { TextInput } from './components/TextInput';
import { getProviders, getPipelineStatus } from './api';
import { Provider, PipelineStatus, ChatMessage } from './types';

function App() {
  const [providers, setProviders] = useState<{
    stt: Provider[];
    llm: Provider[];
    tts: Provider[];
  }>({ stt: [], llm: [], tts: [] });

  const [selectedProviders, setSelectedProviders] = useState({
    stt: 'whisper',
    llm: 'openai',
    tts: 'edge'
  });

  const [selectedModels, setSelectedModels] = useState({
    llm: 'gpt-3.5-turbo', // Default fallback
    stt_language: 'en',
    tts_voice: '',
    tts_language: 'en-US'
  });

  const [pipelineStatus, setPipelineStatus] = useState<PipelineStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [audioResponse, setAudioResponse] = useState<string | null>(null);
  const [responseMetadata, setResponseMetadata] = useState<any>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  useEffect(() => {
    loadProviders();
    loadPipelineStatus();
  }, []);

  const loadProviders = async () => {
    try {
      const data = await getProviders();
      setProviders(data);
      
      // Set default models
      if (data.llm.length > 0) {
        const openaiProvider = data.llm.find(p => p.name === 'openai');
        const defaultModel = openaiProvider?.default_model || data.llm[0].default_model || 'gpt-3.5-turbo';
        setSelectedModels(prev => ({
          ...prev,
          llm: defaultModel
        }));
      }
    } catch (error) {
      console.error('Failed to load providers:', error);
      setError('Failed to load providers');
    }
  };

  const loadPipelineStatus = async () => {
    try {
      const status = await getPipelineStatus();
      setPipelineStatus(status);
    } catch (error) {
      console.error('Failed to load pipeline status:', error);
    }
  };

  const handleProviderChange = (service: 'stt' | 'llm' | 'tts', provider: string) => {
    setSelectedProviders(prev => ({ ...prev, [service]: provider }));
    
    // Update default model when provider changes
    if (service === 'llm') {
      const selectedProvider = providers.llm.find(p => p.name === provider);
      if (selectedProvider) {
        const defaultModel = selectedProvider.default_model || 'gpt-3.5-turbo';
        setSelectedModels(prev => ({
          ...prev,
          llm: defaultModel
        }));
      }
    }
  };

  const handleModelChange = (key: string, value: string) => {
    setSelectedModels(prev => ({ ...prev, [key]: value }));
  };

  const handleProcessingStart = () => {
    setLoading(true);
    setError(null);
    setAudioResponse(null);
    setResponseMetadata(null);
  };

  const handleProcessingComplete = (audioUrl: string, metadata: any) => {
    setLoading(false);
    setAudioResponse(audioUrl);
    setResponseMetadata(metadata);
  };

  const handleProcessingError = (error: string) => {
    setLoading(false);
    setError(error);
  };

  return (
    <Box sx={{ flexGrow: 1, minHeight: '100vh', bgcolor: 'background.default' }}>
      <AppBar position="static" elevation={0}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            🎤 AI Speech Pipeline
          </Typography>
          <Chip 
            label="Made By Mohannad Basyouni" 
            color="secondary" 
            variant="outlined"
            sx={{ color: 'white', borderColor: 'white' }}
          />
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Grid container spacing={3}>
          {/* Header */}
          <Grid item xs={12}>
            <Typography variant="h4" component="h1" gutterBottom align="center">
              Modular AI Speech Pipeline
            </Typography>
            <Typography variant="subtitle1" align="center" color="text.secondary" paragraph>
              Speak → STT → LLM → TTS → Hear the Response
            </Typography>
          </Grid>

          {/* Status Indicators */}
          <Grid item xs={12}>
            <StatusIndicator 
              status={pipelineStatus} 
              onRefresh={loadPipelineStatus}
            />
          </Grid>

          {/* Error Display */}
          {error && (
            <Grid item xs={12}>
              <Alert severity="error" onClose={() => setError(null)}>
                {error}
              </Alert>
            </Grid>
          )}

          {/* Model Selectors */}
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Provider Configuration
              </Typography>
              <ModelSelector
                providers={providers}
                selectedProviders={selectedProviders}
                selectedModels={selectedModels}
                onProviderChange={handleProviderChange}
                onModelChange={handleModelChange}
              />
            </Paper>
          </Grid>

          {/* Input Methods */}
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3, height: '400px' }}>
              <Typography variant="h6" gutterBottom>
                🎤 Voice Input
              </Typography>
              <MicrophoneInput
                selectedProviders={selectedProviders}
                selectedModels={selectedModels}
                loading={loading}
                onProcessingStart={handleProcessingStart}
                onProcessingComplete={handleProcessingComplete}
                onProcessingError={handleProcessingError}
                messages={messages}
                onUpdateMessages={setMessages}
              />
            </Paper>
          </Grid>

          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3, height: '400px' }}>
              <Typography variant="h6" gutterBottom>
                ✏️ Text Input
              </Typography>
              <TextInput
                selectedProviders={selectedProviders}
                selectedModels={selectedModels}
                loading={loading}
                onProcessingStart={handleProcessingStart}
                onProcessingComplete={handleProcessingComplete}
                onProcessingError={handleProcessingError}
                messages={messages}
                onUpdateMessages={setMessages}
              />
            </Paper>
          </Grid>

          {/* Audio Output */}
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                🔊 AI Response
              </Typography>
              <AudioOutput
                audioUrl={audioResponse}
                metadata={responseMetadata}
                loading={loading}
              />
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

export default App; 