import axios from 'axios';
import { ClinicalReport, DashboardStats, PaginatedReports } from '../types/report';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api';

export const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getHealth = async () => {
  const res = await api.get('/health');
  return res.data;
};

export const getDashboardStats = async (): Promise<DashboardStats> => {
  const res = await api.get('/reports/dashboard');
  return res.data;
};

export const analyzeText = async (text: string, documentName?: string): Promise<ClinicalReport> => {
  const res = await api.post('/analyze/text', {
    text,
    document_name: documentName || 'Clinical Note.txt',
  });
  return res.data.data;
};

export const analyzeFile = async (file: File, documentName?: string): Promise<ClinicalReport> => {
  const formData = new FormData();
  formData.append('file', file);
  if (documentName) {
    formData.append('document_name', documentName);
  }

  const res = await api.post('/analyze/file', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return res.data.data;
};

export const getReports = async (
  page: number = 1,
  limit: number = 10,
  search?: string,
  status?: string
): Promise<PaginatedReports> => {
  const params: Record<string, any> = { page, limit };
  if (search) params.search = search;
  if (status && status !== 'all') params.status = status;

  const res = await api.get('/reports', { params });
  return res.data;
};

export const getReportDetails = async (id: string): Promise<ClinicalReport> => {
  const res = await api.get(`/reports/${id}`);
  return res.data.data;
};

export const getReportStatus = async (id: string) => {
  const res = await api.get(`/reports/${id}/status`);
  return res.data;
};

export const deleteReport = async (id: string) => {
  const res = await api.delete(`/reports/${id}`);
  return res.data;
};

export const getDownloadReportUrl = (id: string): string => {
  return `${API_BASE}/reports/${id}/download`;
};
