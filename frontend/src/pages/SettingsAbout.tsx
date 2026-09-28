import React, { useEffect, useState } from 'react';
import { getHealth } from '../services/api';
import {
  Stethoscope,
  ShieldAlert,
  Cpu,
  FileCheck2,
  Lock,
  Info,
  CheckCircle,
  HelpCircle
} from 'lucide-react';

export const SettingsAbout: React.FC = () => {
  const [health, setHealth] = useState<any>(null);

  useEffect(() => {
    getHealth()
      .then(setHealth)
      .catch((err) => console.error('Health check failed:', err));
  }, []);

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">System Settings & About</h1>
        <p className="text-slate-600 text-sm mt-1">
          ClinReview AI application status, architecture overview, privacy notice, and medical disclaimers.
        </p>
      </div>

      {/* App Status Banner */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs space-y-4">
        <div className="flex items-center space-x-3">
          <div className="p-3 bg-blue-50 text-blue-600 rounded-xl">
            <Stethoscope className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-900">ClinReview AI</h2>
            <p className="text-xs text-slate-500 font-medium">Intelligent Clinical Document Reviewer • Version 1.0.0</p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2">
          <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-100 text-xs">
            <span className="text-slate-500 block">Backend Status</span>
            <span className="font-bold text-emerald-600 flex items-center space-x-1 mt-0.5">
              <CheckCircle className="w-3.5 h-3.5" />
              <span>{health?.status ? health.status.toUpperCase() : 'ONLINE'}</span>
            </span>
          </div>

          <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-100 text-xs">
            <span className="text-slate-500 block">AI Engine Provider</span>
            <span className="font-bold text-slate-900 capitalize mt-0.5 block">
              {health?.ai_provider || 'Mock / Heuristic Engine'}
            </span>
          </div>

          <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-100 text-xs">
            <span className="text-slate-500 block">API Key Configuration</span>
            <span className={`font-bold mt-0.5 block ${health?.ai_configured ? 'text-emerald-600' : 'text-amber-600'}`}>
              {health?.ai_configured ? 'Configured (Active API)' : 'Mock Mode (Local)'}
            </span>
          </div>
        </div>
      </div>

      {/* Grid Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Supported File Formats */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs space-y-3">
          <h3 className="text-base font-bold text-slate-900 flex items-center space-x-2">
            <FileCheck2 className="w-5 h-5 text-blue-600" />
            <span>Supported Input Formats</span>
          </h3>
          <ul className="space-y-2 text-xs text-slate-700">
            <li className="flex items-center space-x-2">
              <span className="w-2 h-2 rounded-full bg-blue-600" />
              <span><strong>Plain Text (.txt):</strong> Direct text entry or pasted consultation notes.</span>
            </li>
            <li className="flex items-center space-x-2">
              <span className="w-2 h-2 rounded-full bg-blue-600" />
              <span><strong>PDF Upload (.pdf):</strong> Text extraction via PyMuPDF with page OCR.</span>
            </li>
            <li className="flex items-center space-x-2">
              <span className="w-2 h-2 rounded-full bg-blue-600" />
              <span><strong>Images (.png, .jpg, .jpeg):</strong> Tesseract OCR engine with OpenCV enhancement.</span>
            </li>
          </ul>
        </div>

        {/* AI & ML Architecture */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs space-y-3">
          <h3 className="text-base font-bold text-slate-900 flex items-center space-x-2">
            <Cpu className="w-5 h-5 text-teal-600" />
            <span>AI / ML Pipeline</span>
          </h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Employs structured clinical entity extraction, prompt engineering, and strict Pydantic JSON schema validation. Distinguishes explicitly documented source facts from AI safety flags.
          </p>
        </div>

        {/* Security & Privacy Notice */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs space-y-3">
          <h3 className="text-base font-bold text-slate-900 flex items-center space-x-2">
            <Lock className="w-5 h-5 text-emerald-600" />
            <span>Privacy & Safe Data Policy</span>
          </h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            API keys and credentials strictly reside in environment variables. Uploaded documents are processed safely without persistent static URL exposure.
          </p>
        </div>

        {/* Synthetic Data Notice */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs space-y-3">
          <h3 className="text-base font-bold text-slate-900 flex items-center space-x-2">
            <Info className="w-5 h-5 text-purple-600" />
            <span>Synthetic Demonstration Data</span>
          </h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            All demonstration cases, patient identifiers (e.g. SYN-1001), and clinical records are entirely synthetic. No real patient health information (PHI) is used.
          </p>
        </div>
      </div>

      {/* Medical Use Disclaimer */}
      <div className="bg-amber-50 rounded-2xl p-6 border border-amber-200 text-amber-900 space-y-2">
        <h3 className="text-base font-bold flex items-center space-x-2 text-amber-950">
          <ShieldAlert className="w-5 h-5 text-amber-600" />
          <span>Medical Use Disclaimer</span>
        </h3>
        <p className="text-xs leading-relaxed text-amber-900">
          ClinReview AI is intended solely for clinical document review demonstration, research, and educational purposes. It is not a medical device, nor is it intended for direct diagnosis, treatment decisions, or replacing qualified human clinical judgment. Always verify AI-extracted information against original medical source documentation.
        </p>
      </div>
    </div>
  );
};
