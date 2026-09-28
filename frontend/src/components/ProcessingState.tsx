import React, { useEffect, useState } from 'react';
import { CheckCircle2, Loader2, AlertCircle, RefreshCw, FileText, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface ProcessingStateProps {
  reportId?: string;
  documentName?: string;
  onRetry?: () => void;
  error?: string | null;
}

const STAGES = [
  { id: 1, label: 'Document received & validated', duration: 400 },
  { id: 2, label: 'Extracting text & OCR document content', duration: 1200 },
  { id: 3, label: 'Analyzing clinical entities & symptoms', duration: 2200 },
  { id: 4, label: 'Generating structured JSON clinical review', duration: 3200 },
  { id: 5, label: 'Persisting report to database', duration: 4000 },
];

export const ProcessingState: React.FC<ProcessingStateProps> = ({
  reportId,
  documentName = 'Clinical Document',
  onRetry,
  error,
}) => {
  const [currentStage, setCurrentStage] = useState(1);
  const navigate = useNavigate();

  useEffect(() => {
    if (error) return;

    const timers = STAGES.map((stage) => {
      return setTimeout(() => {
        setCurrentStage(stage.id);
      }, stage.duration);
    });

    return () => {
      timers.forEach((t) => clearTimeout(t));
    };
  }, [error]);

  const progressPercent = Math.min(100, Math.round((currentStage / STAGES.length) * 100));

  return (
    <div className="max-w-2xl mx-auto py-12 px-4">
      <div className="bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
        {/* Header Header */}
        <div className="bg-gradient-to-r from-blue-900 via-blue-800 to-teal-800 p-8 text-white">
          <div className="flex items-center space-x-3 mb-2">
            <div className="p-2.5 bg-white/10 backdrop-blur-md rounded-xl">
              <FileText className="w-6 h-6 text-blue-200" />
            </div>
            <div>
              <h2 className="text-xl font-bold">Clinical Document Processing</h2>
              <p className="text-sm text-blue-200 font-medium truncate max-w-md">{documentName}</p>
            </div>
          </div>
        </div>

        <div className="p-8">
          {error ? (
            <div className="space-y-6">
              <div className="flex items-start space-x-4 bg-rose-50 border border-rose-200 p-5 rounded-xl">
                <AlertCircle className="w-6 h-6 text-rose-600 flex-shrink-0 mt-0.5" />
                <div>
                  <h3 className="font-semibold text-rose-900">Processing Error Occurred</h3>
                  <p className="text-sm text-rose-700 mt-1">{error}</p>
                </div>
              </div>

              <div className="flex justify-end space-x-3">
                <button
                  onClick={() => navigate('/new-review')}
                  className="px-4 py-2.5 border border-slate-300 text-slate-700 font-medium text-sm rounded-lg hover:bg-slate-50"
                >
                  Back to New Review
                </button>
                {onRetry && (
                  <button
                    onClick={onRetry}
                    className="flex items-center space-x-2 px-5 py-2.5 bg-blue-600 text-white font-medium text-sm rounded-lg hover:bg-blue-700 shadow-md shadow-blue-500/20"
                  >
                    <RefreshCw className="w-4 h-4" />
                    <span>Retry Processing</span>
                  </button>
                )}
              </div>
            </div>
          ) : (
            <div className="space-y-8">
              {/* Progress Bar */}
              <div>
                <div className="flex justify-between items-center text-sm font-semibold text-slate-700 mb-2">
                  <span className="flex items-center space-x-2">
                    <Loader2 className="w-4 h-4 text-blue-600 animate-spin" />
                    <span>Processing Clinical Pipeline...</span>
                  </span>
                  <span className="text-blue-600">{progressPercent}%</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                  <div
                    className="bg-gradient-to-r from-blue-600 to-teal-500 h-2.5 rounded-full transition-all duration-500 ease-out"
                    style={{ width: `${progressPercent}%` }}
                  />
                </div>
              </div>

              {/* Stage Stepper */}
              <div className="space-y-4">
                {STAGES.map((stage) => {
                  const isCompleted = currentStage > stage.id;
                  const isCurrent = currentStage === stage.id;

                  return (
                    <div
                      key={stage.id}
                      className={`flex items-center space-x-3.5 p-3 rounded-lg border transition-all ${
                        isCurrent
                          ? 'bg-blue-50/70 border-blue-200 text-blue-900 font-medium shadow-xs'
                          : isCompleted
                          ? 'bg-slate-50/50 border-slate-100 text-slate-700'
                          : 'opacity-40 border-transparent text-slate-400'
                      }`}
                    >
                      {isCompleted ? (
                        <CheckCircle2 className="w-5 h-5 text-emerald-600 flex-shrink-0" />
                      ) : isCurrent ? (
                        <Loader2 className="w-5 h-5 text-blue-600 animate-spin flex-shrink-0" />
                      ) : (
                        <div className="w-5 h-5 rounded-full border-2 border-slate-300 flex items-center justify-center text-xs text-slate-400 flex-shrink-0">
                          {stage.id}
                        </div>
                      )}
                      <span className="text-sm">{stage.label}</span>
                    </div>
                  );
                })}
              </div>

              {/* Action when complete */}
              {reportId && currentStage >= STAGES.length && (
                <div className="pt-4 flex justify-end">
                  <button
                    onClick={() => navigate(`/reports/${reportId}`)}
                    className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-teal-600 text-white font-semibold text-sm rounded-xl hover:from-blue-700 hover:to-teal-700 shadow-md shadow-blue-500/20"
                  >
                    <span>View Generated Clinical Report</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
