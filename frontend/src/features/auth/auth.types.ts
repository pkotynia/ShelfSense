import { z } from 'zod';

// Validation schemas
export const loginSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string().min(1, 'Password is required')
});

export const registerSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/(?=.*[A-Za-z])(?=.*\d)/, 'Password must contain both letters and numbers')
});

// Form value types
export interface LoginFormValues {
  email: string;
  password: string;
}

export interface RegisterFormValues {
  email: string;
  password: string;
}

// API types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  id: string;
  email: string;
  token: string;
}

// Component prop types
export type AuthMode = 'login' | 'register';

export interface AuthLayoutProps {
  mode: AuthMode;
  onToggle: () => void;
  children: React.ReactNode;
}

export interface LoginFormProps {
  onSubmit: (values: LoginFormValues) => void;
  isLoading: boolean;
  errorMessage?: string;
}

export interface RegisterFormProps {
  onSubmit: (values: RegisterFormValues) => void;
  isLoading: boolean;
  errorMessage?: string;
}

export type AuthError = {
  message: string;
  status?: number;
};