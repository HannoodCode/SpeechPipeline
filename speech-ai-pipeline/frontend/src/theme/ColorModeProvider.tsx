import React, { useMemo, useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';

export type ColorMode = 'light' | 'dark';

export const ColorModeContext = React.createContext<{ mode: ColorMode; toggleColorMode: () => void }>({
  mode: 'light',
  toggleColorMode: () => {},
});

interface Props {
  children: React.ReactNode;
}

export const ColorModeProvider: React.FC<Props> = ({ children }) => {
  const [mode, setMode] = useState<ColorMode>('light');

  const theme = useMemo(() => {
    const isDark = mode === 'dark';
    return createTheme({
      palette: {
        mode,
        primary: { main: isDark ? '#7c4dff' : '#3949ab' },
        secondary: { main: isDark ? '#00e5ff' : '#00838f' },
        background: {
          default: mode === 'dark' ? '#0b1020' : '#f1f2f6',
          paper: mode === 'dark' ? '#12182b' : '#f5f5f5',
        },
      },
      typography: {
        fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
        h4: { fontWeight: 600 },
      },
    });
  }, [mode]);

  const toggleColorMode = () => setMode((prev) => (prev === 'light' ? 'dark' : 'light'));

  return (
    <ColorModeContext.Provider value={{ mode, toggleColorMode }}>
      <ThemeProvider theme={theme}>{children}</ThemeProvider>
    </ColorModeContext.Provider>
  );
};

export default ColorModeProvider;


