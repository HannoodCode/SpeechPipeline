
# 🎤 AI Speech Pipeline

A modular, full-stack application that processes speech through a customizable AI pipeline: **Speech-to-Text → Language Model → Text-to-Speech**. Built with FastAPI backend and React frontend.

## ✨ Features

- **🎤 Speech Input**: Record audio directly in the browser
- **✏️ Text Input**: Type messages for text-only processing
- **🔄 Modular Architecture**: Choose from multiple providers for each step
- **🎯 Real-time Processing**: Stream audio through the complete pipeline
- **📊 Service Status**: Monitor which providers are available
- **💾 Audio Download**: Save AI responses as MP3 files
- **📱 Modern UI**: Responsive design with Material-UI

## 🏗️ Architecture

### Speech-to-Text (STT) Providers
- **OpenAI Whisper** - Industry-leading accuracy
- **Google Speech-to-Text** - Enterprise-grade cloud API
- **Azure Speech Services** - Microsoft's speech recognition

### Language Model (LLM) Providers
- **OpenAI GPT** - GPT-3.5 Turbo, GPT-4, GPT-4 Turbo
- **Anthropic Claude** - Claude 3 (Haiku, Sonnet, Opus)
- **Ollama** - Local models (Llama 2, Mistral, CodeLlama)

### Text-to-Speech (TTS) Providers
- **Google Cloud TTS** - High-quality neural voices
- **ElevenLabs** - Premium AI voices with emotion
- **Microsoft Edge TTS** - Free neural voices
- **Google Translate TTS** - Free basic voice synthesis

## 📁 Project Structure

```
speech-ai-pipeline/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI application entry point
│   │   ├── api/            # API route handlers
│   │   │   ├── stt.py      # Speech-to-text endpoints
│   │   │   ├── llm.py      # Language model endpoints
│   │   │   ├── tts.py      # Text-to-speech endpoints
│   │   │   └── pipeline.py # Full pipeline endpoints
│   │   └── services/       # Modular service implementations
│   │       ├── stt/        # STT provider implementations
│   │       ├── llm/        # LLM provider implementations
│   │       └── tts/        # TTS provider implementations
│   ├── requirements.txt    # Python dependencies
│   └── env.example        # Environment variables template
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # UI components
│   │   ├── api.ts         # Backend API client
│   │   ├── types.ts       # TypeScript type definitions
│   │   └── App.tsx        # Main application component
│   └── package.json       # Node.js dependencies
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **API Keys** for your chosen providers (see Configuration below)

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd speech-ai-pipeline
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp env.example .env
# Edit .env with your API keys (see Configuration section)

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will be available at `http://localhost:3000`

## ⚙️ Configuration

### Environment Variables

Copy `backend/env.example` to `backend/.env` and configure your API keys:

```bash
# OpenAI (for Whisper STT and GPT models)
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic (for Claude models)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Google Cloud (for Speech-to-Text and Text-to-Speech)
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/google-credentials.json

# Azure Speech Services
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=eastus

# ElevenLabs (for premium TTS)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Ollama (local LLM server)
OLLAMA_BASE_URL=http://localhost:11434
```

### Provider Setup Guides

#### OpenAI Setup
1. Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Add to `.env`: `OPENAI_API_KEY=sk-...`

