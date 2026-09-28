# ClinReview AI – Technical Decisions & Architectural Trade-Offs

This document outlines key technical choices, library selections, architectural trade-offs, security designs, and future expansion pathways for **ClinReview AI**.

---

## 1. Technical Stack Selection Rationale

### Frontend: React 18 + TypeScript + Vite + Tailwind CSS
- **React 18 & TypeScript:** Provides explicit typing for structured clinical reports, ensuring components safely handle optional or missing fields without runtime NPE errors.
- **Vite:** Offers sub-second HMR and optimized production bundling (`dist/` built in 8.5 seconds).
- **Tailwind CSS & Lucide Icons:** Enables rapid creation of a clean, modern healthcare dashboard with soft blue palette, rounded cards, subtle gradients, and accessible visual hierarchy.

### Backend: Python 3.14 + FastAPI + SQLAlchemy + Pydantic
- **FastAPI:** High-performance asynchronous REST API framework with native OpenAPI schema generation and Pydantic validation integration.
- **SQLAlchemy ORM:** Provides flexible SQLite storage for simple zero-config local development and seamless PostgreSQL migration support for cloud deployment.
- **Pydantic v2:** Guarantees strict type safety and field validation for both REST requests and complex AI JSON responses.

### Document Processing: PyMuPDF + OpenCV + Tesseract
- **PyMuPDF (`fitz`):** Significantly faster text extraction from native PDFs compared to legacy tools, with direct support for page-to-image rendering.
- **OpenCV & Tesseract:** Contrast normalization and noise removal prior to OCR dramatically improves character recognition accuracy on low-contrast scanned medical documents.

### Report Export: ReportLab
- Enables dynamic, server-side generation of high-resolution PDF clinical reports formatted with custom medical headers, color-coded status badges, structured tables, and disclaimers.

---

## 2. Key Architectural Decisions & Trade-Offs

1. **Separation of Concerns:**
   - The React frontend is completely decoupled from AI extraction and document processing logic. All analysis logic runs securely in the FastAPI backend.
2. **Dual-Mode AI Extraction Engine (API + Heuristic Fallback):**
   - *Decision:* Build an intelligent local heuristic extractor alongside external LLM API client support.
   - *Trade-off:* Allows the application to run out-of-the-box without requiring an external API key or internet connection for local demonstration and automated testing.
3. **In-Memory Buffer Temporary File Handling:**
   - *Decision:* Process uploaded PDF and image files directly from memory buffers rather than saving them to permanent static web directories.
   - *Trade-off:* Maximizes patient data security and avoids storage accumulation, while requiring file size limits (10 MB).

---

## 3. Security & Compliance Considerations

- **Secrets Management:** Secrets and API keys are strictly loaded via `.env` environment variables using `pydantic-settings`.
- **CORS Configuration:** Strictly scopes allowed origins (`http://localhost:5173`) to prevent unauthorized cross-origin API abuse.
- **Synthetic Data Guarantee:** All demonstration dataset cases use synthetic patient identifiers (`SYN-1001` through `SYN-1004`) to prevent real PHI exposure.

---

## 4. Future Improvements

1. **PostgreSQL / Vector Store Integration:** Add pgvector or embedding search for semantic querying across thousands of past clinical reports.
2. **DICOM & HL7 / FHIR Support:** Extend input ingestion pipeline to process standard healthcare formats (FHIR JSON resources, DICOM imaging headers).
3. **Multi-User Authentication:** Implement JWT-based RBAC for clinician and administrator user roles.
