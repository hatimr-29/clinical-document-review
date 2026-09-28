# ClinReview AI – Intelligent Clinical Document Reviewer

ClinReview AI is a full-stack AI-powered clinical document review web application designed to process typed, scanned, and handwritten clinical documentation across plain text notes, PDF uploads, and medical image files (PNG, JPG, JPEG).

The system extracts clinical entities, analyzes symptoms, diagnoses, prescribed medications, and vital signs, identifies missing clinical information and contradictions, highlights items requiring qualified human review, and persists structured reports in a backend database.

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
---

## Key Features

- **Multi-Format Input Support:**
  - **Plain Text:** Direct note entry with character counter, validation, and sample synthetic presets.
  - **PDF Documents:** PyMuPDF text extraction with scanned PDF page image rendering & OCR fallback.
  - **Medical Images (PNG/JPG/JPEG):** Adaptive image OCR preprocessing with OpenCV contrast enhancement and Tesseract OCR engine.
- **AI-Powered Structured Extraction:**
  - Extracts 12 core clinical report sections (Summary, Patient Info, Symptoms, Diagnoses, Medications, Vital Signs, Allergies, Observations, Concerns, Missing Info, Inconsistencies, Requires Review).
  - Pydantic schema validation with automatic JSON repair loop.
  - Configurable LLM API provider support (`OpenAI`, `Gemini`, `Custom REST API`) with a built-in deterministic heuristic engine for local execution when no API key is set.
- **Structured Interactive Healthcare UI:**
  - Professional healthcare technology dashboard with real-time statistics calculated from actual database records.
  - Interactive report history with searching, status filtering, pagination, and deletion.
  - Downloadable PDF clinical reports generated dynamically using ReportLab.
- **Database Persistence & API:**
  - Modular FastAPI backend with SQLite/PostgreSQL ORM models via SQLAlchemy.
  - Full suite of RESTful API endpoints for text/file analysis, report CRUD, health check, and PDF export.

---

## Technology Stack

### Frontend
- **Framework:** React 18 + TypeScript + Vite
- **Styling:** Tailwind CSS + Lucide Icons
- **Routing & Forms:** React Router v6, React Hook Form, Zod validation
- **HTTP Client:** Axios

### Backend
- **Framework:** Python 3.14 + FastAPI + Uvicorn
- **ORM & Database:** SQLAlchemy + SQLite (PostgreSQL compatible)
- **Document Processing:** PyMuPDF (`fitz`), Pillow (`PIL`), OpenCV (`cv2`), `pytesseract`
- **Report Export:** ReportLab PDF Engine
- **Testing:** `pytest` + `httpx` / FastAPI `TestClient`

---

## Directory Structure

```
Clinical Document/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app & lifespan initializer
│   │   ├── config.py            # BaseSettings configuration
│   │   ├── database.py          # SQLAlchemy engine & session factory
│   │   ├── seed_data.py         # Initial synthetic demo data seeder
│   │   ├── models/              # SQLAlchemy ORM models (ClinicalReport)
│   │   ├── schemas/             # Pydantic validation schemas
│   │   ├── api/routes/          # REST endpoints (health, analyze, reports)
│   │   ├── services/            # Document processor, OCR, PDF, AI analyzer, PDF generator
│   │   ├── utils/               # Validation & error handlers
│   │   └── tests/               # Pytest suite for health, analyze, reports
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/          # Header, Footer, ProcessingState, StructuredReportView
│   │   ├── pages/               # Dashboard, NewReview, ReportDetail, ReportHistory, SettingsAbout
│   │   ├── services/            # Axios API client
│   │   ├── types/               # TypeScript interfaces
│   │   ├── utils/               # Helper functions
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── index.html
├── README.md
├── ARCHITECTURE.md
├── AI_ML_DESIGN.md
├── TECHNICAL_DECISIONS.md
└── .env.example
```

---

## Environment Variables Setup

Copy `.env.example` to `.env` in the root and `backend/` directory:

```bash
# Backend Configuration (.env)
APP_NAME="ClinReview AI"
APP_VERSION="1.0.0"
DEBUG=True
DATABASE_URL="sqlite:///./clinreview.db"

# AI Provider Configuration
# Set AI_PROVIDER to 'openai', 'gemini', 'custom', or 'mock'
AI_PROVIDER="mock"
AI_API_KEY=""
AI_MODEL="gpt-4o-mini"
AI_BASE_URL=""
MAX_FILE_SIZE_MB=10

# Frontend Configuration (frontend/.env)
VITE_API_BASE_URL="http://127.0.0.1:8000/api"
```

---

## Installation & Running Locally

### 1. Start the Backend Server

```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
The FastAPI backend will launch on `http://127.0.0.1:8000`. Swagger API documentation will be available at `http://127.0.0.1:8000/docs`.

### 2. Start the Frontend Development Server

```bash
cd frontend
npm install
npm run dev
```
The Vite development server will start on `http://localhost:5173`.

---

## Running Backend Unit Tests

Run the test suite using pytest:

```bash
$env:PYTHONPATH="backend"; python -m pytest backend/app/tests
```

All 9 backend test cases (Health, Text Submission, Empty Text Rejection, Unsupported File Rejection, Valid PDF Processing, Invalid PDF Handling, Report Persistence, Retrieval, Deletion) pass cleanly.

---

## API Endpoints

- `GET /api/health` - Backend health and AI provider configuration status.
- `POST /api/analyze/text` - Analyze raw clinical text notes.
- `POST /api/analyze/file` - Upload PDF or image file (PNG, JPG, JPEG) for OCR and AI analysis.
- `GET /api/reports/dashboard` - Get calculated database statistics and recent reports.
- `GET /api/reports` - Get all reports with search, status filtering (`Completed`, `Processing`, `Failed`), and pagination.
- `GET /api/reports/{id}` - Get full structured report details by ID.
- `GET /api/reports/{id}/status` - Check current processing status.
- `DELETE /api/reports/{id}` - Delete a report from the database.
- `GET /api/reports/{id}/download` - Download professional PDF clinical report.

---

## Deployment Instructions

### Backend (Render / Railway)
1. Deploy the `backend/` directory to Render or Railway.
2. Set environment variables (`AI_PROVIDER`, `AI_API_KEY`, `DATABASE_URL`).
3. Set build command to `pip install -r requirements.txt` and start command to `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.

### Frontend (Vercel / Netlify)
1. Deploy `frontend/` directory to Vercel or Netlify.
2. Set build command `npm run build` and output directory `dist`.
3. Configure `VITE_API_BASE_URL` to point to your live hosted backend URL.
