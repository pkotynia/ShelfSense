import { Paper, Box, Typography, Container } from '@mui/material';
import type { AuthLayoutProps } from '../auth.types';

export function AuthLayout({ mode, onToggle, children }: AuthLayoutProps) {
  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography component="h1" variant="h4" sx={{ mb: 3 }}>
          {mode === 'login' ? 'Sign In' : 'Create Account'}
        </Typography>
        <Paper elevation={3} sx={{ p: 4, width: '100%' }}>
          {children}
          <Box sx={{ mt: 2, textAlign: 'center' }}>
            <Typography variant="body2">
              {mode === 'login' ? "Don't have an account? " : "Already have an account? "}
              <Typography
                component="button"
                variant="body2"
                onClick={onToggle}
                sx={{
                  background: 'none',
                  border: 'none',
                  color: 'primary.main',
                  cursor: 'pointer',
                  textDecoration: 'underline',
                  '&:hover': { opacity: 0.8 }
                }}
              >
                {mode === 'login' ? 'Sign Up' : 'Sign In'}
              </Typography>
            </Typography>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
}
