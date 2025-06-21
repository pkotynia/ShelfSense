import { useState } from 'react';
import { Box, TextField, Button, Alert } from '@mui/material';
import type { LoginFormValues, LoginFormProps } from '../auth.types';
import { loginSchema } from '../auth.types';

export function LoginForm({ onSubmit, isLoading, errorMessage }: LoginFormProps) {
  const [values, setValues] = useState<LoginFormValues>({ email: '', password: '' });
  const [errors, setErrors] = useState<Partial<LoginFormValues>>({});

  const validate = async (data: LoginFormValues) => {
    try {
      await loginSchema.parseAsync(data);
      return true;
    } catch (error) {
      if (error instanceof Error) {
        const validationErrors: Partial<LoginFormValues> = {};
        const zodError = JSON.parse(error.message);
        zodError.forEach((err: any) => {
          validationErrors[err.path[0] as keyof LoginFormValues] = err.message;
        });
        setErrors(validationErrors);
      }
      return false;
    }
  };

  const handleChange = (field: keyof LoginFormValues) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setValues({ ...values, [field]: event.target.value });
    setErrors({ ...errors, [field]: undefined });
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (await validate(values)) {
      onSubmit(values);
    }
  };

  const isFormValid = values.email && values.password && Object.keys(errors).length === 0;

  return (
    <Box component="form" onSubmit={handleSubmit} noValidate>
      {errorMessage && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {errorMessage}
        </Alert>
      )}
      <TextField
        margin="normal"
        required
        fullWidth
        id="email"
        label="Email Address"
        name="email"
        autoComplete="email"
        autoFocus
        value={values.email}
        onChange={handleChange('email')}
        error={!!errors.email}
        helperText={errors.email}
      />
      <TextField
        margin="normal"
        required
        fullWidth
        name="password"
        label="Password"
        type="password"
        id="password"
        autoComplete="current-password"
        value={values.password}
        onChange={handleChange('password')}
        error={!!errors.password}
        helperText={errors.password}
      />
      <Button
        type="submit"
        fullWidth
        variant="contained"
        sx={{ mt: 3, mb: 2 }}
        disabled={!isFormValid || isLoading}
      >
        {isLoading ? 'Signing in...' : 'Sign In'}
      </Button>
    </Box>
  );
}
