import React, { useContext } from 'react';
import {
  Typography,
  Box,
  Chip,
  AppBar,
  Toolbar,
  Button,
  Stack,
  Container,
} from '@mui/material';
import { BrowserRouter, Routes, Route, Link as RouterLink } from 'react-router-dom';
import { Switch, Tooltip } from '@mui/material';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import LightModeIcon from '@mui/icons-material/LightMode';
import Landing from './pages/Landing';
import About from './pages/About';
import Dashboard from './pages/Dashboard';
import { ColorModeContext } from './theme/ColorModeProvider';
import Footer from './components/Footer';

function App() {
  const { mode, toggleColorMode } = useContext(ColorModeContext);
  return (
    <BrowserRouter>
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', bgcolor: 'background.default' }}>
        <AppBar position="fixed" elevation={0} sx={{ py: 1 }}>
          <Toolbar sx={{ position: 'relative' }}>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Typography 
                variant="h6" 
                component="div"
                sx={{ 
                  fontFamily: 'Baufra, Inter, "Helvetica", "Arial", sans-serif',
                  fontWeight: 600,
                  letterSpacing: '0.3px'
                }}
              >
               AI Speech Pipeline
              </Typography>
            </Box>

            {/* Absolutely centered nav to avoid any shift across routes */}
            <Box sx={{ position: 'absolute', left: '50%', transform: 'translateX(-50%)' }}>
              <Stack direction="row" spacing={1.5} alignItems="center">
                <Button sx={{ fontFamily: 'Manrope, Inter, "Helvetica", "Arial", sans-serif', fontWeight: 600 }} color="inherit" component={RouterLink} to="/">Home</Button>
                <Button sx={{ fontFamily: 'Manrope, Inter, "Helvetica", "Arial", sans-serif', fontWeight: 600 }} color="inherit" component={RouterLink} to="/app">Demo</Button>
                <Button sx={{ fontFamily: 'Manrope, Inter, "Helvetica", "Arial", sans-serif', fontWeight: 600 }} color="inherit" component={RouterLink} to="/about">About</Button>
              </Stack>
            </Box>

            <Box sx={{ display: 'flex', justifyContent: 'flex-end', ml: 'auto' }}>
              <Stack direction="row" spacing={1} alignItems="center">
                <LightModeIcon fontSize="small" />
                <Tooltip title={`Switch to ${mode === 'dark' ? 'light' : 'dark'} mode`}>
                  <Switch
                    checked={mode === 'dark'}
                    onChange={toggleColorMode}
                    inputProps={{ 'aria-label': 'toggle color mode' }}
                    sx={{
                      '& .MuiSwitch-switchBase.Mui-checked': {
                        color: 'primary.main',
                      },
                      '& .MuiSwitch-track': {
                        opacity: 1,
                      },
                    }}
                  />
                </Tooltip>
                <DarkModeIcon fontSize="small" />
              </Stack>
            </Box>
          </Toolbar>
        </AppBar>

        {/* Spacer to offset fixed AppBar height */}
        <Toolbar />

        <Container maxWidth="xl" sx={{ px: { xs: 2, md: 4 }, flex: 1, minHeight: 'calc(100vh - 64px)' }}>
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/app" element={<Dashboard />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </Container>
        <Footer />
      </Box>
    </BrowserRouter>
  );
}

export default App; 