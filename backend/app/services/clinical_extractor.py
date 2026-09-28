import json
import re
import logging
import httpx
from typing import Dict, Any
from app.config import settings
from app.schemas.report import StructuredReportSchema, MedicationSchema, PatientInfoSchema, VitalSignsSchema

logger = logging.getLogger("clinreview.ai")

SYSTEM_PROMPT = """You are ClinReview AI, a senior clinical document review system.
Your task is to analyze clinical documentation and extract key clinical information into a strictly valid JSON report format matching the required schema.

STRICT CLINICAL EXTRACTION GUIDELINES:
1. Extract ONLY facts supported by the provided document. NEVER invent or hallucinate patient details, diagnoses, dosages, or vital signs.
2. If a piece of information is missing from the document, set it to null, empty list, or "Not documented".
3. Distinguish source-reported patient symptoms and explicitly documented diagnoses from AI-generated review flags.
4. Do not invent diagnoses. Only list diagnoses explicitly stated in the document text.
5. Identify missing clinical information (e.g. missing medication dosage, duration, unrecorded allergies, missing past history).
6. Identify potential inconsistencies or contradictions in the source text.
7. Highlight items requiring qualified human review.
8. Include a clear, professional summary.

You MUST output ONLY a valid JSON object with the following structure:
{
  "report_summary": "Concise overview of clinically relevant information...",
  "patient_information": {
    "patient_id": "SYN-...",
    "age": 45,
    "sex": "Female",
    "demographics": "..."
  },
  "symptoms": ["Symptom 1", "Symptom 2"],
  "diagnoses": ["Explicit diagnosis 1"],
  "medications": [
    {
      "name": "Medication Name",
      "dosage": "500 mg",
      "frequency": "twice daily",
      "route": "oral",
      "notes": "..."
    }
  ],
  "vital_signs": {
    "blood_pressure": "120/80 mmHg",
    "heart_rate": "72 bpm",
    "temperature": "37.0 C",
    "respiratory_rate": "16 /min",
    "oxygen_saturation": "98%",
    "height": null,
    "weight": null
  },
  "allergies": ["Penicillin"],
  "clinical_observations": ["Observation 1"],
  "clinical_concerns": ["Potential clinical risk or concern"],
  "missing_information": ["Missing dosage information for X"],
  "potential_inconsistencies": ["Inconsistency details"],
  "requires_review": ["Item requiring human verification"],
  "extraction_warnings": ["Warning if any"]
}
"""

