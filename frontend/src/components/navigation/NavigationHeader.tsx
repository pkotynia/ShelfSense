import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { useAuth } from '../../features/auth/hooks/useAuth';

export function NavigationHeader() {
  const { logout } = useAuth();
  const token = localStorage.getItem('auth_token');

  if (!token) {
    return null;
  }

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          ShelfSense
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button color="inherit" href="/dashboard">
            Dashboard
          </Button>
          <Button color="inherit" href="/preferences">
            Preferences
          </Button>
          <Button color="inherit" onClick={logout}>
            Logout
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
}
