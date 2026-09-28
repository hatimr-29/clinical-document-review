from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from typing import Optional, List
import math

from app.database import get_db
from app.models.report import ClinicalReport
from app.schemas.report import (
    ReportResponse,
    ReportSummaryItem,
    ReportStatusResponse,
    PaginatedReportsResponse,
    DashboardStatsResponse
)
from app.services.pdf_generator import generate_report_pdf

router = APIRouter()

@router.get("/reports/dashboard", response_model=DashboardStatsResponse)
def get_dashboard_stats(db: Session = Depends(get_db)):
    total = db.query(ClinicalReport).count()
    completed = db.query(ClinicalReport).filter(ClinicalReport.processing_status == "Completed").count()
    failed = db.query(ClinicalReport).filter(ClinicalReport.processing_status == "Failed").count()
    
    recent = (
        db.query(ClinicalReport)
        .order_by(desc(ClinicalReport.created_at))
        .limit(5)
        .all()
    )
    
    recent_items = [ReportSummaryItem.model_validate(r) for r in recent]
    
    return DashboardStatsResponse(
        total_documents=total,
        completed_analyses=completed,
        failed_analyses=failed,
        recent_reports=recent_items
    )

@router.get("/reports", response_model=PaginatedReportsResponse)
def get_all_reports(
    search: Optional[str] = Query(None, description="Search term for report name or ID"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(ClinicalReport)

    if status_filter and status_filter.strip() and status_filter.lower() != "all":
        query = query.filter(ClinicalReport.processing_status == status_filter.strip().capitalize())

    if search and search.strip():
        term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                ClinicalReport.id.ilike(term),
                ClinicalReport.document_name.ilike(term),
                ClinicalReport.report_summary.ilike(term)
            )
        )

    total = query.count()
    pages = max(1, math.ceil(total / limit))
    offset = (page - 1) * limit

    reports = (
        query.order_by(desc(ClinicalReport.created_at))
        .offset(offset)
        .limit(limit)
        .all()
    )

    items = [ReportSummaryItem.model_validate(r) for r in reports]

    return PaginatedReportsResponse(
        success=True,
        message="Reports retrieved successfully",
        reports=items,
        total=total,
        page=page,
        limit=limit,
        pages=pages
    )

@router.get("/reports/{report_id}/status", response_model=ReportStatusResponse)
def get_report_status(report_id: str, db: Session = Depends(get_db)):
    report = db.query(ClinicalReport).filter(ClinicalReport.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "message": f"Report '{report_id}' not found.", "error_code": "REPORT_NOT_FOUND"}
        )
    return ReportStatusResponse(
        id=report.id,
        processing_status=report.processing_status,
        processing_error=report.processing_error,
        created_at=report.created_at,
        completed_at=report.completed_at
    )

@router.get("/reports/{report_id}")
def get_report_details(report_id: str, db: Session = Depends(get_db)):
    report = db.query(ClinicalReport).filter(ClinicalReport.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "message": f"Report '{report_id}' not found.", "error_code": "REPORT_NOT_FOUND"}
        )
    return {
        "success": True,
        "message": "Report details retrieved successfully",
        "data": ReportResponse.model_validate(report)
    }

@router.delete("/reports/{report_id}")
def delete_report(report_id: str, db: Session = Depends(get_db)):
    report = db.query(ClinicalReport).filter(ClinicalReport.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "message": f"Report '{report_id}' not found.", "error_code": "REPORT_NOT_FOUND"}
        )
    db.delete(report)
    db.commit()
    return {
        "success": True,
        "message": f"Report '{report_id}' deleted successfully."
    }

@router.get("/reports/{report_id}/download")
def download_report_pdf(report_id: str, db: Session = Depends(get_db)):
    report = db.query(ClinicalReport).filter(ClinicalReport.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "message": f"Report '{report_id}' not found.", "error_code": "REPORT_NOT_FOUND"}
        )
    
    pdf_bytes = generate_report_pdf(report)
    filename = f"ClinReview_Report_{report.id}.pdf"
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
