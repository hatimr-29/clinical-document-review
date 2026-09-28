import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getReportDetails } from '../services/api';
import { ClinicalReport } from '../types/report';
import { StructuredReportView } from '../components/StructuredReportView';
import { ProcessingState } from '../components/ProcessingState';
import { Loader2, AlertCircle, ArrowLeft, RefreshCw } from 'lucide-react';

export const ReportDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [report, setReport] = useState<ClinicalReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (id) {
      fetchReport(id);
    }
  }, [id]);

  const fetchReport = async (reportId: string) => {
    try {
      setLoading(true);
      setError(null);
      const data = await getReportDetails(reportId);
      setReport(data);
    } catch (err: any) {
      console.error('Failed to load report:', err);
      const msg = err.response?.data?.message || err.message || `Clinical report '${reportId}' not found.`;
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
        <Loader2 className="w-10 h-10 text-blue-600 animate-spin" />
        <p className="text-slate-600 font-medium text-sm">Retrieving Clinical Report Details...</p>
      </div>
    );
  }

  if (error || !report) {
    return (
      <div className="max-w-3xl mx-auto py-12 px-4 space-y-6">
        <div className="bg-rose-50 border border-rose-200 rounded-2xl p-6 text-rose-900 flex items-start space-x-4">
          <AlertCircle className="w-6 h-6 text-rose-600 flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <h3 className="font-bold text-lg">Report Retrieval Failed</h3>
            <p className="text-sm text-rose-700 mt-1">{error || 'Report not found.'}</p>
          </div>
        </div>

        <div className="flex justify-between items-center">
          <button
            onClick={() => navigate('/history')}
            className="flex items-center space-x-2 px-4 py-2 border border-slate-300 rounded-xl text-sm font-medium text-slate-700 hover:bg-slate-50"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Return to Report History</span>
          </button>
          {id && (
            <button
              onClick={() => fetchReport(id)}
              className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-xl text-sm font-medium hover:bg-blue-700"
            >
              <RefreshCw className="w-4 h-4" />
              <span>Retry</span>
            </button>
          )}
        </div>
      </div>
    );
  }

  if (report.processing_status === 'Processing' || report.processing_status === 'Pending') {
    return (
      <ProcessingState
        reportId={report.id}
        documentName={report.document_name}
        onRetry={() => id && fetchReport(id)}
      />
    );
  }

  return (
    <div className="py-6 space-y-6">
      {/* Navigation Top Bar */}
      <div className="flex justify-between items-center">
        <Link
          to="/history"
          className="inline-flex items-center space-x-2 text-xs font-semibold text-slate-600 hover:text-blue-600 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Report History</span>
        </Link>
      </div>

      <StructuredReportView report={report} />
    </div>
  );
};
