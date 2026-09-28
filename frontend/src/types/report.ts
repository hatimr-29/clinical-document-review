export interface PatientInfo {
  patient_id?: string | null;
  age?: number | string | null;
  sex?: string | null;
  demographics?: string | null;
}

export interface Medication {
  name: string;
  dosage?: string | null;
  frequency?: string | null;
  route?: string | null;
  notes?: string | null;
}

export interface VitalSigns {
  blood_pressure?: string | null;
  heart_rate?: string | null;
  temperature?: string | null;
  respiratory_rate?: string | null;
  oxygen_saturation?: string | null;
  height?: string | null;
  weight?: string | null;
}

export interface StructuredReport {
  report_summary: string;
  patient_information: PatientInfo;
  symptoms: string[];
  diagnoses: string[];
  medications: Medication[];
  vital_signs: VitalSigns;
  allergies: string[];
  clinical_observations: string[];
  clinical_concerns: string[];
  missing_information: string[];
  potential_inconsistencies: string[];
  requires_review: string[];
  extraction_warnings: string[];
  processing_metadata: Record<string, any>;
}

export interface ClinicalReport {
  id: string;
  document_name: string;
  input_type: 'text' | 'pdf' | 'image';
  original_text?: string | null;
  extracted_text: string;
  report_summary?: string | null;
  structured_report?: StructuredReport | null;
  processing_status: 'Pending' | 'Processing' | 'Completed' | 'Failed';
  processing_error?: string | null;
  extraction_method: string;
  created_at: string;
  updated_at: string;
  completed_at?: string | null;
}

export interface ReportSummaryItem {
  id: string;
  document_name: string;
  input_type: 'text' | 'pdf' | 'image';
  report_summary?: string | null;
  processing_status: 'Pending' | 'Processing' | 'Completed' | 'Failed';
  extraction_method: string;
  created_at: string;
  completed_at?: string | null;
}

export interface DashboardStats {
  total_documents: number;
  completed_analyses: number;
  failed_analyses: number;
  recent_reports: ReportSummaryItem[];
}

export interface PaginatedReports {
  success: boolean;
  message: string;
  reports: ReportSummaryItem[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}
