import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  LinearProgress,
  Alert,
} from '@mui/material';
import {
  Send,
  Clear,
} from '@mui/icons-material';
import { processTextPipeline } from '../api';
import { SelectedProviders, SelectedModels, ChatMessage } from '../types';

interface TextInputProps {
  selectedProviders: SelectedProviders;
  selectedModels: SelectedModels;
  loading: boolean;
  onProcessingStart: () => void;
  onProcessingComplete: (audioUrl: string, metadata: any) => void;
  onProcessingError: (error: string) => void;
  messages: ChatMessage[];
  onUpdateMessages: (messages: ChatMessage[]) => void;
}

export const TextInput: React.FC<TextInputProps> = ({
  selectedProviders,
  selectedModels,
  loading,
  onProcessingStart,
  onProcessingComplete,
  onProcessingError,
  messages,
  onUpdateMessages,
}) => {
  const [inputText, setInputText] = useState('');
  const [lastProcessedText, setLastProcessedText] = useState('');

  const processText = async () => {
    if (!inputText.trim()) {
      onProcessingError('Please enter some text to process');
      return;
    }
    
    try {
      onProcessingStart();
      setLastProcessedText(inputText);
      
      const result = await processTextPipeline(inputText, {
        llm_provider: selectedProviders.llm,
        tts_provider: selectedProviders.tts,
        llm_model: selectedModels.llm,
        tts_language: selectedModels.tts_language,
        tts_voice: selectedModels.tts_voice,
        llm_system_prompt: "You are a helpful AI assistant. Provide clear, concise responses.",
        llm_max_tokens: 150,
        llm_temperature: 0.7,
        tts_speed: 1.0,
        tts_pitch: 0.0,
        llm_messages: messages,
      });
      
      const responseAudioUrl = URL.createObjectURL(result.blob);
      
      const metadata = {
        inputText: result.headers['x-input-text'] || inputText,
        responseText: result.headers['x-response-text'],
        llmProvider: result.headers['x-llm-provider'],
        ttsProvider: result.headers['x-tts-provider'],
      };
      
      onProcessingComplete(responseAudioUrl, metadata);
      // Update chat history
      const userText = metadata.inputText || inputText;
      const assistantText = metadata.responseText || '';
      const updated: ChatMessage[] = [
        ...messages,
        { role: 'user' as const, content: userText as string },
        ...(assistantText ? [{ role: 'assistant' as const, content: assistantText as string }] : []),
      ];
      onUpdateMessages(updated);
      
      // Clear input after successful processing
      setInputText('');
      
    } catch (error) {
      console.error('Processing failed:', error);
      onProcessingError(error instanceof Error ? error.message : 'Processing failed');
    }
  };

  const clearText = () => {
    setInputText('');
    setLastProcessedText('');
    onUpdateMessages([]);
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && event.ctrlKey && !loading) {
      processText();
    }
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Text Input */}
      <TextField
        multiline
        rows={5}
        fullWidth
        variant="outlined"
        placeholder="Type your message here... (Ctrl+Enter to send)"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        onKeyPress={handleKeyPress}
        disabled={loading}
        sx={{ mb: 2 }}
      />

      {/* Controls */}
      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <Button
          variant="contained"
          color="primary"
          onClick={processText}
          startIcon={<Send />}
          disabled={loading || !inputText.trim()}
          size="large"
        >
          Process Text
        </Button>
        <Button
          variant="outlined"
          onClick={clearText}
          startIcon={<Clear />}
          disabled={loading}
        >
          Clear
        </Button>
      </Box>

      {/* Processing Status */}
      {loading && (
        <Box sx={{ mb: 2 }}>
          <Typography variant="body2" gutterBottom>
            Processing text through LLM and TTS...
          </Typography>
          <LinearProgress />
        </Box>
      )}

      {/* Instructions removed as requested */}
    </Box>
  );
}; 