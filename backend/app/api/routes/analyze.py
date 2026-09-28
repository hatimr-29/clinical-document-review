from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schemas.report import AnalyzeTextRequest, ReportResponse
from app.services.document_processor import process_plain_text, process_uploaded_file
from app.services.report_generator import create_and_process_report
from app.utils.validation import DocumentValidationError

router = APIRouter()

@router.post("/analyze/text")
async def analyze_text(request: AnalyzeTextRequest, db: Session = Depends(get_db)):
    try:
        doc = process_plain_text(request.text)
        report = await create_and_process_report(
            db=db,
            document=doc,
            document_name=request.document_name or "Clinical Note.txt"
        )
        return {
            "success": True,
            "message": "Clinical report generated successfully",
            "data": ReportResponse.model_validate(report)
        }
    except DocumentValidationError as ve:
        raise ve
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"success": False, "message": str(e), "error_code": "TEXT_ANALYSIS_FAILED"}
        )

@router.post("/analyze/file")
async def analyze_file(
    file: UploadFile = File(...),
    document_name: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    try:
        filename = document_name or file.filename or "Uploaded_Document"
        content_type = file.content_type or ""
        file_bytes = await file.read()
        
        if not file_bytes:
            raise DocumentValidationError("Uploaded file is empty.", "EMPTY_FILE")

        doc = process_uploaded_file(filename=filename, content_type=content_type, file_bytes=file_bytes)
        
        report = await create_and_process_report(
            db=db,
            document=doc,
            document_name=filename
        )
        
        return {
            "success": True,
            "message": "Document uploaded and analyzed successfully",
            "data": ReportResponse.model_validate(report)
        }
    except DocumentValidationError as ve:
        raise ve
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"success": False, "message": str(e), "error_code": "FILE_PROCESSING_FAILED"}
        )
