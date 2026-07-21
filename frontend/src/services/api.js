import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to inject JWT token if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;

// ── Auth APIs ──
export const loginUser = (username, password) =>
  api.post('/api/auth/login', { username, password });

export const registerUser = (data) =>
  api.post('/api/auth/register', data);

export const getCurrentUser = () =>
  api.get('/api/auth/me');

// ── Document APIs ──
export const fetchDocuments = (params) =>
  api.get('/api/documents', { params });

export const fetchDocumentDetail = (filePath) =>
  api.get('/api/documents/detail', { params: { file_path: filePath } });

export const uploadDocument = (formData) =>
  api.post('/api/documents/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });

export const deleteDocument = (filePath) =>
  api.delete('/api/documents/remove', { params: { file_path: filePath } });

export const updateDocumentMetadata = (filePath, metadata) =>
  api.put('/api/documents/metadata', metadata, { params: { file_path: filePath } });

// ── Search & Chat APIs ──
export const searchKnowledgeBase = (query, topK = 5, filters = null) =>
  api.post('/api/search', { query, top_k: topK, filters });

export const sendChatMessage = (question, mode = 'standard') =>
  api.post('/api/chat', { question, mode });

// ── Registry & System Health APIs ──
export const fetchRegistryStats = () =>
  api.get('/api/registry/stats');

export const fetchSystemHealth = () =>
  api.get('/api/registry/health');

export const triggerReindex = () =>
  api.post('/api/registry/reindex');

// ── Admin & Analytics APIs ──
export const fetchAnalytics = () =>
  api.get('/api/analytics');

export const fetchUsers = () =>
  api.get('/api/admin/users');

export const toggleUserStatus = (userId, isActive) =>
  api.put(`/api/admin/users/${userId}/status`, null, { params: { is_active: isActive } });

export const removeUser = (userId) =>
  api.delete(`/api/admin/users/${userId}`);
