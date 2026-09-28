import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getDashboardStats } from '../services/api';
import { DashboardStats } from '../types/report';
import { formatDate, getStatusBadgeColor } from '../utils/helpers';
import {
  FileText,
  CheckCircle2,
  XCircle,
  FilePlus,
  ArrowRight,
  Clock,
  Activity,
  Sparkles,
  Loader2,
  AlertCircle
} from 'lucide-react';

export const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getDashboardStats();
      setStats(data);
    } catch (err: any) {
      console.error('Failed to load dashboard statistics:', err);
      setError('Could not connect to backend API server. Please ensure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
        <Loader2 className="w-10 h-10 text-blue-600 animate-spin" />
        <p className="text-slate-600 font-medium text-sm">Loading ClinReview AI Dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto py-12 px-4">
        <div className="bg-rose-50 border border-rose-200 rounded-2xl p-6 text-rose-900 flex items-start space-x-4">
          <AlertCircle className="w-6 h-6 text-rose-600 flex-shrink-0 mt-1" />
          <div className="flex-1">
            <h3 className="font-bold text-lg">Backend Connection Error</h3>
            <p className="text-sm text-rose-700 mt-1">{error}</p>
            <button
              onClick={fetchStats}
              className="mt-4 px-4 py-2 bg-rose-600 text-white rounded-lg text-sm font-semibold hover:bg-rose-700 transition-colors"
            >
              Retry Connection
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 py-6">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-blue-900 via-blue-800 to-teal-800 rounded-3xl p-8 text-white shadow-xl relative overflow-hidden">
        <div className="absolute -right-10 -bottom-10 opacity-10 pointer-events-none">
          <Activity className="w-80 h-80 text-white" />
        </div>
        <div className="relative z-10 max-w-3xl space-y-4">
          <div className="inline-flex items-center space-x-2 bg-white/10 backdrop-blur-md px-3 py-1 rounded-full text-xs font-medium text-blue-200 border border-white/10">
            <Sparkles className="w-3.5 h-3.5 text-teal-300" />
            <span>AI Clinical Extraction & Review Dashboard</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight">
            Welcome to ClinReview AI
          </h1>
          <p className="text-blue-100 text-sm sm:text-base leading-relaxed">
            Automated clinical document review system. Process plain text notes, PDFs, or scanned medical images to extract structured clinical entities, vital signs, allergies, and safety concerns.
          </p>
          <div className="pt-2 flex flex-wrap gap-4">
            <button
              onClick={() => navigate('/new-review')}
              className="flex items-center space-x-2 px-6 py-3 bg-white text-blue-900 font-bold rounded-xl hover:bg-blue-50 shadow-md transition-transform duration-150 active:scale-95"
            >
              <FilePlus className="w-5 h-5 text-blue-700" />
              <span>Review New Document</span>
            </button>
            <Link
              to="/history"
              className="flex items-center space-x-2 px-5 py-3 bg-white/10 text-white font-medium rounded-xl hover:bg-white/20 border border-white/20 backdrop-blur-xs transition-colors"
            >
              <span>View History</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </div>

      {/* Database Statistics Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs flex items-center space-x-4">
          <div className="p-3.5 bg-blue-50 text-blue-700 rounded-2xl border border-blue-100">
            <FileText className="w-7 h-7" />
          </div>
          <div>
            <span className="text-xs font-semibold uppercase text-slate-500 tracking-wider">Total Processed</span>
            <div className="text-3xl font-extrabold text-slate-900">{stats?.total_documents ?? 0}</div>
          </div>
        </div>

        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs flex items-center space-x-4">
          <div className="p-3.5 bg-emerald-50 text-emerald-700 rounded-2xl border border-emerald-100">
            <CheckCircle2 className="w-7 h-7" />
          </div>
          <div>
            <span className="text-xs font-semibold uppercase text-slate-500 tracking-wider">Completed Analyses</span>
            <div className="text-3xl font-extrabold text-slate-900">{stats?.completed_analyses ?? 0}</div>
          </div>
        </div>

        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs flex items-center space-x-4">
          <div className="p-3.5 bg-rose-50 text-rose-700 rounded-2xl border border-rose-100">
            <XCircle className="w-7 h-7" />
          </div>
          <div>
            <span className="text-xs font-semibold uppercase text-slate-500 tracking-wider">Failed Analyses</span>
            <div className="text-3xl font-extrabold text-slate-900">{stats?.failed_analyses ?? 0}</div>
          </div>
        </div>
      </div>

      {/* Recent Activity & Quick Action */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
        <div className="p-6 border-b border-slate-100 flex justify-between items-center">
          <div>
            <h2 className="text-lg font-bold text-slate-900">Recent Clinical Reports</h2>
            <p className="text-xs text-slate-500 mt-0.5">Retrieved dynamically from backend database</p>
          </div>
          <Link
            to="/history"
            className="text-xs font-semibold text-blue-600 hover:text-blue-800 flex items-center space-x-1"
          >
            <span>View All Reports</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {stats?.recent_reports && stats.recent_reports.length > 0 ? (
          <div className="divide-y divide-slate-100">
            {stats.recent_reports.map((report) => (
              <div
                key={report.id}
                onClick={() => navigate(`/reports/${report.id}`)}
                className="p-5 hover:bg-slate-50/80 cursor-pointer transition-colors flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-3 sm:space-y-0"
              >
                <div className="space-y-1 max-w-xl">
                  <div className="flex items-center space-x-3">
                    <span className="font-bold text-slate-900 text-sm hover:text-blue-600 transition-colors">
                      {report.document_name}
                    </span>
                    <span
                      className={`px-2.5 py-0.5 rounded-full text-xs font-semibold border ${getStatusBadgeColor(
                        report.processing_status
                      )}`}
                    >
                      {report.processing_status}
                    </span>
                    <span className="text-xs font-mono text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
                      {report.input_type.toUpperCase()}
                    </span>
                  </div>
                  <p className="text-xs text-slate-600 line-clamp-1">
                    {report.report_summary || 'Analysis completed.'}
                  </p>
                </div>

                <div className="flex items-center space-x-4 text-xs text-slate-500">
                  <span className="flex items-center space-x-1">
                    <Clock className="w-3.5 h-3.5 text-slate-400" />
                    <span>{formatDate(report.created_at)}</span>
                  </span>
                  <span className="font-medium text-blue-600 group-hover:translate-x-1 transition-transform">
                    View Report &rarr;
                  </span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="p-12 text-center space-y-4">
            <div className="w-12 h-12 rounded-2xl bg-blue-50 text-blue-600 mx-auto flex items-center justify-center">
              <FileText className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-slate-800 font-bold">No Clinical Reports Found</h3>
              <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1">
                You have not analyzed any clinical documents yet. Upload a document or type clinical notes to generate your first report.
              </p>
            </div>
            <button
              onClick={() => navigate('/new-review')}
              className="px-5 py-2.5 bg-blue-600 text-white rounded-xl text-xs font-semibold hover:bg-blue-700 shadow-sm"
            >
              Upload First Document
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
