import fitz

def test_valid_text_submission(client):
    payload = {
        "text": "Patient ID: TEST-101. Age 40, Female. Chief complaint headache and fatigue. BP 120/80 mmHg. Medication Paracetamol 500mg.",
        "document_name": "Test Note.txt"
    }
    response = client.post("/api/analyze/text", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert res["data"]["processing_status"] == "Completed"
    assert "TEST-101" in str(res["data"]["structured_report"])

def test_empty_text_rejection(client):
    payload = {"text": "   ", "document_name": "Empty.txt"}
    response = client.post("/api/analyze/text", json=payload)
    assert response.status_code == 400
    res = response.json()
    assert res["success"] is False
    assert res["error_code"] == "EMPTY_TEXT"

def test_unsupported_file_rejection(client):
    files = {"file": ("script.sh", b"echo hello", "text/x-shellscript")}
    response = client.post("/api/analyze/file", files=files)
    assert response.status_code == 400
    res = response.json()
    assert res["error_code"] == "UNSUPPORTED_FILE_TYPE"

def test_valid_pdf_processing(client):
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Patient ID: PDF-999. Age 50, Male. Symptoms: Shortness of breath. BP 130/85 mmHg.")
    pdf_bytes = doc.write()
    doc.close()

    files = {"file": ("test_doc.pdf", pdf_bytes, "application/pdf")}
    response = client.post("/api/analyze/file", files=files)
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert res["data"]["input_type"] == "pdf"

def test_invalid_pdf_handling(client):
    files = {"file": ("corrupted.pdf", b"%PDF-1.4 corrupted data content invalid", "application/pdf")}
    response = client.post("/api/analyze/file", files=files)
    assert response.status_code == 400
    res = response.json()
    detail = res.get("detail", res)
    assert detail["success"] is False
    assert detail["error_code"] == "FILE_PROCESSING_FAILED"
