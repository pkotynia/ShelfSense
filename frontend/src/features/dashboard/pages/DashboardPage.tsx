import { Typography, Paper, Box } from '@mui/material';

export function DashboardPage() {
  return (
    <Paper sx={{ p: 4 }}>
      <Box>
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Welcome to ShelfSense! Your personal library management system.
        </Typography>
      </Box>
    </Paper>
  );
}