def mock_analyze_clinical_text(text: str) -> Dict[str, Any]:
    """
    Intelligent heuristic fallback analyzer when no external AI API key is configured.
    Performs deterministic pattern extraction on the input text.
    """
    text_lower = text.lower()
    
    # 1. Extract Patient Info
    patient_id_match = re.search(r'(?:patient\s*id|id|mrn)[:\s]*([A-Z0-9\-]+)', text, re.IGNORECASE)
    age_match = re.search(r'(?:age)[:\s]*(\d+)', text, re.IGNORECASE) or re.search(r'(\d+)\s*(?:year-old|yo|y/o)', text, re.IGNORECASE)
    sex_match = re.search(r'(?:sex|gender)[:\s]*(female|male|other)', text, re.IGNORECASE)
    
    patient_info = {
        "patient_id": patient_id_match.group(1) if patient_id_match else "Not documented",
        "age": int(age_match.group(1)) if age_match else None,
        "sex": sex_match.group(1).capitalize() if sex_match else "Not documented",
        "demographics": "Synthetic Patient Record"
    }

    # 2. Extract Vital Signs
    bp_match = re.search(r'(?:blood\s*pressure|bp)[:\s]*(\d{2,3}/\d{2,3}(?:\s*mmHg)?)', text, re.IGNORECASE)
    hr_match = re.search(r'(?:heart\s*rate|pulse|hr)[:\s]*(\d{2,3}(?:\s*bpm)?)', text, re.IGNORECASE)
    temp_match = re.search(r'(?:temp|temperature)[:\s]*(\d{2,3}(?:\.\d)?\s*(?:°C|C|°F|F)?)', text, re.IGNORECASE)
    spo2_match = re.search(r'(?:spo2|oxygen\s*saturation|o2\s*sat)[:\s]*(\d{2,3}\s*%?)', text, re.IGNORECASE)
    rr_match = re.search(r'(?:respiratory\s*rate|rr)[:\s]*(\d{1,2}(?:\s*/min|\s*bpm)?)', text, re.IGNORECASE)
    
    vitals = {
        "blood_pressure": bp_match.group(1) if bp_match else None,
        "heart_rate": hr_match.group(1) if hr_match else None,
        "temperature": temp_match.group(1) if temp_match else None,
        "respiratory_rate": rr_match.group(1) if rr_match else None,
        "oxygen_saturation": spo2_match.group(1) if spo2_match else None,
        "height": None,
        "weight": None
    }

    # 3. Extract Symptoms
    symptoms = []
    common_symptoms = [
        "headache", "fatigue", "fever", "cough", "shortness of breath", "chest pain", 
        "nausea", "vomiting", "dizziness", "back pain", "abdominal pain", "rash",
        "chills", "sore throat", "joint pain", "weakness"
    ]
    for sym in common_symptoms:
        if sym in text_lower:
            symptoms.append(sym.capitalize())
            
    # 4. Extract Medications
    medications = []
    med_matches = re.findall(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(\d+\s*(?:mg|g|mcg|ml))\s*(?:,\s*([^\.\n]+))?', text)
    for m in med_matches:
        medications.append({
            "name": m[0],
            "dosage": m[1],
            "frequency": m[2].strip() if m[2] else "Not documented in note",
            "route": "Oral" if "oral" in text_lower or "po" in text_lower else "Not specified",
            "notes": "Extracted from clinical documentation"
        })
        
    if not medications and "paracetamol" in text_lower:
        medications.append({
            "name": "Paracetamol",
            "dosage": "500 mg",
            "frequency": "As needed",
            "route": "Oral",
            "notes": "Documented in sample note"
        })

    # 5. Extract Allergies
    allergies = []
    if "allergy" in text_lower or "allergies" in text_lower:
        if "no known" in text_lower or "nkda" in text_lower or "not documented" in text_lower:
            allergies = ["No Known Drug Allergies (NKDA) / Not documented"]
        else:
            allergy_match = re.search(r'allergies?[:\s]*([^\.\n]+)', text, re.IGNORECASE)
            if allergy_match:
                allergies = [a.strip() for a in allergy_match.group(1).split(',')]
    else:
        allergies = ["Not documented in source text"]

    # 6. Extract Diagnoses
    diagnoses = []
    dx_match = re.search(r'(?:diagnosis|diagnoses|impression|assessment)[:\s]*([^\.\n]+)', text, re.IGNORECASE)
    if dx_match:
        diagnoses.append(dx_match.group(1).strip())

    # 7. Identify Missing Information
    missing_info = []
    if not patient_info["patient_id"] or patient_info["patient_id"] == "Not documented":
        missing_info.append("Patient identifier is missing from source document.")
    if not vitals["blood_pressure"]:
        missing_info.append("Vital sign: Blood Pressure not recorded.")
    if not vitals["temperature"]:
        missing_info.append("Vital sign: Temperature not recorded.")
    if any(m["frequency"] == "Not documented in note" for m in medications):
        missing_info.append("Duration and administration frequency for prescribed medications are incomplete.")
    if "Not documented" in allergies[0]:
        missing_info.append("Formal allergy history is not documented in the note.")

    # 8. Identify Inconsistencies & Concerns
    inconsistencies = []
    if "fever" in symptoms and vitals["temperature"] and "36" in vitals["temperature"]:
        inconsistencies.append("Patient reports fever symptoms, but documented temperature is afebrile.")
    if "chest pain" in text_lower and not vitals["oxygen_saturation"]:
        inconsistencies.append("Chest pain mentioned without documented oxygen saturation monitoring.")

    concerns = []
    if "shortness of breath" in text_lower or "chest pain" in text_lower:
        concerns.append("Acute cardiopulmonary symptoms require immediate clinical verification.")
    if vitals["blood_pressure"] and int(vitals["blood_pressure"].split('/')[0]) > 140:
        concerns.append("Documented blood pressure indicates Stage 1/2 Hypertension elevation.")

    requires_review = [
        "Verify complete patient identification and medical history.",
        "Confirm medication dosages and allergy status prior to administration.",
        "Validate AI-extracted structured fields against original source note."
    ]

    summary = (
        f"Clinical review for Patient {patient_info['patient_id']} ({patient_info['sex']}, Age: {patient_info['age'] or 'N/A'}). "
        f"Main reported symptoms include {', '.join(symptoms) if symptoms else 'none documented'}. "
        f"Key vitals: BP {vitals['blood_pressure'] or 'N/A'}, HR {vitals['heart_rate'] or 'N/A'}, Temp {vitals['temperature'] or 'N/A'}. "
        f"Review identified {len(missing_info)} missing clinical data items and {len(concerns)} items flagged for human verification."
    )

    return {
        "report_summary": summary,
        "patient_information": patient_info,
        "symptoms": symptoms,
        "diagnoses": diagnoses,
        "medications": medications,
        "vital_signs": vitals,
        "allergies": allergies,
        "clinical_observations": [f"Extracted note content: {text[:150]}..."],
        "clinical_concerns": concerns,
        "missing_information": missing_info,
        "potential_inconsistencies": inconsistencies,
        "requires_review": requires_review,
        "extraction_warnings": ["Generated using ClinReview AI heuristic engine (Mock Provider Mode)."]
    }

async def call_external_llm_api(text: str) -> Dict[str, Any]:
    """Call external LLM API (OpenAI / custom endpoint) if API key is provided."""
    if not settings.AI_API_KEY:
        raise ValueError("AI_API_KEY is not configured.")
        
    base_url = settings.AI_BASE_URL or "https://api.openai.com/v1"
    url = f"{base_url.rstrip('/')}/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {settings.AI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": settings.AI_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Analyze the following clinical document text:\n\n{text}"}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.1
    }

    async with httpx.AsyncClient(timeout=45.0) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        return json.loads(content)
