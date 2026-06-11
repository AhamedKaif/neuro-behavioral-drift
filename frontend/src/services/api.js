import axios from 'axios';

// Axios instance with base config
const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
});

// Attach JWT token automatically to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 (token expired / invalid) globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (username, password) =>
    api.post('/auth/register', { username, password }),
  login: (username, password) =>
    api.post('/auth/login', { username, password }),
  me: () => api.get('/auth/me'),
};

// Behavioral Metrics API
export const metricsAPI = {
  ingest: (payload) => api.post('/metrics', payload),
  dashboard: () => api.get('/dashboard'),
};

// Alerts API
export const alertsAPI = {
  list: () => api.get('/alerts'),
  markRead: (alertId) =>
    api.post('/alerts/read', alertId ? { alert_id: alertId } : {}),
};

// Model API
export const modelAPI = {
  info: () => api.get('/model/info'),
  retrain: () => api.post('/model/retrain'),
};

export default api;
