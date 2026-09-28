import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { analyzeText, analyzeFile } from '../services/api';
import { formatFileSize } from '../utils/helpers';
import {
  FileText,
  Upload,
  X,
  FileCheck,
  AlertCircle,
  Loader2,
  Sparkles,
  Trash2,
  Send,
  FileCode
} from 'lucide-react';

const SYNTHETIC_PRESETS = [
  {
    title: 'Complete Clinical Note',
    description: 'Standard outpatient consult note with complete vitals and meds',
    text: `Patient ID: SYN-1001
Age: 45
Sex: Female

Chief Complaint:
Patient reports headache and fatigue for three days.

Symptoms:
- Headache
- Fatigue

Vitals:
- Blood pressure: 128/82 mmHg
- Heart rate: 84 bpm
- Temperature: 37.1 °C
- Oxygen saturation: 98%

Medication:
- Paracetamol 500 mg oral as documented in note.

Allergies:
Not documented.

Clinical observation:
Patient reports persistent headache worsening in late afternoon.`
  },
  {
    title: 'Note with Missing Details',
    description: 'Incomplete record with missing medication frequency & vital signs',
    text: `Patient ID: SYN-1002
Age: 62 | Sex: Male

Progress Note:
Patient admitted with acute shortness of breath. Prescribed Lisinopril and Metformin. BP recorded as 148/92 mmHg.
No allergy status listed on transfer sheet. Past surgical history unverified.`
  },
  {
    title: 'Conflicting Observations',
    description: 'Contradiction between subjective fever and objective afebrile temperature',
    text: `Patient ID: SYN-1003
Age: 38 | Sex: Female

Subjective:
Patient complains of severe high fever and body aches since yesterday morning.

Objective Vitals:
Temperature: 36.6 °C (Axillary)
Heart Rate: 72 bpm
Blood Pressure: 116/74 mmHg
SpO2: 99%

Allergies: Penicillin (causes severe anaphylactic hives)
Current Meds: Amoxicillin 500mg TID prescribed by urgent care center.`
  }
];

