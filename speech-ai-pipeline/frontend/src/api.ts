import axios from 'axios';
import { Provider, PipelineStatus, ChatMessage } from './types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Configure axios
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000, // 2 minutes timeout for audio processing
});

// Get all providers
export const getProviders = async (): Promise<{
  stt: Provider[];
  llm: Provider[];
  tts: Provider[];
}> => {
  const response = await api.get('/providers');
  return response.data;
};

// Get STT providers
export const getSTTProviders = async (): Promise<{ providers: Provider[] }> => {
  const response = await api.get('/stt/providers');
  return response.data;
};

// Get LLM providers
export const getLLMProviders = async (): Promise<{ providers: Provider[] }> => {
  const response = await api.get('/llm/providers');
  return response.data;
};

// Get TTS providers
export const getTTSProviders = async (): Promise<{ providers: Provider[] }> => {
  const response = await api.get('/tts/providers');
  return response.data;
};

// Get voices for a specific TTS provider
export const getTTSVoices = async (provider: string, language?: string) => {
  const params = language ? { language } : {};
  const response = await api.get(`/tts/voices/${provider}`, { params });
  return response.data;
};

// Get pipeline status
export const getPipelineStatus = async (): Promise<PipelineStatus> => {
  const response = await api.get('/pipeline/status');
  return response.data;
};

// Process full pipeline (audio input)
export const processFullPipeline = async (
  audioFile: File,
  config: {
    stt_provider: string;
    llm_provider: string;
    tts_provider: string;
    stt_language?: string;
    llm_model?: string;
    llm_system_prompt?: string;
    llm_max_tokens?: number;
    llm_temperature?: number;
    tts_voice?: string;
    tts_language?: string;
    tts_speed?: number;
    tts_pitch?: number;
    llm_messages?: ChatMessage[];
  }
): Promise<{ blob: Blob; headers: any }> => {
  const formData = new FormData();
  formData.append('audio', audioFile);
  
  Object.entries(config).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      if (key === 'llm_messages' && Array.isArray(value)) {
        formData.append('llm_messages', JSON.stringify(value));
      } else {
        formData.append(key, value.toString());
      }
    }
  });

  const response = await api.post('/pipeline/process', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    responseType: 'blob',
  });

  return {
    blob: response.data,
    headers: response.headers,
  };
};

// Process text pipeline (text input)
export const processTextPipeline = async (
  text: string,
  config: {
    llm_provider: string;
    tts_provider: string;
    llm_model?: string;
    llm_system_prompt?: string;
    llm_max_tokens?: number;
    llm_temperature?: number;
    tts_voice?: string;
    tts_language?: string;
    tts_speed?: number;
    tts_pitch?: number;
    llm_messages?: ChatMessage[];
  }
): Promise<{ blob: Blob; headers: any }> => {
  const formData = new FormData();
  formData.append('text', text);
  
  Object.entries(config).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      if (key === 'llm_messages' && Array.isArray(value)) {
        formData.append('llm_messages', JSON.stringify(value));
      } else {
        formData.append(key, value.toString());
      }
    }
  });

  const response = await api.post('/pipeline/process-text', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    responseType: 'blob',
  });

  return {
    blob: response.data,
    headers: response.headers,
  };
};

// Individual service endpoints
export const transcribeAudio = async (
  audioFile: File,
  provider: string,
  language?: string
) => {
  const formData = new FormData();
  formData.append('audio', audioFile);
  formData.append('provider', provider);
  if (language) formData.append('language', language);

  const response = await api.post('/stt/transcribe', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const generateText = async (
  text: string,
  provider: string,
  config: {
    model?: string;
    max_tokens?: number;
    temperature?: number;
    system_prompt?: string;
  } = {}
) => {
  const formData = new FormData();
  formData.append('text', text);
  formData.append('provider', provider);
  
  Object.entries(config).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      formData.append(key, value.toString());
    }
  });

  const response = await api.post('/llm/generate', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const synthesizeSpeech = async (
  text: string,
  provider: string,
  config: {
    voice?: string;
    language?: string;
    speed?: number;
    pitch?: number;
  } = {}
): Promise<Blob> => {
  const formData = new FormData();
  formData.append('text', text);
  formData.append('provider', provider);
  
  Object.entries(config).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      formData.append(key, value.toString());
    }
  });

  const response = await api.post('/tts/synthesize', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    responseType: 'blob',
  });

  return response.data;
}; 