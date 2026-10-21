import { createTheme } from '@mui/material/styles';

export const getTheme = (mode) =>
  createTheme({
    palette: {
      mode,
      primary: {
        main: '#10b981', // Emerald green
        light: '#34d399',
        dark: '#059669',
        contrastText: '#ffffff',
      },
      secondary: {
        main: '#0ea5e9', // Sky blue
        light: '#38bdf8',
        dark: '#0284c7',
      },
      warning: {
        main: '#f59e0b',
        light: '#fbbf24',
      },
      background: {
        default: mode === 'dark' ? '#0f172a' : '#f8fafc',
        paper: mode === 'dark' ? '#1e293b' : '#ffffff',
      },
      text: {
        primary: mode === 'dark' ? '#f8fafc' : '#0f172a',
        secondary: mode === 'dark' ? '#94a3b8' : '#64748b',
      },
    },
    typography: {
      fontFamily: '"Plus Jakarta Sans", "Outfit", "Roboto", "Helvetica", "Arial", sans-serif',
      h1: { fontFamily: 'Outfit, sans-serif', fontWeight: 800 },
      h2: { fontFamily: 'Outfit, sans-serif', fontWeight: 700 },
      h3: { fontFamily: 'Outfit, sans-serif', fontWeight: 700 },
      h4: { fontFamily: 'Outfit, sans-serif', fontWeight: 600 },
      h5: { fontFamily: 'Outfit, sans-serif', fontWeight: 600 },
      h6: { fontFamily: 'Outfit, sans-serif', fontWeight: 600 },
    },
    shape: {
      borderRadius: 12,
    },
    components: {
      MuiButton: {
        styleOverrides: {
          root: {
            borderRadius: 10,
            textTransform: 'none',
            fontWeight: 600,
            boxShadow: 'none',
            padding: '8px 18px',
          },
        },
      },
      MuiCard: {
        styleOverrides: {
          root: {
            borderRadius: 16,
            backgroundImage: 'none',
            boxShadow: mode === 'dark' 
              ? '0 10px 25px -5px rgba(0, 0, 0, 0.4)' 
              : '0 10px 25px -5px rgba(16, 185, 129, 0.08)',
          },
        },
      },
    },
  });
