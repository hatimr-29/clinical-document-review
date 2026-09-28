from app.config import settings

class DocumentValidationError(Exception):
    def __init__(self, message: str, error_code: str = "INVALID_DOCUMENT"):
        self.message = message
        self.error_code = error_code
        super().__init__(message)

def validate_text_input(text: str) -> str:
    if not text or not text.strip():
        raise DocumentValidationError("Clinical text content cannot be empty", "EMPTY_TEXT")
    
    cleaned_text = text.strip()
    if len(cleaned_text) < 10:
        raise DocumentValidationError("Clinical text is too short to perform a meaningful review", "TEXT_TOO_SHORT")
        
    return cleaned_text

def validate_file_upload(filename: str, content_type: str, file_size: int):
    allowed_types = settings.ALLOWED_IMAGE_TYPES + settings.ALLOWED_PDF_TYPES
    if content_type not in allowed_types:
        # Check file extension fallback
        ext = filename.lower().split('.')[-1] if '.' in filename else ''
        if ext not in ['pdf', 'png', 'jpg', 'jpeg']:
            raise DocumentValidationError(
                f"Unsupported file format '{ext}'. Allowed formats: PDF, PNG, JPG, JPEG.",
                "UNSUPPORTED_FILE_TYPE"
            )
    
    max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if file_size > max_bytes:
        raise DocumentValidationError(
            f"File size ({file_size / (1024*1024):.1f} MB) exceeds maximum allowed limit of {settings.MAX_FILE_SIZE_MB} MB.",
            "FILE_TOO_LARGE"
        )
