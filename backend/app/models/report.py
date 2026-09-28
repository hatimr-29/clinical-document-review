import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, JSON, DateTime
from app.database import Base

def generate_report_id():
    return f"CR-{uuid.uuid4().hex[:8].upper()}"

class ClinicalReport(Base):
    __tablename__ = "clinical_reports"

    id = Column(String, primary_key=True, default=generate_report_id)
    document_name = Column(String, nullable=False, default="Untitled Document")
    input_type = Column(String, nullable=False)  # text, pdf, image
    original_text = Column(Text, nullable=True)
    extracted_text = Column(Text, nullable=False)
    report_summary = Column(Text, nullable=True)
    structured_report = Column(JSON, nullable=True)
    processing_status = Column(String, nullable=False, default="Pending")  # Pending, Processing, Completed, Failed
    processing_error = Column(Text, nullable=True)
    extraction_method = Column(String, nullable=False, default="direct")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)