export const NewReview: React.FC = () => {
  const [mode, setMode] = useState<'text' | 'file'>('text');
  const [textInput, setTextInput] = useState('');
  const [documentName, setDocumentName] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isDragOver, setIsDragOver] = useState(false);
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const navigate = useNavigate();

  const handleFileChange = (file: File) => {
    setError(null);
    const validExtensions = ['pdf', 'png', 'jpg', 'jpeg'];
    const ext = file.name.split('.').pop()?.toLowerCase() || '';
    
    if (!validExtensions.includes(ext)) {
      setError(`Unsupported file type '.${ext}'. Please upload a PDF, PNG, JPG, or JPEG file.`);
      return;
    }

    const maxBytes = 10 * 1024 * 1024; // 10MB
    if (file.size > maxBytes) {
      setError(`File size (${formatFileSize(file.size)}) exceeds maximum limit of 10 MB.`);
      return;
    }

    setSelectedFile(file);
    if (!documentName) {
      setDocumentName(file.name);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const handleSubmitText = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!textInput.trim()) {
      setError('Please enter or paste clinical notes before submitting.');
      return;
    }

    if (textInput.trim().length < 10) {
      setError('Clinical notes must be at least 10 characters long.');
      return;
    }

    try {
      setLoading(true);
      const report = await analyzeText(textInput, documentName || 'Clinical Note.txt');
      navigate(`/reports/${report.id}`);
    } catch (err: any) {
      console.error('Text analysis error:', err);
      const message = err.response?.data?.message || err.message || 'Failed to process clinical text.';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitFile = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!selectedFile) {
      setError('Please select a document file (PDF or Image) to upload.');
      return;
    }

    try {
      setLoading(true);
      const report = await analyzeFile(selectedFile, documentName || selectedFile.name);
      navigate(`/reports/${report.id}`);
    } catch (err: any) {
      console.error('File upload error:', err);
      const message = err.response?.data?.message || err.message || 'Failed to analyze uploaded document.';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 space-y-8">
      {/* Header Title */}
      <div>
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">Submit Clinical Document</h1>
        <p className="text-slate-600 text-sm mt-1">
          Select input method to extract clinical entities, vital signs, allergies, and safety risks.
        </p>
      </div>

      {/* Input Mode Selector Tabs */}
      <div className="bg-slate-200/60 p-1.5 rounded-2xl flex max-w-md">
        <button
          type="button"
          onClick={() => {
            setMode('text');
            setError(null);
          }}
          className={`flex-1 flex items-center justify-center space-x-2 py-2.5 rounded-xl text-sm font-bold transition-all ${
            mode === 'text'
              ? 'bg-white text-blue-900 shadow-xs'
              : 'text-slate-600 hover:text-slate-900'
          }`}
        >
          <FileText className="w-4 h-4" />
          <span>Enter Clinical Notes</span>
        </button>

        <button
          type="button"
          onClick={() => {
            setMode('file');
            setError(null);
          }}
          className={`flex-1 flex items-center justify-center space-x-2 py-2.5 rounded-xl text-sm font-bold transition-all ${
            mode === 'file'
              ? 'bg-white text-blue-900 shadow-xs'
              : 'text-slate-600 hover:text-slate-900'
          }`}
        >
          <Upload className="w-4 h-4" />
          <span>Upload Document</span>
        </button>
      </div>

      {/* Error Banner */}
      {error && (
        <div className="bg-rose-50 border border-rose-200 rounded-xl p-4 flex items-start space-x-3 text-rose-900 text-sm">
          <AlertCircle className="w-5 h-5 text-rose-600 flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <span className="font-semibold block">Submission Error</span>
            <span>{error}</span>
          </div>
          <button onClick={() => setError(null)} className="text-rose-500 hover:text-rose-700">
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* MODE 1: ENTER CLINICAL NOTES */}
      {mode === 'text' && (
        <form onSubmit={handleSubmitText} className="space-y-6">
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs space-y-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                Document Name / Title (Optional)
              </label>
              <input
                type="text"
                placeholder="e.g. Outpatient Consult Note - SYN-1001"
                value={documentName}
                onChange={(e) => setDocumentName(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
              />
            </div>

            <div>
              <div className="flex justify-between items-center mb-1">
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
                  Clinical Notes Content
                </label>
                <div className="flex items-center space-x-3 text-xs text-slate-500">
                  <span>{textInput.length} characters</span>
                  {textInput && (
                    <button
                      type="button"
                      onClick={() => setTextInput('')}
                      className="text-rose-600 hover:text-rose-800 flex items-center space-x-1 font-medium"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                      <span>Clear Input</span>
                    </button>
                  )}
                </div>
              </div>
              <textarea
                rows={10}
                placeholder="Type or paste clinical notes here..."
                value={textInput}
                onChange={(e) => setTextInput(e.target.value)}
                className="w-full px-4 py-3 rounded-xl border border-slate-300 text-sm font-sans focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none leading-relaxed"
              />
            </div>
          </div>

          {/* Synthetic Demo Data Preset Selector */}
          <div className="bg-blue-50/50 rounded-2xl p-5 border border-blue-100 space-y-3">
            <div className="flex items-center space-x-2 text-xs font-bold text-blue-900 uppercase tracking-wider">
              <Sparkles className="w-4 h-4 text-blue-600" />
              <span>Load Synthetic Demonstration Notes</span>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {SYNTHETIC_PRESETS.map((preset, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => {
                    setTextInput(preset.text);
                    setDocumentName(preset.title);
                    setError(null);
                  }}
                  className="text-left bg-white p-3.5 rounded-xl border border-blue-200/60 hover:border-blue-500 hover:shadow-xs transition-all group"
                >
                  <span className="font-bold text-xs text-slate-900 group-hover:text-blue-600 block">
                    {preset.title}
                  </span>
                  <span className="text-[11px] text-slate-500 line-clamp-2 mt-0.5">
                    {preset.description}
                  </span>
                </button>
              ))}
            </div>
          </div>

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={loading || !textInput.trim()}
              className="flex items-center space-x-2 px-8 py-3.5 bg-gradient-to-r from-blue-600 to-teal-600 text-white font-bold text-sm rounded-xl hover:from-blue-700 hover:to-teal-700 shadow-md shadow-blue-500/20 disabled:opacity-50 transition-all active:scale-95"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>Processing Clinical AI Pipeline...</span>
                </>
              ) : (
                <>
                  <Send className="w-4 h-4" />
                  <span>Submit for AI Review</span>
                </>
              )}
            </button>
          </div>
        </form>
      )}

      {/* MODE 2: UPLOAD DOCUMENT */}
      {mode === 'file' && (
        <form onSubmit={handleSubmitFile} className="space-y-6">
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs space-y-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                Document Name / Title (Optional)
              </label>
              <input
                type="text"
                placeholder="e.g. Scanned Consult Report.pdf"
                value={documentName}
                onChange={(e) => setDocumentName(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
              />
            </div>

            {/* Drag and Drop Zone */}
            <div
              onDragOver={(e) => {
                e.preventDefault();
                setIsDragOver(true);
              }}
              onDragLeave={() => setIsDragOver(false)}
              onDrop={handleDrop}
              className={`border-2 border-dashed rounded-2xl p-8 text-center transition-all cursor-pointer ${
                isDragOver
                  ? 'border-blue-500 bg-blue-50/50'
                  : selectedFile
                  ? 'border-emerald-300 bg-emerald-50/20'
                  : 'border-slate-300 hover:border-blue-400 bg-slate-50/50'
              }`}
            >
              {selectedFile ? (
                <div className="flex flex-col items-center space-y-3">
                  <div className="p-3 bg-emerald-100 text-emerald-700 rounded-2xl">
                    <FileCheck className="w-8 h-8" />
                  </div>
                  <div>
                    <span className="font-bold text-slate-900 block text-base">{selectedFile.name}</span>
                    <span className="text-xs text-slate-500 mt-0.5 block">
                      Size: {formatFileSize(selectedFile.size)} • Type: {selectedFile.type || 'Document'}
                    </span>
                  </div>
                  <button
                    type="button"
                    onClick={() => {
                      setSelectedFile(null);
                      setDocumentName('');
                    }}
                    className="flex items-center space-x-1 text-xs font-semibold text-rose-600 hover:text-rose-800 bg-rose-50 px-3 py-1.5 rounded-lg border border-rose-200"
                  >
                    <X className="w-3.5 h-3.5" />
                    <span>Remove Selected File</span>
                  </button>
                </div>
              ) : (
                <label className="cursor-pointer flex flex-col items-center space-y-3">
                  <div className="p-4 bg-blue-50 text-blue-600 rounded-2xl border border-blue-100">
                    <Upload className="w-8 h-8" />
                  </div>
                  <div>
                    <span className="text-sm font-bold text-slate-800 block">
                      Drag & Drop medical document here
                    </span>
                    <span className="text-xs text-slate-500 block mt-1">
                      Supported Formats: <strong className="text-slate-700">PDF, PNG, JPG, JPEG</strong> (Max 10 MB)
                    </span>
                  </div>
                  <input
                    type="file"
                    accept=".pdf,.png,.jpg,.jpeg,application/pdf,image/*"
                    onChange={(e) => {
                      if (e.target.files && e.target.files[0]) {
                        handleFileChange(e.target.files[0]);
                      }
                    }}
                    className="hidden"
                  />
                  <span className="inline-block px-4 py-2 bg-white border border-slate-300 rounded-xl text-xs font-semibold text-slate-700 shadow-xs hover:bg-slate-50">
                    Browse Files
                  </span>
                </label>
              )}
            </div>
          </div>

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={loading || !selectedFile}
              className="flex items-center space-x-2 px-8 py-3.5 bg-gradient-to-r from-blue-600 to-teal-600 text-white font-bold text-sm rounded-xl hover:from-blue-700 hover:to-teal-700 shadow-md shadow-blue-500/20 disabled:opacity-50 transition-all active:scale-95"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>Processing File & OCR Pipeline...</span>
                </>
              ) : (
                <>
                  <Send className="w-4 h-4" />
                  <span>Upload & Review Document</span>
                </>
              )}
            </button>
          </div>
        </form>
      )}
    </div>
  );
};
