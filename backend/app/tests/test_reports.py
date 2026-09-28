def test_report_persistence_and_retrieval(client):
    payload = {
        "text": "Patient ID: PERSIST-100. Age 60, Male. Symptoms: Fever and cough. BP 135/85 mmHg.",
        "document_name": "Persistence_Test.txt"
    }
    create_res = client.post("/api/analyze/text", json=payload)
    assert create_res.status_code == 200
    report_id = create_res.json()["data"]["id"]

    get_res = client.get(f"/api/reports/{report_id}")
    assert get_res.status_code == 200
    data = get_res.json()["data"]
    assert data["id"] == report_id
    assert data["structured_report"]["patient_information"]["patient_id"] == "PERSIST-100"

    list_res = client.get("/api/reports")
    assert list_res.status_code == 200
    list_data = list_res.json()
    assert list_data["total"] >= 1

def test_invalid_report_id(client):
    res = client.get("/api/reports/CR-NONEXISTENT-999")
    assert res.status_code == 404
    detail = res.json().get("detail", res.json())
    assert detail["error_code"] == "REPORT_NOT_FOUND"

def test_delete_report(client):
    payload = {"text": "Patient ID: DELETE-ME. Symptoms: Mild cough for two days.", "document_name": "Delete_Test.txt"}
    create_res = client.post("/api/analyze/text", json=payload)
    assert create_res.status_code == 200
    report_id = create_res.json()["data"]["id"]

    del_res = client.delete(f"/api/reports/{report_id}")
    assert del_res.status_code == 200

    get_res = client.get(f"/api/reports/{report_id}")
    assert get_res.status_code == 404
