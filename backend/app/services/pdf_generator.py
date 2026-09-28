import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from app.models.report import ClinicalReport

def generate_report_pdf(report: ClinicalReport) -> bytes:
    """Generate a clean, professional medical PDF report from ClinicalReport database model."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A')
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#0284C7')
    )

    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155')
    )

    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#64748B')
    )

    elements = []

    # Header
    elements.append(Paragraph("ClinReview AI – Intelligent Clinical Report", title_style))
    elements.append(Paragraph(f"Report ID: {report.id}  |  Date: {report.created_at.strftime('%Y-%m-%d %H:%M UTC')}  |  Status: {report.processing_status}", subtitle_style))
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284C7'), spaceBefore=2, spaceAfter=12))

    s_data = report.structured_report or {}

    # 1. Summary
    elements.append(Paragraph("1. Report Summary", heading_style))
    elements.append(Paragraph(report.report_summary or "No summary available.", body_style))
    elements.append(Spacer(1, 10))

    # 2. Patient Information
    patient = s_data.get("patient_information", {})
    elements.append(Paragraph("2. Patient Information", heading_style))
    p_info = [
        [Paragraph(f"<b>Patient ID:</b> {patient.get('patient_id') or 'Not documented'}", body_style),
         Paragraph(f"<b>Age:</b> {patient.get('age') or 'Not documented'}", body_style)],
        [Paragraph(f"<b>Sex:</b> {patient.get('sex') or 'Not documented'}", body_style),
         Paragraph(f"<b>Demographics:</b> {patient.get('demographics') or 'N/A'}", body_style)]
    ]
    t_patient = Table(p_info, colWidths=[270, 270])
    t_patient.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t_patient)
    elements.append(Spacer(1, 10))

    # 3. Vital Signs
    vitals = s_data.get("vital_signs", {})
    elements.append(Paragraph("3. Vital Signs", heading_style))
    v_info = [
        [Paragraph(f"<b>BP:</b> {vitals.get('blood_pressure') or 'N/A'}", body_style),
         Paragraph(f"<b>Heart Rate:</b> {vitals.get('heart_rate') or 'N/A'}", body_style),
         Paragraph(f"<b>Temp:</b> {vitals.get('temperature') or 'N/A'}", body_style)],
        [Paragraph(f"<b>SpO2:</b> {vitals.get('oxygen_saturation') or 'N/A'}", body_style),
         Paragraph(f"<b>Resp Rate:</b> {vitals.get('respiratory_rate') or 'N/A'}", body_style),
         Paragraph(f"<b>Height/Weight:</b> {vitals.get('height') or 'N/A'} / {vitals.get('weight') or 'N/A'}", body_style)]
    ]
    t_vitals = Table(v_info, colWidths=[180, 180, 180])
    t_vitals.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t_vitals)
    elements.append(Spacer(1, 10))

    # 4. Symptoms & Diagnoses
    symptoms = s_data.get("symptoms", [])
    diagnoses = s_data.get("diagnoses", [])
    elements.append(Paragraph("4. Extracted Symptoms & Diagnoses", heading_style))
    elements.append(Paragraph(f"<b>Symptoms:</b> {', '.join(symptoms) if symptoms else 'None documented'}", body_style))
    elements.append(Paragraph(f"<b>Diagnoses (Documented):</b> {', '.join(diagnoses) if diagnoses else 'None explicitly documented'}", body_style))
    elements.append(Spacer(1, 10))

    # 5. Medications
    meds = s_data.get("medications", [])
    elements.append(Paragraph("5. Prescribed / Documented Medications", heading_style))
    if meds:
        m_table_data = [["Medication", "Dosage", "Frequency", "Route"]]
        for m in meds:
            m_table_data.append([
                m.get("name", "N/A"),
                m.get("dosage", "N/A"),
                m.get("frequency", "N/A"),
                m.get("route", "N/A")
            ])
        t_meds = Table(m_table_data, colWidths=[160, 120, 140, 120])
        t_meds.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 6),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F8FAFC')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        elements.append(t_meds)
    else:
        elements.append(Paragraph("No medications documented.", body_style))
    elements.append(Spacer(1, 10))

    # 6. Concerns & Missing Information
    concerns = s_data.get("clinical_concerns", [])
    missing = s_data.get("missing_information", [])
    inconsistencies = s_data.get("potential_inconsistencies", [])
    requires_review = s_data.get("requires_review", [])

    elements.append(Paragraph("6. Review Flags & Clinical Audit", heading_style))
    if concerns:
        elements.append(Paragraph("<b>Clinical Concerns:</b>", body_style))
        for c in concerns:
            elements.append(Paragraph(f"• {c}", body_style))
    if missing:
        elements.append(Spacer(1, 4))
        elements.append(Paragraph("<b>Missing Information:</b>", body_style))
        for m in missing:
            elements.append(Paragraph(f"• {m}", body_style))
    if inconsistencies:
        elements.append(Spacer(1, 4))
        elements.append(Paragraph("<b>Potential Inconsistencies:</b>", body_style))
        for inc in inconsistencies:
            elements.append(Paragraph(f"• {inc}", body_style))
    if requires_review:
        elements.append(Spacer(1, 4))
        elements.append(Paragraph("<b>Requires Human Review:</b>", body_style))
        for r in requires_review:
            elements.append(Paragraph(f"• {r}", body_style))

    elements.append(Spacer(1, 15))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceBefore=5, spaceAfter=8))
    elements.append(Paragraph("DISCLAIMER: ClinReview AI is an educational document review software tool. Output is for clinical document review and demonstration purposes only, not for direct diagnosis or treatment decisions. Always verify with qualified human medical professionals.", disclaimer_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
