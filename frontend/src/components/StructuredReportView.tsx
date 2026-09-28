import React, { useState } from 'react';
import { ClinicalReport } from '../types/report';
import { formatDate, getStatusBadgeColor } from '../utils/helpers';
import { getDownloadReportUrl } from '../services/api';
import {
  Download,
  Copy,
  Check,
  FileText,
  User,
  Activity,
  Pill,
  AlertTriangle,
  HelpCircle,
  ShieldAlert,
  FileCheck,
  CheckCircle,
  Eye,
  Info
} from 'lucide-react';

interface StructuredReportViewProps {
  report: ClinicalReport;
}

export const StructuredReportView: React.FC<StructuredReportViewProps> = ({ report }) => {
  const [copiedSummary, setCopiedSummary] = useState(false);
  const [showRawText, setShowRawText] = useState(false);

  const structured = report.structured_report || {
    report_summary: report.report_summary || '',
    patient_information: {},
    symptoms: [],
    diagnoses: [],
    medications: [],
    vital_signs: {},
    allergies: [],
    clinical_observations: [],
    clinical_concerns: [],
    missing_information: [],
    potential_inconsistencies: [],
    requires_review: [],
    extraction_warnings: [],
    processing_metadata: {}
  };

  const handleCopySummary = () => {
    if (structured.report_summary) {
      navigator.clipboard.writeText(structured.report_summary);
      setCopiedSummary(true);
      setTimeout(() => setCopiedSummary(false), 2000);
    }
  };

  const patient = structured.patient_information || {};
  const vitals = structured.vital_signs || {};

  return (
    <div className="space-y-8">
      {/* Header & Actions Bar */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center space-y-4 md:space-y-0">
        <div>
          <div className="flex items-center space-x-3 mb-1">
            <h1 className="text-2xl font-bold text-slate-900">{report.document_name}</h1>
            <span
              className={`px-3 py-1 rounded-full text-xs font-semibold border ${getStatusBadgeColor(
                report.processing_status
              )}`}
            >
              {report.processing_status}
            </span>
          </div>
          <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500 font-medium">
            <span>Report ID: <strong className="text-slate-700">{report.id}</strong></span>
            <span>•</span>
            <span>Input Type: <strong className="text-slate-700 capitalize">{report.input_type}</strong></span>
            <span>•</span>
            <span>Extraction: <strong className="text-slate-700">{report.extraction_method}</strong></span>
            <span>•</span>
            <span>Processed: <strong className="text-slate-700">{formatDate(report.created_at)}</strong></span>
          </div>
        </div>

        <div className="flex items-center space-x-3 w-full sm:w-auto">
          <button
            onClick={() => setShowRawText(!showRawText)}
            className="flex-1 sm:flex-none flex items-center justify-center space-x-2 px-3.5 py-2 border border-slate-300 text-slate-700 text-sm font-medium rounded-lg hover:bg-slate-50 transition-colors"
          >
            <Eye className="w-4 h-4" />
            <span>{showRawText ? 'Hide Source Text' : 'View Source Text'}</span>
          </button>

          <button
            onClick={handleCopySummary}
            className="flex-1 sm:flex-none flex items-center justify-center space-x-2 px-3.5 py-2 border border-slate-300 text-slate-700 text-sm font-medium rounded-lg hover:bg-slate-50 transition-colors"
          >
            {copiedSummary ? <Check className="w-4 h-4 text-emerald-600" /> : <Copy className="w-4 h-4" />}
            <span>{copiedSummary ? 'Copied!' : 'Copy Summary'}</span>
          </button>

          <a
            href={getDownloadReportUrl(report.id)}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 sm:flex-none flex items-center justify-center space-x-2 px-4 py-2 bg-blue-600 text-white text-sm font-semibold rounded-lg hover:bg-blue-700 shadow-sm shadow-blue-500/20 transition-colors"
          >
            <Download className="w-4 h-4" />
            <span>Download PDF</span>
          </a>
        </div>
      </div>

      {/* Optional Raw Extracted Text View */}
      {showRawText && (
        <div className="bg-slate-900 text-slate-100 rounded-2xl p-6 border border-slate-800 shadow-md">
          <div className="flex justify-between items-center mb-3">
            <h3 className="text-sm font-bold text-blue-400 uppercase tracking-wider flex items-center space-x-2">
              <FileText className="w-4 h-4" />
              <span>Original Extracted Text</span>
            </h3>
            <span className="text-xs text-slate-400">{report.extracted_text.length} characters</span>
          </div>
          <pre className="text-xs font-mono bg-slate-950 p-4 rounded-xl overflow-x-auto whitespace-pre-wrap text-slate-300 leading-relaxed max-h-96">
            {report.extracted_text}
          </pre>
        </div>
      )}

      {/* 1. Report Summary Card */}
      <div className="bg-gradient-to-br from-blue-900 via-blue-800 to-teal-900 rounded-2xl p-6 text-white shadow-md">
        <h2 className="text-lg font-bold flex items-center space-x-2 mb-3 text-blue-200">
          <FileCheck className="w-5 h-5 text-teal-400" />
          <span>1. Clinical Report Summary</span>
        </h2>
        <p className="text-sm sm:text-base leading-relaxed text-blue-50 font-normal">
          {structured.report_summary || report.report_summary || 'No report summary generated.'}
        </p>
      </div>

      {/* Grid Layout for Patient & Vitals */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* 2. Patient Information */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
          <h3 className="text-base font-bold text-slate-900 flex items-center space-x-2 mb-4 border-b pb-3 border-slate-100">
            <User className="w-5 h-5 text-blue-600" />
            <span>2. Patient Information</span>
          </h3>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-xs font-medium text-slate-500 uppercase block mb-1">Patient ID</span>
              <span className="font-semibold text-slate-900">{patient.patient_id || 'Not documented'}</span>
            </div>
            <div>
              <span className="text-xs font-medium text-slate-500 uppercase block mb-1">Age</span>
              <span className="font-semibold text-slate-900">{patient.age !== null && patient.age !== undefined ? patient.age : 'Not documented'}</span>
            </div>
            <div>
              <span className="text-xs font-medium text-slate-500 uppercase block mb-1">Sex</span>
              <span className="font-semibold text-slate-900 capitalize">{patient.sex || 'Not documented'}</span>
            </div>
            <div>
              <span className="text-xs font-medium text-slate-500 uppercase block mb-1">Demographics</span>
              <span className="font-semibold text-slate-900">{patient.demographics || 'Not documented'}</span>
            </div>
          </div>
        </div>

        {/* 6. Vital Signs */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
          <h3 className="text-base font-bold text-slate-900 flex items-center space-x-2 mb-4 border-b pb-3 border-slate-100">
            <Activity className="w-5 h-5 text-teal-600" />
            <span>6. Vital Signs</span>
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-sm">
            <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-100">
              <span className="text-xs text-slate-500 block">Blood Pressure</span>
              <span className="font-bold text-slate-800">{vitals.blood_pressure || 'Unavailable'}</span>
            </div>
            <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-100">
              <span className="text-xs text-slate-500 block">Heart Rate</span>
              <span className="font-bold text-slate-800">{vitals.heart_rate || 'Unavailable'}</span>
            </div>
            <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-100">
              <span className="text-xs text-slate-500 block">Temperature</span>
              <span className="font-bold text-slate-800">{vitals.temperature || 'Unavailable'}</span>
            </div>
            <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-100">
              <span className="text-xs text-slate-500 block">SpO2</span>
              <span className="font-bold text-slate-800">{vitals.oxygen_saturation || 'Unavailable'}</span>
            </div>
            <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-100">
              <span className="text-xs text-slate-500 block">Resp. Rate</span>
              <span className="font-bold text-slate-800">{vitals.respiratory_rate || 'Unavailable'}</span>
            </div>
            <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-100">
              <span className="text-xs text-slate-500 block">Height / Weight</span>
              <span className="font-bold text-slate-800">
                {vitals.height || 'N/A'} / {vitals.weight || 'N/A'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* 3 & 4. Symptoms & Diagnoses */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* 3. Symptoms */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
          <h3 className="text-base font-bold text-slate-900 mb-3 flex items-center space-x-2">
            <CheckCircle className="w-5 h-5 text-blue-600" />
            <span>3. Extracted Symptoms</span>
          </h3>
          {structured.symptoms && structured.symptoms.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {structured.symptoms.map((sym, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1 bg-blue-50 text-blue-700 text-xs font-semibold rounded-lg border border-blue-200"
                >
                  {sym}
                </span>
              ))}
            </div>
          ) : (
            <p className="text-sm text-slate-500 italic">No symptoms documented in source text.</p>
          )}
        </div>

        {/* 4. Diagnoses */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
          <h3 className="text-base font-bold text-slate-900 mb-3 flex items-center space-x-2">
            <FileText className="w-5 h-5 text-purple-600" />
            <span>4. Explicit Diagnoses</span>
          </h3>
          {structured.diagnoses && structured.diagnoses.length > 0 ? (
            <ul className="space-y-1.5 text-sm">
              {structured.diagnoses.map((dx, idx) => (
                <li key={idx} className="flex items-center space-x-2 text-slate-800 font-medium">
                  <span className="w-1.5 h-1.5 rounded-full bg-purple-600" />
                  <span>{dx}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-slate-500 italic">No explicit diagnoses documented in note.</p>
          )}
        </div>
      </div>

      {/* 5. Medications Table */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
        <h3 className="text-base font-bold text-slate-900 mb-4 flex items-center space-x-2">
          <Pill className="w-5 h-5 text-emerald-600" />
          <span>5. Prescribed & Reported Medications</span>
        </h3>
        {structured.medications && structured.medications.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm border-collapse">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold text-xs">
                  <th className="py-2.5 px-4">Medication Name</th>
                  <th className="py-2.5 px-4">Dosage</th>
                  <th className="py-2.5 px-4">Frequency</th>
                  <th className="py-2.5 px-4">Route</th>
                  <th className="py-2.5 px-4">Notes</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {structured.medications.map((med, idx) => (
                  <tr key={idx} className="hover:bg-slate-50/80">
                    <td className="py-3 px-4 font-semibold text-slate-900">{med.name}</td>
                    <td className="py-3 px-4 text-slate-700">{med.dosage || 'Not specified'}</td>
                    <td className="py-3 px-4 text-slate-700">{med.frequency || 'Not specified'}</td>
                    <td className="py-3 px-4 text-slate-700">{med.route || 'Not specified'}</td>
                    <td className="py-3 px-4 text-xs text-slate-500">{med.notes || '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-sm text-slate-500 italic">No active medications documented.</p>
        )}
      </div>

      {/* 7. Allergies */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
        <h3 className="text-base font-bold text-slate-900 mb-3 flex items-center space-x-2">
          <ShieldAlert className="w-5 h-5 text-rose-600" />
          <span>7. Allergy History</span>
        </h3>
        {structured.allergies && structured.allergies.length > 0 ? (
          <div className="flex flex-wrap gap-2">
            {structured.allergies.map((alg, idx) => (
              <span
                key={idx}
                className="px-3 py-1 bg-rose-50 text-rose-800 border border-rose-200 text-xs font-semibold rounded-lg"
              >
                {alg}
              </span>
            ))}
          </div>
        ) : (
          <p className="text-sm text-slate-500 italic">Allergy status is not documented in source text.</p>
        )}
      </div>

      {/* Clinical Review Flags (Sections 9, 10, 11, 12) */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* 9. Clinical Concerns */}
        <div className="bg-amber-50/50 rounded-2xl p-6 border border-amber-200 shadow-xs">
          <h3 className="text-base font-bold text-amber-900 mb-3 flex items-center space-x-2">
            <AlertTriangle className="w-5 h-5 text-amber-600" />
            <span>9. Identified Clinical Concerns</span>
          </h3>
          {structured.clinical_concerns && structured.clinical_concerns.length > 0 ? (
            <ul className="space-y-2 text-sm">
              {structured.clinical_concerns.map((concern, idx) => (
                <li key={idx} className="flex items-start space-x-2 text-amber-900">
                  <span className="font-bold text-amber-600">•</span>
                  <span>{concern}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-amber-700 italic">No acute clinical concerns flagged.</p>
          )}
        </div>

        {/* 10. Missing Information */}
        <div className="bg-slate-50 rounded-2xl p-6 border border-slate-200 shadow-xs">
          <h3 className="text-base font-bold text-slate-900 mb-3 flex items-center space-x-2">
            <HelpCircle className="w-5 h-5 text-slate-600" />
            <span>10. Missing Information</span>
          </h3>
          {structured.missing_information && structured.missing_information.length > 0 ? (
            <ul className="space-y-2 text-sm">
              {structured.missing_information.map((item, idx) => (
                <li key={idx} className="flex items-start space-x-2 text-slate-700">
                  <span className="font-bold text-slate-400">•</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-slate-500 italic">No critical missing information detected.</p>
          )}
        </div>

        {/* 11. Potential Inconsistencies */}
        <div className="bg-rose-50/60 rounded-2xl p-6 border border-rose-200 shadow-xs">
          <h3 className="text-base font-bold text-rose-950 mb-3 flex items-center space-x-2">
            <AlertTriangle className="w-5 h-5 text-rose-600" />
            <span>11. Potential Inconsistencies</span>
          </h3>
          {structured.potential_inconsistencies && structured.potential_inconsistencies.length > 0 ? (
            <ul className="space-y-2 text-sm">
              {structured.potential_inconsistencies.map((inc, idx) => (
                <li key={idx} className="flex items-start space-x-2 text-rose-900 font-medium">
                  <span className="font-bold text-rose-600">•</span>
                  <span>{inc}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-rose-700 italic">No contradictory information found in document.</p>
          )}
        </div>

        {/* 12. Requires Review */}
        <div className="bg-blue-50/60 rounded-2xl p-6 border border-blue-200 shadow-xs">
          <h3 className="text-base font-bold text-blue-950 mb-3 flex items-center space-x-2">
            <Info className="w-5 h-5 text-blue-600" />
            <span>12. Requires Qualified Human Review</span>
          </h3>
          {structured.requires_review && structured.requires_review.length > 0 ? (
            <ul className="space-y-2 text-sm">
              {structured.requires_review.map((req, idx) => (
                <li key={idx} className="flex items-start space-x-2 text-blue-900 font-medium">
                  <span className="font-bold text-blue-600">•</span>
                  <span>{req}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-blue-700 italic">Standard review complete.</p>
          )}
        </div>
      </div>
    </div>
  );
};
