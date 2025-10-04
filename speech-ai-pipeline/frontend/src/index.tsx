import React from 'react';
import ReactDOM from 'react-dom/client';
import ColorModeProvider from './theme/ColorModeProvider';
import CssBaseline from '@mui/material/CssBaseline';
import App from './App';

// Ensure consistent scrollbar behavior across all pages
const style = document.createElement('style');
style.textContent = `
  html {
    overflow-y: scroll; /* Always show vertical scrollbar */
  }
`;
document.head.appendChild(style);


const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <ColorModeProvider>
      <CssBaseline />
      <App />
    </ColorModeProvider>
  </React.StrictMode>
);