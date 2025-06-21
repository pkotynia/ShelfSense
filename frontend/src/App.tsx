import { createBrowserRouter, RouterProvider, Navigate, Outlet } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { NavigationHeader } from './components/navigation/NavigationHeader';
import { ProtectedLayout } from './components/layout/ProtectedLayout';
import { ErrorBoundary } from './components/error/ErrorBoundary';
import { AuthPage } from './features/auth/pages/AuthPage';
import { ProtectedRoute } from './features/auth/components/ProtectedRoute';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: 1
    }
  }
});

// Root layout component that includes the header
function RootLayout() {
  return (
    <div className="min-h-screen flex flex-col">
      <NavigationHeader />
      <main className="flex-1">
        <Outlet /> {/* This is where child routes will render */}
      </main>
    </div>
  );
}

// Create router configuration with code splitting
const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />, // Use our layout with header at the root level
    errorElement: <ErrorBoundary><div>Not Found</div></ErrorBoundary>,
    children: [
      {
        path: '/',
        element: <ProtectedRoute><ProtectedLayout /></ProtectedRoute>,
        children: [
          {
            index: true,
            element: <Navigate to="/dashboard" replace />
          },
          {
            path: 'dashboard',
            lazy: async () => {
              const { DashboardPage } = await import('./features/dashboard/pages/DashboardPage');
              return { Component: DashboardPage };
            }
          },
          {
            path: 'preferences',
            lazy: async () => {
              const { PreferencesPage } = await import('./features/preferences/pages/PreferencesPage');
              return { Component: PreferencesPage };
            }
          }
        ]
      },
      {
        path: '/login',
        element: <AuthPage />
      },
      {
        path: '/register',
        element: <AuthPage />
      }
    ]
  },
]);

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  );
}

export default App
