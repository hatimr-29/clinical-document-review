import fitz  # PyMuPDF
import io
import logging
from typing import Tuple, List

logger = logging.getLogger("clinreview.pdf")

def extract_text_from_pdf(pdf_bytes: bytes) -> Tuple[str, str, bool, List[str]]:
    """
    Extract text from PDF using PyMuPDF.
    Returns: (extracted_text, method_used, is_scanned_or_ocr, warnings)
    """
    warnings = []
    text_chunks = []
    
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as e:
        logger.error(f"Failed to open PDF document: {e}")
        raise ValueError("The uploaded PDF file is corrupted or password-protected.")
        
    page_count = len(doc)
    if page_count == 0:
        raise ValueError("The uploaded PDF document contains no pages.")

    total_text_length = 0
    for i in range(page_count):
        page = doc[i]
        page_text = page.get_text("text")
        if page_text:
            text_chunks.append(page_text.strip())
            total_text_length += len(page_text.strip())

    combined_text = "\n\n".join(text_chunks)
    
    # Check if PDF appears scanned (very little text relative to page count)
    is_scanned = total_text_length < (page_count * 20)
    
    if is_scanned:
        warnings.append("PDF appears to contain scanned or image-based pages. OCR was attempted on page images.")
        # Render pages to image and extract text via OCR if needed
        from app.services.image_ocr import extract_text_from_image_bytes
        ocr_texts = []
        for i in range(page_count):
            page = doc[i]
            pix = page.get_pixmap(dpi=150)
            img_bytes = pix.tobytes("png")
            ocr_text, ocr_method, ocr_warn = extract_text_from_image_bytes(img_bytes)
            if ocr_text:
                ocr_texts.append(ocr_text)
                warnings.extend(ocr_warn)
        
        if ocr_texts:
            combined_ocr = "\n\n".join(ocr_texts)
            if len(combined_ocr) > len(combined_text):
                return combined_ocr, "pymupdf_ocr_render", True, list(set(warnings))

    doc.close()
    
    if not combined_text and not is_scanned:
        raise ValueError("Could not extract readable text from the uploaded PDF document.")

    return combined_text, "pymupdf_direct", is_scanned, warnings
