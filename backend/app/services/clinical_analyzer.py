import logging
import json
from typing import Dict, Any, Tuple
from app.config import settings
from app.schemas.report import StructuredReportSchema
from app.services.clinical_extractor import call_external_llm_api, mock_analyze_clinical_text

logger = logging.getLogger("clinreview.analyzer")

async def analyze_clinical_document(extracted_text: str, input_type: str, extraction_method: str, warnings: list = None) -> Tuple[StructuredReportSchema, str]:
    """
    Main orchestration entrypoint for clinical document AI analysis.
    Validates output using Pydantic, executes fallback or JSON repairs if necessary.
    """
    warnings = warnings or []
    raw_dict = None
    ai_provider_used = settings.AI_PROVIDER

    if settings.AI_API_KEY and settings.AI_PROVIDER != "mock":
        try:
            logger.info(f"Using external AI Provider ({settings.AI_PROVIDER}) for clinical analysis...")
            raw_dict = await call_external_llm_api(extracted_text)
        except Exception as e:
            logger.warning(f"External AI Provider failed: {e}. Falling back to ClinReview AI Heuristic Engine.")
            warnings.append(f"External LLM API call failed ({str(e)}). Used backup clinical analysis engine.")
            raw_dict = mock_analyze_clinical_text(extracted_text)
            ai_provider_used = "mock_fallback"
    else:
        logger.info("No AI_API_KEY configured or AI_PROVIDER set to 'mock'. Using ClinReview AI Heuristic Engine.")
        raw_dict = mock_analyze_clinical_text(extracted_text)
        ai_provider_used = "mock"

    # Merge metadata
    if "processing_metadata" not in raw_dict or not isinstance(raw_dict["processing_metadata"], dict):
        raw_dict["processing_metadata"] = {}
        
    raw_dict["processing_metadata"].update({
        "input_type": input_type,
        "extraction_method": extraction_method,
        "ai_provider": ai_provider_used,
        "model": settings.AI_MODEL if ai_provider_used not in ["mock", "mock_fallback"] else "clinreview-heuristic-v1",
        "disclaimer": "Educational & Demonstration Use Only. Requires qualified human clinical review."
    })
    
    if warnings:
        existing_warn = raw_dict.get("extraction_warnings", [])
        if isinstance(existing_warn, list):
            raw_dict["extraction_warnings"] = list(set(existing_warn + warnings))

    # Pydantic validation & repair loop
    try:
        validated_schema = StructuredReportSchema(**raw_dict)
    except Exception as validation_err:
        logger.warning(f"Initial Pydantic validation error: {validation_err}. Attempting schema repair.")
        # Attempt repair
        try:
            repaired_dict = repair_malformed_json_dict(raw_dict)
            validated_schema = StructuredReportSchema(**repaired_dict)
        except Exception as final_err:
            logger.error(f"Failed to repair structured report: {final_err}")
            raise ValueError(f"AI response failed schema validation: {str(final_err)}")

    summary = validated_schema.report_summary or "Structured clinical review completed."
    return validated_schema, summary

def repair_malformed_json_dict(d: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure key fields exist and types match Pydantic schema expectations."""
    if not isinstance(d, dict):
        d = {}
    
    d.setdefault("report_summary", "Clinical document review completed.")
    d.setdefault("patient_information", {})
    d.setdefault("symptoms", [])
    d.setdefault("diagnoses", [])
    d.setdefault("medications", [])
    d.setdefault("vital_signs", {})
    d.setdefault("allergies", [])
    d.setdefault("clinical_observations", [])
    d.setdefault("clinical_concerns", [])
    d.setdefault("missing_information", [])
    d.setdefault("potential_inconsistencies", [])
    d.setdefault("requires_review", [])
    d.setdefault("extraction_warnings", [])
    d.setdefault("processing_metadata", {})

    # Ensure list types
    for list_field in ["symptoms", "diagnoses", "allergies", "clinical_observations", "clinical_concerns", "missing_information", "potential_inconsistencies", "requires_review", "extraction_warnings"]:
        if not isinstance(d[list_field], list):
            d[list_field] = [str(d[list_field])] if d[list_field] else []

    return d
