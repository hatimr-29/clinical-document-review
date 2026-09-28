import re
import logging
from typing import Dict, Any, Tuple, List
from app.services.pdf_extractor import extract_text_from_pdf
from app.services.image_ocr import extract_text_from_image_bytes
from app.utils.validation import validate_text_input, validate_file_upload

logger = logging.getLogger("clinreview.processor")

class ProcessedDocument:
    def __init__(
        self,
        extracted_text: str,
        input_type: str,
        extraction_method: str,
        was_ocr_used: bool = False,
        warnings: List[str] = None,
        metadata: Dict[str, Any] = None
    ):
        self.extracted_text = extracted_text
        self.input_type = input_type
        self.extraction_method = extraction_method
        self.was_ocr_used = was_ocr_used
        self.warnings = warnings or []
        self.metadata = metadata or {}

def normalize_text(text: str) -> str:
    """Normalize whitespace and clean up raw extracted clinical text."""
    if not text:
        return ""
    # Replace multiple empty lines with maximum 2 newlines
    text = re.sub(r'\r\n|\r', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Replace weird space characters
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def process_plain_text(raw_text: str) -> ProcessedDocument:
    cleaned = validate_text_input(raw_text)
    normalized = normalize_text(cleaned)
    return ProcessedDocument(
        extracted_text=normalized,
        input_type="text",
        extraction_method="direct_text",
        was_ocr_used=False,
        warnings=[],
        metadata={"character_count": len(normalized)}
    )

def process_uploaded_file(filename: str, content_type: str, file_bytes: bytes) -> ProcessedDocument:
    validate_file_upload(filename, content_type, len(file_bytes))
    
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    
    if ext == 'pdf' or content_type == 'application/pdf':
        text, method, is_scanned, warnings = extract_text_from_pdf(file_bytes)
        normalized = normalize_text(text)
        if not normalized or len(normalized) < 10:
            raise ValueError("Extracted PDF content is empty or unreadable.")
        return ProcessedDocument(
            extracted_text=normalized,
            input_type="pdf",
            extraction_method=method,
            was_ocr_used=is_scanned,
            warnings=warnings,
            metadata={"filename": filename, "file_size": len(file_bytes)}
        )
        
    elif ext in ['png', 'jpg', 'jpeg'] or content_type.startswith('image/'):
        text, method, warnings = extract_text_from_image_bytes(file_bytes)
        normalized = normalize_text(text)
        if not normalized or len(normalized) < 10:
            raise ValueError("OCR engine could not extract readable text from the image.")
        return ProcessedDocument(
            extracted_text=normalized,
            input_type="image",
            extraction_method=method,
            was_ocr_used=True,
            warnings=warnings,
            metadata={"filename": filename, "file_size": len(file_bytes)}
        )
    else:
        raise ValueError(f"Unsupported file format: {ext}")
