import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.report import ClinicalReport
from app.services.document_processor import ProcessedDocument
from app.services.clinical_analyzer import analyze_clinical_document

logger = logging.getLogger("clinreview.report_gen")

async def create_and_process_report(
    db: Session,
    document: ProcessedDocument,
    document_name: str
) -> ClinicalReport:
    """
    Creates initial DB record in 'Processing' status, performs AI analysis,
    updates DB record with structured result or error, and marks 'Completed' or 'Failed'.
    """
    report = ClinicalReport(
        document_name=document_name,
        input_type=document.input_type,
        original_text=document.extracted_text,
        extracted_text=document.extracted_text,
        processing_status="Processing",
        extraction_method=document.extraction_method,
        created_at=datetime.now(timezone.utc)
    )
    
    db.add(report)
    db.commit()
    db.refresh(report)

    try:
        structured_report, summary = await analyze_clinical_document(
            extracted_text=document.extracted_text,
            input_type=document.input_type,
            extraction_method=document.extraction_method,
            warnings=document.warnings
        )

        report.report_summary = summary
        report.structured_report = structured_report.model_dump()
        report.processing_status = "Completed"
        report.completed_at = datetime.now(timezone.utc)
        report.processing_error = None
        
        db.commit()
        db.refresh(report)
        logger.info(f"Successfully processed report {report.id}")
        return report

    except Exception as e:
        logger.error(f"Failed to process report {report.id}: {e}")
        report.processing_status = "Failed"
        report.processing_error = str(e)
        report.completed_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(report)
        return report
