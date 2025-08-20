import React from 'react';
import {
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Typography,
  Grid,
  Chip,
} from '@mui/material';
import { Provider, SelectedProviders, SelectedModels } from '../types';

interface ModelSelectorProps {
  providers: {
    stt: Provider[];
    llm: Provider[];
    tts: Provider[];
  };
  selectedProviders: SelectedProviders;
  selectedModels: SelectedModels;
  onProviderChange: (service: 'stt' | 'llm' | 'tts', provider: string) => void;
  onModelChange: (key: string, value: string) => void;
}

export const ModelSelector: React.FC<ModelSelectorProps> = ({
  providers,
  selectedProviders,
  selectedModels,
  onProviderChange,
  onModelChange,
}) => {
  const getSelectedProvider = (service: 'stt' | 'llm' | 'tts') => {
    return providers[service].find(p => p.name === selectedProviders[service]);
  };

  return (
    <Box>
      <Grid container spacing={3}>
        {/* STT Provider Selection */}
        <Grid item xs={12} md={4}>
          <Typography variant="subtitle1" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            🎤 Speech-to-Text
          </Typography>
          
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>STT Provider</InputLabel>
            <Select
              value={selectedProviders.stt}
              label="STT Provider"
              onChange={(e) => onProviderChange('stt', e.target.value)}
            >
              {providers.stt.map((provider) => (
                <MenuItem key={provider.name} value={provider.name}>
                  {provider.display_name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl fullWidth sx={{ mb: 1 }}>
            <InputLabel>Language</InputLabel>
            <Select
              value={selectedModels.stt_language}
              label="Language"
              onChange={(e) => onModelChange('stt_language', e.target.value)}
            >
              {getSelectedProvider('stt')?.languages?.map((lang) => (
                <MenuItem key={lang} value={lang}>
                  {lang}
                </MenuItem>
              )) || []}
            </Select>
          </FormControl>

          <Typography variant="caption" color="text.secondary">
            {getSelectedProvider('stt')?.description}
          </Typography>
        </Grid>

        {/* LLM Provider Selection */}
        <Grid item xs={12} md={4}>
          <Typography variant="subtitle1" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            🧠 Language Model
          </Typography>
          
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>LLM Provider</InputLabel>
            <Select
              value={selectedProviders.llm}
              label="LLM Provider"
              onChange={(e) => onProviderChange('llm', e.target.value)}
            >
              {providers.llm.map((provider) => (
                <MenuItem key={provider.name} value={provider.name}>
                  {provider.display_name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl fullWidth sx={{ mb: 1 }}>
            <InputLabel>Model</InputLabel>
            <Select
              value={selectedModels.llm}
              label="Model"
              onChange={(e) => onModelChange('llm', e.target.value)}
            >
              {getSelectedProvider('llm')?.models?.map((model) => (
                <MenuItem key={model} value={model}>
                  {model}
                </MenuItem>
              )) || []}
            </Select>
          </FormControl>

          <Typography variant="caption" color="text.secondary">
            {getSelectedProvider('llm')?.description}
          </Typography>
        </Grid>

        {/* TTS Provider Selection */}
        <Grid item xs={12} md={4}>
          <Typography variant="subtitle1" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            🔊 Text-to-Speech
          </Typography>
          
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>TTS Provider</InputLabel>
            <Select
              value={selectedProviders.tts}
              label="TTS Provider"
              onChange={(e) => onProviderChange('tts', e.target.value)}
            >
              {providers.tts.map((provider) => (
                <MenuItem key={provider.name} value={provider.name}>
                  {provider.display_name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <Box sx={{ mb: 2 }}>
            <FormControl fullWidth sx={{ mb: 1 }}>
              <InputLabel>Language</InputLabel>
              <Select
                value={selectedModels.tts_language}
                label="Language"
                onChange={(e) => onModelChange('tts_language', e.target.value)}
              >
                {getSelectedProvider('tts')?.languages?.map((lang) => (
                  <MenuItem key={lang} value={lang}>
                    {lang}
                  </MenuItem>
                )) || []}
              </Select>
            </FormControl>

            {getSelectedProvider('tts')?.voices && getSelectedProvider('tts')!.voices!.length > 0 && (
              <FormControl fullWidth>
                <InputLabel>Voice</InputLabel>
                <Select
                  value={selectedModels.tts_voice}
                  label="Voice"
                  onChange={(e) => onModelChange('tts_voice', e.target.value)}
                >
                  <MenuItem value="">Default</MenuItem>
                  {getSelectedProvider('tts')?.voices?.map((voice) => (
                    <MenuItem key={voice.name} value={voice.name}>
                      {voice.display_name || voice.name}
                      {voice.gender && (
                        <Chip 
                          label={voice.gender} 
                          size="small" 
                          sx={{ ml: 1 }} 
                        />
                      )}
                    </MenuItem>
                  )) || []}
                </Select>
              </FormControl>
            )}
          </Box>

          <Typography variant="caption" color="text.secondary">
            {getSelectedProvider('tts')?.description}
          </Typography>
        </Grid>
      </Grid>

      {/* Pipeline Flow Visualization */}
      <Box sx={{ mt: 3, p: 2, bgcolor: 'background.paper', borderRadius: 1, border: '1px solid', borderColor: 'divider' }}>
        <Typography variant="subtitle2" gutterBottom>
          Selected Pipeline:
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap' }}>
          <Chip label={getSelectedProvider('stt')?.display_name} color="primary" variant="outlined" />
          <Typography variant="body2">→</Typography>
          <Chip label={getSelectedProvider('llm')?.display_name} color="secondary" variant="outlined" />
          <Typography variant="body2">→</Typography>
          <Chip label={getSelectedProvider('tts')?.display_name} color="success" variant="outlined" />
        </Box>
      </Box>
    </Box>
  );
}; 