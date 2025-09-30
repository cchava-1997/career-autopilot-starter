import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const api = {
  // Jobs API
  jobs: {
    list: () => apiClient.get('/jobs/list'),
    add: (job: any) => apiClient.post('/jobs/add', job),
    updateStatus: (jobId: string, status: string) => 
      apiClient.post('/jobs/status', { job_id: jobId, status }),
    get: (jobId: string) => apiClient.get(`/jobs/${jobId}`),
    update: (jobId: string, updates: any) => 
      apiClient.put(`/jobs/${jobId}`, updates),
    delete: (jobId: string) => apiClient.delete(`/jobs/${jobId}`),
  },

  // Resumes API
  resumes: {
    list: (track?: string) => 
      apiClient.get('/resume/list', { params: { track } }),
    upload: (file: File, track: string, version: string) => {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('track', track);
      formData.append('version', version);
      return apiClient.post('/resume/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
    },
    setDefault: (resumeId: string) => 
      apiClient.post('/resume/set-default', { resume_id: resumeId }),
  },

  // Overleaf API
  overleaf: {
    build: (track: string, jobId: string) => 
      apiClient.post('/overleaf/build', { track, job_id: jobId }),
    openLink: (url: string) => 
      apiClient.post('/overleaf/open-link', { url }),
  },

  // Job Sources API
  sources: {
    list: () => apiClient.get('/sites/'),
    add: (site: any) => apiClient.post('/sites/', site),
    update: (siteId: string, updates: any) => 
      apiClient.put(`/sites/${siteId}`, updates),
    delete: (siteId: string) => apiClient.delete(`/sites/${siteId}`),
    test: (siteId: string) => apiClient.post(`/sites/${siteId}/test`),
  },

  // Apply Pack API
  apply: {
    prepare: (data: any) => apiClient.post('/apply/prepare', data),
  },

  // Outreach API
  outreach: {
    plan: (jobId: string, company: string, role: string) => 
      apiClient.post('/outreach/plan', { job_id: jobId, company, role }),
    drafts: (jobId: string) => 
      apiClient.post('/outreach/drafts', { job_id: jobId }),
  },

  // Follow-ups API
  followups: {
    schedule: (jobId: string) => 
      apiClient.post('/followups/schedule', { job_id: jobId }),
  },

  // Summary API
  summary: {
    today: () => apiClient.post('/summary/today'),
  },

  // Dashboard API
  dashboard: {
    stats: () => apiClient.get('/dashboard/stats'),
  },

  // Settings API
  settings: {
    get: () => apiClient.get('/settings/'),
    update: (settings: any) => apiClient.put('/settings/', settings),
    testOverleaf: () => apiClient.post('/settings/test-overleaf'),
    testChrome: () => apiClient.post('/settings/test-chrome'),
    testLaTeX: () => apiClient.post('/settings/test-latex'),
  },

  // Health check
  health: () => apiClient.get('/health'),
};

export default api;