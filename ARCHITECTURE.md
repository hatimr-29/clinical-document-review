# ClinReview AI – System Architecture Documentation

This document describes the high-level system architecture, data processing flow, document extraction pipeline, AI extraction service, and database persistence layers of **ClinReview AI**.

---

## 1. System Architecture Diagram

```mermaid
flowchart TD
    subgraph Client ["Frontend (React + TypeScript + Vite)"]
        User["User / Clinical Reviewer"]
        UI["React Dashboard / New Review"]
        FormVal["Zod & React Hook Form Validation"]
        AxiosClient["Axios REST API Client"]
    end

    subgraph Backend ["Backend (FastAPI + Uvicorn)"]
        API["FastAPI API Router (/api/*)"]
        DocProc["Document Processing Service"]
        
        subgraph Extractors ["Document Extractors"]
            PyMuPDF["PyMuPDF (PDF Text Extraction)"]
            OCR["OpenCV + Tesseract OCR (Image & Scanned PDF)"]
            TextNorm["Whitespace Normalizer"]
        end
        
        subgraph AIService ["AI Clinical Service"]
            PromptEng["Prompt Engine & LLM Client"]
            MockEngine["Intelligent Mock Analyzer (Fallback)"]
            PydanticVal["Pydantic Structured JSON Validation"]
            RepairLoop["JSON Malformed Repair Loop"]
        end
        
        subgraph Persistence ["Persistence & Reports"]
            SQLAlchemy["SQLAlchemy ORM"]
            DB[(SQLite / PostgreSQL Database)]
            PDFGen["ReportLab PDF Generator"]
        end
    end

    subgraph External ["External Services"]
        LLMProvider["LLM API Provider (OpenAI / Gemini / Custom REST)"]
    end

    User --> UI
    UI --> FormVal
    FormVal --> AxiosClient
    AxiosClient -->|"HTTP POST /api/analyze/*"| API
    
    API --> DocProc
    DocProc --> PyMuPDF
    DocProc --> OCR
    DocProc --> TextNorm
    
    DocProc --> AIService
    PromptEng -->|"HTTP API Call (If API Key Configured)"| LLMProvider
    PromptEng -->|"If No Key / Provider Mock"| MockEngine
    
    AIService --> PydanticVal
    PydanticVal -->|"On Schema Error"| RepairLoop
    RepairLoop --> PydanticVal
    
    PydanticVal --> SQLAlchemy
    SQLAlchemy --> DB
    
    API -->|"GET /api/reports/{id}/download"| PDFGen
    PDFGen -->|"Returns Binary PDF"| AxiosClient
    SQLAlchemy -->|"Returns JSON Structured Data"| API
    API --> UI
```

---

## 2. Document Processing Pipeline Sequence

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Frontend as React Frontend
    participant API as FastAPI Backend
    participant DocProc as Document Processor
    participant AI as AI Clinical Analyzer
    participant DB as Database (SQLAlchemy)

    User->>Frontend: Select file (PDF/PNG/JPG) or enter plain text
    Frontend->>Frontend: Perform client-side file size & extension validation
    Frontend->>API: POST /api/analyze/file (Multipart) or /text
    API->>DocProc: Validate input & detect document format
    
    alt PDF Document
        DocProc->>DocProc: PyMuPDF text extraction (detect if scanned)
    else Image Document
        DocProc->>DocProc: OpenCV image preprocessing + Tesseract OCR
    else Plain Text
        DocProc->>DocProc: Whitespace normalization
    end

    DocProc font-->>API: Return cleaned text + extraction metadata
    API->>DB: Create initial report record (Status: "Processing")
    
    API->>AI: Send normalized text for clinical analysis
    alt LLM API Configured
        AI->>AI: Call external LLM (Structured JSON Mode)
    else Mock / Fallback Engine
        AI->>AI: Execute deterministic clinical regex pattern extraction
    end
    
    AI->>AI: Validate output against Pydantic StructuredReportSchema
    AI-->>API: Return validated structured report + summary
    
    API->>DB: Update report record (Status: "Completed", JSON report)
    API-->>Frontend: Return 200 OK + Report JSON payload
    Frontend->>User: Render 12 structured report sections & enable PDF download
```

---

## 3. Data Flow & Security Layer

- **Safe Temporary Memory Processing:** Files uploaded via multipart endpoints are read directly into memory buffers without exposing permanent static server file URLs.
- **Environment Key Isolation:** `AI_API_KEY` and database credentials remain strictly in backend environment variables and are never exposed to the client bundle.
- **Fail-Safe Processing States:** If document processing or AI JSON validation encounters unrecoverable errors, the database record status is updated to `"Failed"` with error details, preventing corrupted records from appearing as successfully completed.
