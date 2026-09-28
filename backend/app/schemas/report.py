from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime

class PatientInfoSchema(BaseModel):
    patient_id: Optional[str] = None
    age: Optional[Any] = None
    sex: Optional[str] = None
    demographics: Optional[str] = None

class MedicationSchema(BaseModel):
    name: str
    dosage: Optional[str] = "Not specified"
    frequency: Optional[str] = "Not specified"
    route: Optional[str] = "Not specified"
    notes: Optional[str] = None

class VitalSignsSchema(BaseModel):
    blood_pressure: Optional[str] = None
    heart_rate: Optional[str] = None
    temperature: Optional[str] = None
    respiratory_rate: Optional[str] = None
    oxygen_saturation: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[str] = None

class StructuredReportSchema(BaseModel):
    report_summary: str = ""
    patient_information: PatientInfoSchema = Field(default_factory=PatientInfoSchema)
    symptoms: List[str] = Field(default_factory=list)
    diagnoses: List[str] = Field(default_factory=list)
    medications: List[MedicationSchema] = Field(default_factory=list)
    vital_signs: VitalSignsSchema = Field(default_factory=VitalSignsSchema)
    allergies: List[str] = Field(default_factory=list)
    clinical_observations: List[str] = Field(default_factory=list)
    clinical_concerns: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    potential_inconsistencies: List[str] = Field(default_factory=list)
    requires_review: List[str] = Field(default_factory=list)
    extraction_warnings: List[str] = Field(default_factory=list)
    processing_metadata: Dict[str, Any] = Field(default_factory=dict)

# API Request/Response Schemas
class AnalyzeTextRequest(BaseModel):
    text: str
    document_name: Optional[str] = "Clinical Note.txt"

class ReportResponse(BaseModel):
    id: str
    document_name: str
    input_type: str
    original_text: Optional[str] = None
    extracted_text: str
    report_summary: Optional[str] = None
    structured_report: Optional[StructuredReportSchema] = None
    processing_status: str
    processing_error: Optional[str] = None
    extraction_method: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ReportSummaryItem(BaseModel):
    id: str
    document_name: str
    input_type: str
    report_summary: Optional[str] = None
    processing_status: str
    extraction_method: str
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ReportStatusResponse(BaseModel):
    id: str
    processing_status: str
    processing_error: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    error_code: Optional[str] = None

class PaginatedReportsResponse(BaseModel):
    success: bool = True
    message: str = "Reports fetched successfully"
    reports: List[ReportSummaryItem]
    total: int
    page: int
    limit: int
    pages: int

class DashboardStatsResponse(BaseModel):
    total_documents: int
    completed_analyses: int
    failed_analyses: int
    recent_reports: List[ReportSummaryItem]
