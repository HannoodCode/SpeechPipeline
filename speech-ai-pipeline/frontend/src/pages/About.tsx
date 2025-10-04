import React from 'react';
import { Box, Container, Typography, Grid, Paper, Stack, Accordion, AccordionDetails, AccordionSummary, Divider } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

export const About: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 8 }}>
      <Stack spacing={4}>
        <Box>
          <Typography variant="h3" sx={{ fontWeight: 800, mb: 2 }}>
            About the Project
          </Typography>
          <Typography color="text.secondary" sx={{ maxWidth: 900 }}>
            This AI Speech Pipeline showcases a modular approach to speech applications: Speech-to-Text → Language Model → Text-to-Speech.
            It’s built with FastAPI and React, cleanly separating provider integrations.
          </Typography>
        </Box>

        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>Tech Stack</Typography>
              <Stack spacing={1}>
                <Box>
                  <Typography variant="subtitle2" sx={{ fontWeight: 600, color: 'primary.main' }}>Backend</Typography>
                  <Typography variant="body2" color="text.secondary">FastAPI, Python, Pydantic, Uvicorn</Typography>
                </Box>
                <Box>
                  <Typography variant="subtitle2" sx={{ fontWeight: 600, color: 'primary.main' }}>Frontend</Typography>
                  <Typography variant="body2" color="text.secondary">React, TypeScript, Material-UI</Typography>
                </Box>
                <Box>
                  <Typography variant="subtitle2" sx={{ fontWeight: 600, color: 'primary.main' }}>AI Services</Typography>
                  <Typography variant="body2" color="text.secondary">OpenAI, Anthropic, Whisper, Azure, Google</Typography>
                </Box>
                <Box>
                  <Typography variant="subtitle2" sx={{ fontWeight: 600, color: 'primary.main' }}>Tools</Typography>
                  <Typography variant="body2" color="text.secondary">REST APIs, WebSocket support, Docker</Typography>
                </Box>
              </Stack>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>Key Features</Typography>
              <Stack spacing={1}>
                <Typography variant="body2" color="text.secondary">• Modular provider architecture</Typography>
                <Typography variant="body2" color="text.secondary">• Real-time audio processing</Typography>
                <Typography variant="body2" color="text.secondary">• Multi-model support & switching</Typography>
                <Typography variant="body2" color="text.secondary">• RESTful API endpoints</Typography>
                <Typography variant="body2" color="text.secondary">• WebSocket streaming</Typography>
                <Typography variant="body2" color="text.secondary">• Dark/Light theme support</Typography>
                <Typography variant="body2" color="text.secondary">• Responsive design</Typography>
                <Typography variant="body2" color="text.secondary">• Error handling & validation</Typography>
              </Stack>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>Use Cases</Typography>
              <Stack spacing={1}>
                <Typography variant="body2" color="text.secondary">• Voice assistant development</Typography>
                <Typography variant="body2" color="text.secondary">• AI model benchmarking</Typography>
                <Typography variant="body2" color="text.secondary">• Interactive chatbots</Typography>
                <Typography variant="body2" color="text.secondary">• Accessibility applications</Typography>
                <Typography variant="body2" color="text.secondary">• Content creation tools</Typography>
                <Typography variant="body2" color="text.secondary">• Customer service automation</Typography>
                <Typography variant="body2" color="text.secondary">• Language learning apps</Typography>
                <Typography variant="body2" color="text.secondary">• Research & prototyping</Typography>
              </Stack>
            </Paper>
          </Grid>
        </Grid>

        <Box>
          <Typography variant="h4" align="center" sx={{ fontWeight: 700, mb: 3 }}>
            FAQ
          </Typography>
          
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography>Which providers are supported?</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Box>
                <Typography variant="subtitle2" sx={{ fontWeight: 700, mb: 0.5 }}>STT services</Typography>
                <Typography color="text.secondary" sx={{ mb: 1.5 }}>
                  Whisper, Google STT, Azure Speech
                </Typography>
                <Divider sx={{ my: 1.5 }} />
                <Typography variant="subtitle2" sx={{ fontWeight: 700, mb: 0.5 }}>LLM services</Typography>
                <Typography color="text.secondary" sx={{ mb: 1.5 }}>
                  OpenAI, Anthropic, Ollama (local)
                </Typography>
                <Divider sx={{ my: 1.5 }} />
                <Typography variant="subtitle2" sx={{ fontWeight: 700, mb: 0.5 }}>TTS services</Typography>
                <Typography color="text.secondary">
                  Google TTS, Microsoft Edge TTS, ElevenLabs, gTTS
                </Typography>
              </Box>
            </AccordionDetails>
          </Accordion>

          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography>Can I switch providers without code changes?</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography color="text.secondary">
                Yes! Just select the providers and models you want to use and the backend does the rest!
              </Typography>
            </AccordionDetails>
          </Accordion>

          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography>How do I run it locally?</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography color="text.secondary">
                configure .env with your API keys, run the start.sh script in your terminal, and you're set.
              </Typography>
            </AccordionDetails>
          </Accordion>

          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography>How do I use Ollama?</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography color="text.secondary">
                Install the Ollama runtime, then pull the models you want
                to use (e.g., <code>ollama pull llama2</code>, <code>ollama pull mistral</code>). Make sure the
                Ollama server is running (<code>ollama serve</code>) before selecting Ollama in the demo.
              </Typography>
            </AccordionDetails>
          </Accordion>

          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography>How do I add my own service(s)?</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography color="text.secondary">
                To add your own service, create a new service class in the appropriate directory 
                (<code>services/stt/</code>, <code>services/llm/</code>, or <code>services/tts/</code>). 
                Follow the existing service patterns and implement the required interface methods. 
                Then register your service in the provider configuration and add it to the frontend 
                model selector. Check the existing service implementations for reference.
              </Typography>
            </AccordionDetails>
          </Accordion>
        </Box>
      </Stack>
    </Container>
  );
};

export default About;



