import type { LoginFormValues } from '../auth.types';

export interface LoginFormProps {
  onSubmit: (values: LoginFormValues) => void;
  isLoading: boolean;
  errorMessage?: string;
}
