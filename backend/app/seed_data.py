import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.report import ClinicalReport

logger = logging.getLogger("clinreview.seed")

SYNTHETIC_SAMPLES = [
    {
        "id": "CR-SYN-1001",
        "document_name": "Outpatient Consultation - SYN-1001.txt",
        "input_type": "text",
        "original_text": """Patient ID: SYN-1001
Age: 45
Sex: Female

Chief Complaint:
Patient reports headache and fatigue for three days.

Symptoms:
- Headache
- Fatigue

Vitals:
- Blood pressure: 128/82 mmHg
- Heart rate: 84 bpm
- Temperature: 37.1 °C
- Oxygen saturation: 98%

Medication:
- Paracetamol 500 mg oral as documented in the sample note.

Allergies:
Not documented.

Clinical observation:
Patient reports persistent headache worsening in late afternoon. No focal neurological deficits.

Missing information:
- Duration and frequency of medication use are not documented.
- Relevant past medical history is not available.""",
        "extracted_text": """Patient ID: SYN-1001
Age: 45
Sex: Female

Chief Complaint:
Patient reports headache and fatigue for three days.

Symptoms:
- Headache
- Fatigue

Vitals:
- Blood pressure: 128/82 mmHg
- Heart rate: 84 bpm
- Temperature: 37.1 °C
- Oxygen saturation: 98%

Medication:
- Paracetamol 500 mg oral as documented in the sample note.

Allergies:
Not documented.

Clinical observation:
Patient reports persistent headache worsening in late afternoon. No focal neurological deficits.

Missing information:
- Duration and frequency of medication use are not documented.
- Relevant past medical history is not available.""",
        "report_summary": "Clinical review for synthetic patient SYN-1001 (45F) presenting with 3-day history of headache and fatigue. Stable vital signs (BP 128/82 mmHg, HR 84 bpm, SpO2 98%). Prescribed Paracetamol 500 mg. Notable for missing allergy history and medication frequency.",
        "structured_report": {
            "report_summary": "Clinical review for synthetic patient SYN-1001 (45F) presenting with 3-day history of headache and fatigue. Stable vital signs (BP 128/82 mmHg, HR 84 bpm, SpO2 98%). Prescribed Paracetamol 500 mg. Notable for missing allergy history and medication frequency.",
            "patient_information": {
                "patient_id": "SYN-1001",
                "age": 45,
                "sex": "Female",
                "demographics": "Synthetic Outpatient Demo Record"
            },
            "symptoms": ["Headache", "Fatigue"],
            "diagnoses": ["Acute Tension Headache"],
            "medications": [
                {
                    "name": "Paracetamol",
                    "dosage": "500 mg",
                    "frequency": "As needed",
                    "route": "Oral",
                    "notes": "Documented in note"
                }
            ],
            "vital_signs": {
                "blood_pressure": "128/82 mmHg",
                "heart_rate": "84 bpm",
                "temperature": "37.1 °C",
                "respiratory_rate": "16 /min",
                "oxygen_saturation": "98%",
                "height": "165 cm",
                "weight": "62 kg"
            },
            "allergies": ["Not documented in note"],
            "clinical_observations": ["Persistent headache worsening in late afternoon.", "No focal neurological deficits observed."],
            "clinical_concerns": ["Persistent headache without documented prior neurological baseline."],
            "missing_information": [
                "Duration and frequency of medication use are not documented.",
                "Relevant past medical history is not available.",
                "Allergy status is not recorded."
            ],
            "potential_inconsistencies": [],
            "requires_review": [
                "Confirm allergy history with patient before prescribing additional analgesics.",
                "Verify neurological baseline if symptoms persist beyond 5 days."
            ],
            "extraction_warnings": ["Synthetic Demonstration Dataset"],
            "processing_metadata": {
                "input_type": "text",
                "extraction_method": "direct_text",
                "ai_provider": "synthetic_seed"
            }
        },
        "processing_status": "Completed",
        "extraction_method": "direct_text"
    },
    {
        "id": "CR-SYN-1002",
        "document_name": "Incomplete Note - SYN-1002.pdf",
        "input_type": "pdf",
        "original_text": """Patient ID: SYN-1002
Age: 62
Sex: Male

Progress Note:
Patient admitted with shortness of breath. Prescribed Lisinopril and Metformin. BP recorded as 148/92 mmHg.
No allergy status listed on transfer sheet. Past surgical history unverified.""",
        "extracted_text": """Patient ID: SYN-1002
Age: 62
Sex: Male

Progress Note:
Patient admitted with shortness of breath. Prescribed Lisinopril and Metformin. BP recorded as 148/92 mmHg.
No allergy status listed on transfer sheet. Past surgical history unverified.""",
        "report_summary": "Incomplete clinical note review for synthetic patient SYN-1002 (62M). Shortness of breath noted with elevated blood pressure (148/92 mmHg). Missing critical medication dosages and complete allergy verification.",
        "structured_report": {
            "report_summary": "Incomplete clinical note review for synthetic patient SYN-1002 (62M). Shortness of breath noted with elevated blood pressure (148/92 mmHg). Missing critical medication dosages and complete allergy verification.",
            "patient_information": {
                "patient_id": "SYN-1002",
                "age": 62,
                "sex": "Male",
                "demographics": "Synthetic Inpatient Transfer Record"
            },
            "symptoms": ["Shortness of breath"],
            "diagnoses": ["Dyspnea"],
            "medications": [
                {
                    "name": "Lisinopril",
                    "dosage": "Not specified",
                    "frequency": "Not specified",
                    "route": "Oral",
                    "notes": "Missing dosage on transfer note"
                },
                {
                    "name": "Metformin",
                    "dosage": "Not specified",
                    "frequency": "Not specified",
                    "route": "Oral",
                    "notes": "Missing dosage on transfer note"
                }
            ],
            "vital_signs": {
                "blood_pressure": "148/92 mmHg",
                "heart_rate": "Not recorded",
                "temperature": "Not recorded",
                "respiratory_rate": "Not recorded",
                "oxygen_saturation": "Not recorded"
            },
            "allergies": ["Not documented on transfer sheet"],
            "clinical_observations": ["Patient admitted with shortness of breath."],
            "clinical_concerns": ["Stage 2 Hypertension BP reading (148/92 mmHg).", "Unmonitored shortness of breath without oxygen saturation measurement."],
            "missing_information": [
                "Lisinopril dosage and frequency missing.",
                "Metformin dosage and frequency missing.",
                "Heart rate, temperature, and SpO2 vital signs unrecorded.",
                "Allergy status unverified.",
                "Past surgical history unverified."
            ],
            "potential_inconsistencies": [],
            "requires_review": [
                "Immediate reconciliation of Lisinopril and Metformin dosages required.",
                "Obtain pulse oximetry and full baseline vital signs."
            ],
            "extraction_warnings": ["Extracted from scanned PDF document"],
            "processing_metadata": {
                "input_type": "pdf",
                "extraction_method": "pymupdf_direct",
                "ai_provider": "synthetic_seed"
            }
        },
        "processing_status": "Completed",
        "extraction_method": "pymupdf_direct"
    },
    {
        "id": "CR-SYN-1003",
        "document_name": "Conflicting Observations - SYN-1003.txt",
        "input_type": "text",
        "original_text": """Patient ID: SYN-1003
Age: 38
Sex: Female

Subjective:
Patient complains of severe high fever and body aches since yesterday morning.

Objective Vitals:
Temperature: 36.6 °C (Axillary)
Heart Rate: 72 bpm
Blood Pressure: 116/74 mmHg
SpO2: 99%

Allergies: Penicillin (causes severe anaphylactic hives)
Current Meds: Amoxicillin 500mg TID prescribed by urgent care center.""",
        "extracted_text": """Patient ID: SYN-1003
Age: 38
Sex: Female

Subjective:
Patient complains of severe high fever and body aches since yesterday morning.

Objective Vitals:
Temperature: 36.6 °C (Axillary)
Heart Rate: 72 bpm
Blood Pressure: 116/74 mmHg
SpO2: 99%

Allergies: Penicillin (causes severe anaphylactic hives)
Current Meds: Amoxicillin 500mg TID prescribed by urgent care center.""",
        "report_summary": "High risk clinical contradiction review for SYN-1003 (38F). Critical allergy alert: Patient has documented severe Penicillin anaphylaxis, yet is currently prescribed Amoxicillin (a penicillin-class antibiotic). Subjective high fever contradicts objective normal temperature (36.6 °C).",
        "structured_report": {
            "report_summary": "High risk clinical contradiction review for SYN-1003 (38F). Critical allergy alert: Patient has documented severe Penicillin anaphylaxis, yet is currently prescribed Amoxicillin (a penicillin-class antibiotic). Subjective high fever contradicts objective normal temperature (36.6 °C).",
            "patient_information": {
                "patient_id": "SYN-1003",
                "age": 38,
                "sex": "Female",
                "demographics": "Synthetic Urgent Care Record"
            },
            "symptoms": ["Fever (subjective)", "Body aches"],
            "diagnoses": ["Viral syndrome"],
            "medications": [
                {
                    "name": "Amoxicillin",
                    "dosage": "500 mg",
                    "frequency": "Three times daily (TID)",
                    "route": "Oral",
                    "notes": "CONTRAINDICATED due to Penicillin allergy"
                }
            ],
            "vital_signs": {
                "blood_pressure": "116/74 mmHg",
                "heart_rate": "72 bpm",
                "temperature": "36.6 °C",
                "oxygen_saturation": "99%"
            },
            "allergies": ["Penicillin (Severe anaphylactic hives)"],
            "clinical_observations": ["Subjective fever reported by patient.", "Objective temperature reading is 36.6 C (afebrile)."],
            "clinical_concerns": ["CRITICAL DRUG-ALLERGY SAFETY RISK: Amoxicillin prescribed despite documented Penicillin anaphylaxis history."],
            "missing_information": ["Indication for urgent care antibiotic prescription is unspecified."],
            "potential_inconsistencies": [
                "Patient reports severe high fever, but documented objective temperature is 36.6 °C (normal).",
                "Amoxicillin (Penicillin class) active prescription directly conflicts with Penicillin allergy record."
            ],
            "requires_review": [
                "IMMEDIATE ACTION REQUIRED: Discontinue Amoxicillin and review alternative non-beta-lactam therapy.",
                "Re-evaluate temperature with core thermometer."
            ],
            "extraction_warnings": ["Critical Allergy Contradiction Detected"],
            "processing_metadata": {
                "input_type": "text",
                "extraction_method": "direct_text",
                "ai_provider": "synthetic_seed"
            }
        },
        "processing_status": "Completed",
        "extraction_method": "direct_text"
    },
    {
        "id": "CR-SYN-1004",
        "document_name": "Scanned Document OCR - SYN-1004.png",
        "input_type": "image",
        "original_text": """PATIENT RECORD / SCANNED NOTE
Patient ID: SYN-1004
Age: 55 | Sex: Male
Chief Complaint: Progressive shortness of breath and mild chest pain.
Vital Signs: BP 142/90 mmHg, HR 88 bpm, Temp 37.0 C, SpO2 95% on room air.
Medications: Lisinopril 10mg daily, Aspirin 81mg daily.
Allergies: Penicillin (Rash).
Observations: Bilateral mild lung crackles. Recommend EKG and troponin lab evaluation.""",
        "extracted_text": """PATIENT RECORD / SCANNED NOTE
Patient ID: SYN-1004
Age: 55 | Sex: Male
Chief Complaint: Progressive shortness of breath and mild chest pain.
Vital Signs: BP 142/90 mmHg, HR 88 bpm, Temp 37.0 C, SpO2 95% on room air.
Medications: Lisinopril 10mg daily, Aspirin 81mg daily.
Allergies: Penicillin (Rash).
Observations: Bilateral mild lung crackles. Recommend EKG and troponin lab evaluation.""",
        "report_summary": "Scanned document OCR analysis for synthetic patient SYN-1004 (55M). Presenting with dyspnea, chest pain, and bilateral lung crackles. SpO2 95% on room air. EKG and cardiac troponin evaluation recommended.",
        "structured_report": {
            "report_summary": "Scanned document OCR analysis for synthetic patient SYN-1004 (55M). Presenting with dyspnea, chest pain, and bilateral lung crackles. SpO2 95% on room air. EKG and cardiac troponin evaluation recommended.",
            "patient_information": {
                "patient_id": "SYN-1004",
                "age": 55,
                "sex": "Male",
                "demographics": "Synthetic Scanned Document Record"
            },
            "symptoms": ["Progressive shortness of breath", "Mild chest pain"],
            "diagnoses": ["Chest Pain / Dyspnea under investigation"],
            "medications": [
                {
                    "name": "Lisinopril",
                    "dosage": "10 mg",
                    "frequency": "Daily",
                    "route": "Oral"
                },
                {
                    "name": "Aspirin",
                    "dosage": "81 mg",
                    "frequency": "Daily",
                    "route": "Oral"
                }
            ],
            "vital_signs": {
                "blood_pressure": "142/90 mmHg",
                "heart_rate": "88 bpm",
                "temperature": "37.0 °C",
                "oxygen_saturation": "95% (Room Air)"
            },
            "allergies": ["Penicillin (Rash)"],
            "clinical_observations": ["Bilateral mild lung crackles on auscultation."],
            "clinical_concerns": ["Cardiopulmonary symptom combination (chest pain + dyspnea + crackles + borderline SpO2 95%)."],
            "missing_information": ["Baseline EKG and troponin results pending."],
            "potential_inconsistencies": [],
            "requires_review": [
                "Stat EKG and cardiac biomarker laboratory verification required.",
                "Monitor oxygen saturation trend."
            ],
            "extraction_warnings": ["Processed via Image OCR Pipeline"],
            "processing_metadata": {
                "input_type": "image",
                "extraction_method": "tesseract_ocr",
                "ai_provider": "synthetic_seed"
            }
        },
        "processing_status": "Completed",
        "extraction_method": "tesseract_ocr"
    }
]

def seed_synthetic_data(db: Session):
    count = db.query(ClinicalReport).count()
    if count == 0:
        logger.info("Seeding initial synthetic demonstration dataset...")
        for sample in SYNTHETIC_SAMPLES:
            report = ClinicalReport(
                id=sample["id"],
                document_name=sample["document_name"],
                input_type=sample["input_type"],
                original_text=sample["original_text"],
                extracted_text=sample["extracted_text"],
                report_summary=sample["report_summary"],
                structured_report=sample["structured_report"],
                processing_status=sample["processing_status"],
                extraction_method=sample["extraction_method"],
                created_at=datetime.now(timezone.utc),
                completed_at=datetime.now(timezone.utc)
            )
            db.add(report)
        db.commit()
        logger.info("Synthetic demonstration dataset seeded successfully.")
