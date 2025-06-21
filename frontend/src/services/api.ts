const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface ApiError {
  message: string;
  status: number;
}

interface ApiConfig extends RequestInit {
  requiresAuth?: boolean;
}

async function apiClient<T>(endpoint: string, config: ApiConfig = {}): Promise<T> {
  const { requiresAuth = true, ...fetchConfig } = config;
  
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(fetchConfig.headers as Record<string, string>),
  };

  if (requiresAuth) {
    const token = localStorage.getItem('auth_token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...fetchConfig,
    headers,
  });

  // Handle 401 Unauthorized by redirecting to login
  if (response.status === 401) {
    localStorage.removeItem('auth_token');
    window.location.href = '/login';
    throw new Error('Session expired. Please login again.');
  }

  // Handle other error responses
  if (!response.ok) {
    const error: ApiError = {
      message: 'An error occurred',
      status: response.status,
    };

    try {
      const data = await response.json();
      error.message = data.detail || data.message || error.message;
    } catch {
      // If the error response is not JSON, use the status text
      error.message = response.statusText;
    }

    throw error;
  }

  return response.json();
}

export const api = {
  get: <T>(endpoint: string, config?: ApiConfig) => 
    apiClient<T>(endpoint, { ...config, method: 'GET' }),
  
  post: <T>(endpoint: string, body: unknown, config?: ApiConfig) =>
    apiClient<T>(endpoint, { ...config, method: 'POST', body: JSON.stringify(body) }),
  
  put: <T>(endpoint: string, body: unknown, config?: ApiConfig) =>
    apiClient<T>(endpoint, { ...config, method: 'PUT', body: JSON.stringify(body) }),
  
  delete: <T>(endpoint: string, config?: ApiConfig) =>
    apiClient<T>(endpoint, { ...config, method: 'DELETE' }),
};
