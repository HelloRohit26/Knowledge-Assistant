import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

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

// ── AI Workflows & Copilot APIs ──
export const fetchWorkflowTemplates = () =>
  api.get('/api/workflows/templates');

export const createWorkflowTemplate = (data) =>
  api.post('/api/workflows/templates', data);

export const executeWorkflow = (workflowId, inputs = {}, customTemplate = null) =>
  api.post('/api/workflows/execute', { workflow_id: workflowId, inputs, custom_template: customTemplate });

export const fetchWorkflowHistory = (limit = 50, category = null) =>
  api.get('/api/workflows/history', { params: { limit, category } });

export const fetchWorkflowRunDetail = (runId) =>
  api.get(`/api/workflows/history/${runId}`);

export const exportWorkflowPDF = (title, category, markdownContent) =>
  api.post('/api/workflows/export/pdf', { title, category, markdown_content: markdownContent }, { responseType: 'blob' });

export const exportWorkflowDOCX = (title, category, markdownContent) =>
  api.post('/api/workflows/export/docx', { title, category, markdown_content: markdownContent }, { responseType: 'blob' });

export const fetchCopilotSuggestions = () =>
  api.get('/api/copilot/suggestions');

// ── Next-Level SaaS & Multi-Agent APIs ──
export const executeMultiAgentTask = (task, agents = null) =>
  api.post('/api/platform/multi-agent/collaborate', { task, agents });

export const fetchKnowledgeGraph = () =>
  api.get('/api/platform/knowledge-graph');

export const fetchMemory = (memoryType = null) =>
  api.get('/api/platform/memory', { params: { memory_type: memoryType } });

export const fetchAutomationRules = () =>
  api.get('/api/platform/automation/rules');

export const fetchOrganizationInfo = () =>
  api.get('/api/platform/organization');

export const fetchApiKeys = () =>
  api.get('/api/platform/api-keys');

export const createApiKey = (name = 'Developer Key') =>
  api.post('/api/platform/api-keys', { name });


