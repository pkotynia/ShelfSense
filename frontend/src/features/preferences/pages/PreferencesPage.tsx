import { Typography, Paper, Box } from '@mui/material';

export function PreferencesPage() {
  return (
    <Paper sx={{ p: 4 }}>
      <Box>
        <Typography variant="h4" gutterBottom>
          User Preferences
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Customize your ShelfSense experience here.
        </Typography>
      </Box>
    </Paper>
  );
}
