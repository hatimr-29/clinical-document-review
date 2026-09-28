# ClinReview AI – AI/ML Architecture & Design Document

This document details the machine learning design, prompt engineering strategies, document OCR workflows, Pydantic JSON schema enforcement, missing information detection, and safety mechanisms used in **ClinReview AI**.

---

## 1. AI/ML Pipeline Overview

ClinReview AI uses a hybrid document intelligence and clinical entity extraction pipeline:

1. **Document Ingestion & Preprocessing:**
   - **PDF Extractor:** PyMuPDF (`fitz`) parses text streams. Automatically calculates text density per page to flag scanned PDFs and trigger page image rendering.
   - **Image OCR Engine:** Converts image bytes to OpenCV arrays, applies grayscale conversion, contrast normalization, and denoising before calling `pytesseract`.
2. **Clinical Entity Extraction Engine:**
   - **External LLM Provider:** Configurable API client supporting OpenAI API specifications or custom REST endpoints (`gpt-4o-mini`, Gemini, etc.). Uses system prompts designed to enforce strict fact grounding.
   - **ClinReview AI Heuristic Engine (Mock Provider):** High-precision regex pattern matcher and clinical rule evaluator that runs locally when no external API key is provided.
3. **Validation & JSON Repair Loop:**
   - Parses LLM output against Pydantic's `StructuredReportSchema`.
   - If malformed JSON or type mismatches occur, an automated repair loop fixes key structures and re-validates before database persistence.

---

## 2. Prompt Engineering Strategy

The system prompt enforces strict clinical document review boundaries:

- **Fact Grounding:** Instructs the LLM to extract *only* information supported by the source document.
- **No Diagnostic Inventions:** Explicitly forbids inventing patient ages, missing dosages, or speculative diagnoses.
- **Distinguishing Facts from Review Flags:** Demarcates documented patient complaints/diagnoses from AI-generated review concerns.
- **Uncertainty & Missing Data:** Replaces missing details with explicit `"Not documented"` or `null` values rather than arbitrary defaults.
- **Contradiction Detection:** Explicitly prompts the model to highlight clinical contradictions (e.g. subjective fever vs afebrile temp, or Penicillin allergy vs active Amoxicillin prescription).

---

## 3. Pydantic Structured JSON Schema

All AI outputs adhere to the following schema structure:

```json
{
  "report_summary": "Concise clinical summary...",
  "patient_information": {
    "patient_id": "SYN-1001",
    "age": 45,
    "sex": "Female",
    "demographics": "Outpatient"
  },
  "symptoms": ["Headache", "Fatigue"],
  "diagnoses": ["Acute Tension Headache"],
  "medications": [
    {
      "name": "Paracetamol",
      "dosage": "500 mg",
      "frequency": "As needed",
      "route": "Oral",
      "notes": "Extracted from note"
    }
  ],
  "vital_signs": {
    "blood_pressure": "128/82 mmHg",
    "heart_rate": "84 bpm",
    "temperature": "37.1 °C",
    "respiratory_rate": "16 /min",
    "oxygen_saturation": "98%",
    "height": null,
    "weight": null
  },
  "allergies": ["Not documented in note"],
  "clinical_observations": ["Observation notes"],
  "clinical_concerns": ["Persistent headache worsening in late afternoon"],
  "missing_information": ["Medication frequency missing"],
  "potential_inconsistencies": [],
  "requires_review": ["Confirm allergy history"],
  "extraction_warnings": [],
  "processing_metadata": {
    "input_type": "text",
    "extraction_method": "direct_text",
    "ai_provider": "mock"
  }
}
```

---

## 4. Error Handling & Safety Controls

- **Unreadable Documents:** If extracted text is less than 10 characters or corrupted, extraction is halted with a clear HTTP 400 error (`DOCUMENT_PROCESSING_FAILED`).
- **Malformed JSON Handling:** If LLM output fails Pydantic validation, `repair_malformed_json_dict()` cleans up types, fills required schema keys, and attempts re-validation.
- **Fallback Guarantee:** If external API calls fail (e.g., rate limit, network timeout, invalid key), the system seamlessly falls back to the internal clinical heuristic engine and appends a clear extraction warning to the report.
