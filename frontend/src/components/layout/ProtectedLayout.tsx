import { Suspense } from 'react';
import { Outlet } from 'react-router-dom';
import { Container, Box } from '@mui/material';
import { ErrorBoundary } from '../error/ErrorBoundary';
import { LoadingSpinner } from '../ui/LoadingSpinner';

export function ProtectedLayout() {
  return (
    <ErrorBoundary>
      <Container maxWidth="lg">
        <Box sx={{ py: 4 }}>
          <Suspense fallback={<LoadingSpinner />}>
            <Outlet />
          </Suspense>
        </Box>
      </Container>
    </ErrorBoundary>
  );
}
