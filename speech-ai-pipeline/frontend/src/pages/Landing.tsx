import React from 'react';
import { Box, Button, Container, Typography, Stack, Grid, Paper, Chip } from '@mui/material';
import { useTheme, alpha } from '@mui/material/styles';
import { Link as RouterLink } from 'react-router-dom';
import SpeedIcon from '@mui/icons-material/Speed';
import BuildIcon from '@mui/icons-material/Build';
import PublicIcon from '@mui/icons-material/Public';

export const Landing: React.FC = () => {
  const theme = useTheme();
  const isLight = theme.palette.mode === 'light';
  return (
      <>
        <Container maxWidth="lg" sx={{ pt: 8, pb: { xs: 1, md: 0.5 } }}>
          <Typography variant="h2" sx={{ fontWeight: 800, letterSpacing: -1, mb: 2 }}>
            Compare. Evaluate. Explore.
          </Typography>
          <Typography
            variant="h6"
            sx={{
              color: isLight ? 'text.secondary' : 'rgba(255,255,255,0.8)',
              maxWidth: 760,
              mb: 6,
            }}
          >
            A modular platform for side‑by‑side comparison of STT, LLM, and TTS services. 
            <br />
            See the differences, explore the possibilities.
          </Typography>
          <Box sx={{ display: 'flex', justifyContent: 'center' }}>
            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} alignItems="center">
              <Button component={RouterLink} to="/app" variant="contained" color="secondary" size="large">
                Launch Demo
              </Button>
              <Button
                component={RouterLink}
                to="/about"
                variant="outlined"
                size="large"
                sx={
                  isLight
                    ? {
                        color: 'primary.main',
                        borderColor: 'primary.main',
                        ':hover': {
                          borderColor: 'primary.dark',
                          backgroundColor: alpha(theme.palette.primary.main, 0.08),
                        },
                      }
                    : {
                        color: 'rgba(255,255,255,0.9)',
                        borderColor: 'rgba(255,255,255,0.6)',
                        ':hover': {
                          borderColor: '#ffffff',
                          backgroundColor: 'rgba(255,255,255,0.08)'
                        }
                      }
                }
              >
                Learn More
              </Button>
            </Stack>
          </Box>

          {/* Stats/Highlights Section */}
          <Box sx={{ textAlign: 'center', pt: 10, pb: 2 }}>
            <Grid container spacing={4} justifyContent="center">
              <Grid item xs={4} sm={4}>
                <Typography variant="h4" sx={{ fontWeight: 800, color: 'primary.main', mb: 0.5 }}>
                  10+
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  AI Providers
                </Typography>
              </Grid>
              <Grid item xs={4} sm={4}>
                <Typography variant="h4" sx={{ fontWeight: 800, color: 'primary.main', mb: 0.5 }}>
                  3
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Core Services
                </Typography>
              </Grid>
              <Grid item xs={4} sm={4}>
                <Typography variant="h4" sx={{ fontWeight: 800, color: 'primary.main', mb: 0.5 }}>
                  &lt;1s
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Response Time
                </Typography>
              </Grid>
            </Grid>
          </Box>
        </Container>

      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Stack spacing={1}>
          <Box>
            <Typography variant="h4" sx={{ fontWeight: 700, mb: 2 }}>
              Modular & Production-Ready
            </Typography>
            <Typography color="text.secondary" sx={{ mb: 2 }}>
              Choose your favorite providers for each step: Whisper, OpenAI, Edge TTS, and more.
              Swap them instantly without code changes.
            </Typography>
            <Typography color="text.secondary">
              Built with FastAPI backend, React + MUI frontend, clean API contracts, and flexible configuration.
            </Typography>
          </Box>

          <Grid container spacing={4}>
            <Grid item xs={12} md={4}>
              <Paper sx={{ p: 3, textAlign: 'center', height: '100%' }}>
                <SpeedIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                  Fast & Efficient
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Optimized for speed with real-time processing and minimal latency
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} md={4}>
              <Paper sx={{ p: 3, textAlign: 'center', height: '100%' }}>
                <BuildIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                  Easy Integration
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Simple API design makes it easy to integrate into your existing projects
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} md={4}>
              <Paper sx={{ p: 3, textAlign: 'center', height: '100%' }}>
                <PublicIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                  Cloud Ready
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Deploy anywhere with Docker support and cloud-native architecture
                </Typography>
              </Paper>
            </Grid>
          </Grid>

          <Box sx={{ textAlign: 'center', py: 4 }}>
            <Typography variant="h5" sx={{ fontWeight: 600, mb: 2 }}>
              Supported Providers
            </Typography>
            <Stack direction="row" spacing={1} justifyContent="center" flexWrap="wrap" sx={{ gap: 1 }}>
              <Chip label="OpenAI" variant="outlined" />
              <Chip label="Anthropic" variant="outlined" />
              <Chip label="Whisper" variant="outlined" />
              <Chip label="Azure Speech" variant="outlined" />
              <Chip label="Google TTS" variant="outlined" />
              <Chip label="Edge TTS" variant="outlined" />
              <Chip label="ElevenLabs" variant="outlined" />
              <Chip label="Ollama" variant="outlined" />
            </Stack>
          </Box>
        </Stack>
      </Container>
    </>
  );
};

export default Landing;



