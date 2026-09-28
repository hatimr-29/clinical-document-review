from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.utils.validation import DocumentValidationError
import logging

logger = logging.getLogger("clinreview")

async def document_validation_exception_handler(request: Request, exc: DocumentValidationError):
    logger.warning(f"Document validation error: {exc.message} ({exc.error_code})")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "message": exc.message,
            "error_code": exc.error_code
        }
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled server error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "An internal server error occurred during clinical document processing.",
            "error_code": "INTERNAL_SERVER_ERROR"
        }
    )
