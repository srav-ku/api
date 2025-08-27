
import styled, { createGlobalStyle } from 'styled-components'

export const theme = {
  colors: {
    primary: '#6b46c1',
    secondary: '#8b5cf6',
    success: '#10b981',
    warning: '#f59e0b',
    error: '#ef4444',
    background: '#0a0a0a',
    surface: '#1a1a1a',
    surfaceLight: '#2a2a2a',
    text: '#ffffff',
    textMuted: '#a1a1aa',
    border: '#374151',
    matrix: '#00ff41'
  },
  fonts: {
    primary: "'Inter', sans-serif",
    mono: "'JetBrains Mono', monospace"
  },
  breakpoints: {
    mobile: '768px',
    tablet: '1024px',
    desktop: '1280px'
  }
}

export const GlobalStyle = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: ${theme.fonts.primary};
    background-color: ${theme.colors.background};
    color: ${theme.colors.text};
    line-height: 1.6;
    overflow-x: hidden;
  }

  .matrix-rain {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
    background: linear-gradient(
      135deg,
      rgba(0, 0, 0, 0.9) 0%,
      rgba(26, 0, 51, 0.8) 50%,
      rgba(51, 0, 102, 0.7) 100%
    );
  }

  .glow {
    box-shadow: 0 0 20px rgba(107, 70, 193, 0.3);
  }

  .matrix-text {
    font-family: ${theme.fonts.mono};
    color: ${theme.colors.matrix};
    text-shadow: 0 0 10px ${theme.colors.matrix};
  }
`

export const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;

  @media (min-width: ${theme.breakpoints.tablet}) {
    padding: 0 2rem;
  }
`

export const Card = styled.div`
  background: ${theme.colors.surface};
  border: 1px solid ${theme.colors.border};
  border-radius: 8px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
`

export const Button = styled.button<{ variant?: 'primary' | 'secondary' | 'ghost' }>`
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: ${theme.fonts.primary};
  
  ${props => {
    switch (props.variant) {
      case 'secondary':
        return `
          background: ${theme.colors.surface};
          color: ${theme.colors.text};
          border: 1px solid ${theme.colors.border};
          
          &:hover {
            background: ${theme.colors.surfaceLight};
            border-color: ${theme.colors.primary};
          }
        `
      case 'ghost':
        return `
          background: transparent;
          color: ${theme.colors.textMuted};
          
          &:hover {
            color: ${theme.colors.text};
            background: ${theme.colors.surface};
          }
        `
      default:
        return `
          background: linear-gradient(135deg, ${theme.colors.primary}, ${theme.colors.secondary});
          color: white;
          
          &:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(107, 70, 193, 0.4);
          }
        `
    }
  }}
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }
`

export const Input = styled.input`
  width: 100%;
  padding: 0.75rem;
  background: ${theme.colors.surface};
  border: 1px solid ${theme.colors.border};
  border-radius: 6px;
  color: ${theme.colors.text};
  font-family: ${theme.fonts.primary};
  
  &:focus {
    outline: none;
    border-color: ${theme.colors.primary};
    box-shadow: 0 0 0 2px rgba(107, 70, 193, 0.2);
  }
  
  &::placeholder {
    color: ${theme.colors.textMuted};
  }
`