#### Google Cloud Setup
1. Create project at [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Speech-to-Text and Text-to-Speech APIs
3. Create service account and download JSON key
4. Set `GOOGLE_APPLICATION_CREDENTIALS` to JSON file path

#### Azure Speech Setup
1. Create Speech resource at [Azure Portal](https://portal.azure.com/)
2. Get key and region from resource overview
3. Add to `.env`: `AZURE_SPEECH_KEY` and `AZURE_SPEECH_REGION`

#### Anthropic Setup
1. Get API key from [Anthropic Console](https://console.anthropic.com/)
2. Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`

#### ElevenLabs Setup
1. Sign up at [ElevenLabs](https://elevenlabs.io/)
2. Get API key from profile
3. Add to `.env`: `ELEVENLABS_API_KEY=...`

#### Ollama Setup (Local LLMs)
1. Install [Ollama](https://ollama.ai/)
2. Pull models: `ollama pull llama2`, `ollama pull mistral`
3. Start server: `ollama serve`

## 🔧 API Endpoints

### Core Pipeline
- `POST /api/pipeline/process` - Full pipeline (Audio → STT → LLM → TTS → Audio)
- `POST /api/pipeline/process-text` - Text pipeline (Text → LLM → TTS → Audio)
- `GET /api/pipeline/status` - Check service availability

### Individual Services
- `POST /api/stt/transcribe` - Speech-to-text only
- `POST /api/llm/generate` - Language model only
- `POST /api/tts/synthesize` - Text-to-speech only

### Provider Information
- `GET /api/providers` - List all available providers
- `GET /api/stt/providers` - STT provider details
- `GET /api/llm/providers` - LLM provider details
- `GET /api/tts/providers` - TTS provider details

## 🎯 Usage Examples

### Basic Voice Interaction
1. Select your preferred providers (e.g., Whisper + OpenAI + ElevenLabs)
2. Click "Start Recording" and speak your message
3. Click "Stop Recording" then "Process Audio"
4. Listen to the AI's response

### Text Chat
1. Choose LLM and TTS providers
2. Type your message in the text input
3. Click "Process Text" or use Ctrl+Enter
4. Hear the AI's spoken response

### Custom Configuration
- Change providers mid-conversation
- Adjust language settings for multilingual support
- Select different voices for varied experiences
- Monitor service status in real-time

## 🚢 Deployment

### Docker Deployment (Coming Soon)
```bash
# Build and run with Docker Compose
docker-compose up --build
```

### Manual Deployment
1. **Backend**: Deploy FastAPI app with Gunicorn/Uvicorn
2. **Frontend**: Build with `npm run build` and serve static files
3. **Environment**: Set production API keys and endpoints

## 🛠️ Development

### Adding New Providers

1. **STT Provider**:
   - Create service class in `backend/app/services/stt/`
   - Implement `transcribe()` and `is_available()` methods
   - Register in `backend/app/api/stt.py`

2. **LLM Provider**:
   - Create service class in `backend/app/services/llm/`
   - Implement `generate()` and `chat()` methods
   - Register in `backend/app/api/llm.py`

3. **TTS Provider**:
   - Create service class in `backend/app/services/tts/`
   - Implement `synthesize()` and `get_voices()` methods
   - Register in `backend/app/api/tts.py`

### Frontend Development
```bash
cd frontend
npm start    # Development server
npm test     # Run tests
npm run build # Production build
```

### Backend Development
```bash
cd backend
uvicorn app.main:app --reload  # Development server with auto-reload
pytest                         # Run tests (when implemented)
```

## 📋 TODO / Roadmap

- [ ] Docker containerization
- [ ] Authentication and user accounts
- [ ] Conversation history
- [ ] Voice cloning integration
- [ ] Real-time streaming pipeline
- [ ] Webhook integrations
- [ ] Mobile app (React Native)
- [ ] Voice activity detection
- [ ] Multi-language auto-detection
- [ ] Cost tracking and analytics

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for Whisper and GPT models
- **Anthropic** for Claude models
- **Google Cloud** for Speech APIs
- **Microsoft** for Azure Speech Services
- **ElevenLabs** for premium voice synthesis
- **Material-UI** for React components
- **FastAPI** for the excellent Python web framework

## 🔗 Links

- **Demo**: [Live Demo](your-demo-url)
- **Documentation**: [API Docs](http://localhost:8000/docs)
- **Portfolio**: [Your Portfolio](your-portfolio-url)

---

**Built with ❤️ for AI enthusiasts and developers** 