import { useState } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthLayout } from '../components/AuthLayout';
import { LoginForm } from '../components/LoginForm';
import { RegisterForm } from '../components/RegisterForm';
import { useAuth } from '../hooks/useAuth';
import type { AuthMode } from '../auth.types';

export function AuthPage() {
  const [mode, setMode] = useState<AuthMode>('login');
  const { login, register, isLoading, error } = useAuth();
  
  // If user is already authenticated, redirect to dashboard
  const token = localStorage.getItem('auth_token');
  if (token) {
    return <Navigate to="/dashboard" replace />;
  }

  const toggleMode = () => {
    setMode(mode === 'login' ? 'register' : 'login');
  };

  return (
    <AuthLayout mode={mode} onToggle={toggleMode}>
      {mode === 'login' ? (
        <LoginForm
          onSubmit={login}
          isLoading={isLoading}
          errorMessage={error}
        />
      ) : (
        <RegisterForm
          onSubmit={register}
          isLoading={isLoading}
          errorMessage={error}
        />
      )}
    </AuthLayout>
  );
}
