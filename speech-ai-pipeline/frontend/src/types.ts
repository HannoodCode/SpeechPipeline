export interface Provider {
  name: string;
  display_name: string;
  models?: string[];
  default_model?: string;
  voices?: Voice[];
  languages?: string[];
  description: string;
}

export interface Voice {
  name: string;
  display_name?: string;
  gender?: string;
  language?: string;
  voice_id?: string;
  locale?: string;
}

export interface PipelineStatus {
  stt: { [key: string]: boolean };
  llm: { [key: string]: boolean };
  tts: { [key: string]: boolean };
}

export interface ProcessingResult {
  audioUrl: string;
  metadata: {
    transcribedText?: string;
    responseText?: string;
    inputText?: string;
    sttProvider?: string;
    llmProvider?: string;
    ttsProvider?: string;
    sttConfidence?: number;
  };
}

export interface SelectedProviders {
  stt: string;
  llm: string;
  tts: string;
}

export interface SelectedModels {
  llm: string;
  stt_language: string;
  tts_voice: string;
  tts_language: string;
} 