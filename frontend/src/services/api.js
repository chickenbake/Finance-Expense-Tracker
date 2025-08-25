import axios from 'axios';

const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://finance-expense-tracker-467666307950.us-central1.run.app/api'
  : process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && localStorage.getItem('token')) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth services
export const authService = {
  register: async (username, password) => {
    const response = await api.post('/register', { username, password });
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  login: async (username, password) => {
    const response = await api.post('/login', { username, password });
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  getCurrentUser: () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },

  isAuthenticated: () => {
    return !!localStorage.getItem('token');
  },
};

// Expense services
export const expenseService = {
  getExpenses: async () => {
    const response = await api.get('/expenses');
    return response.data;
  },

  addExpense: async (expenseData) => {
    const token = localStorage.getItem('token');
    
    try {
      const response = await api.post('/expenses', expenseData);
      return response.data;
    } catch (error) {
      console.error('🚨 API Error:', error.response?.status, error.response?.data);
      throw error;
    }
  },

  updateExpense: async (expenseId, expenseData) => {
    const response = await api.put(`/expenses/${expenseId}`, expenseData);
    return response.data;
  },

  deleteExpense: async (expenseId) => {
    const response = await api.delete(`/expenses/${expenseId}`);
    return response.data;
  },

  getDashboardSummary: async () => {
    const response = await api.get('/dashboard/summary');
    return response.data;
  },
};

export default api;
