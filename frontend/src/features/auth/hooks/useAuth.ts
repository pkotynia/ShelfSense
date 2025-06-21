import { useMutation } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import type { 
  AuthResponse, 
  LoginFormValues, 
  RegisterFormValues,
  AuthError
} from '../auth.types';

import { api } from '../../../services/api';

async function loginUser(data: LoginFormValues): Promise<AuthResponse> {
  return api.post('/auth/login', data, { requiresAuth: false });
}

async function registerUser(data: RegisterFormValues): Promise<AuthResponse> {
  return api.post('/auth/register', data, { requiresAuth: false });
}

export function useAuth() {
  const navigate = useNavigate();

  const loginMutation = useMutation<AuthResponse, AuthError, LoginFormValues>({
    mutationFn: loginUser,
    onSuccess: (data) => {
      localStorage.setItem('auth_token', data.token);
      navigate('/dashboard');
    }
  });

  const registerMutation = useMutation<AuthResponse, AuthError, RegisterFormValues>({
    mutationFn: registerUser,
    onSuccess: (data) => {
      localStorage.setItem('auth_token', data.token);
      navigate('/dashboard');
    }
  });
  const logout = () => {
    localStorage.removeItem('auth_token');
    navigate('/login');
  };

  return {
    login: loginMutation.mutate,
    register: registerMutation.mutate,
    logout,
    isLoading: loginMutation.isPending || registerMutation.isPending,
    error: loginMutation.error?.message || registerMutation.error?.message
  };
}
