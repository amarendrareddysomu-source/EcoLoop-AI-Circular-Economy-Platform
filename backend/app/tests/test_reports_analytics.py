import pytest
from fastapi import status

def get_auth_token(client, email="rep_analytics@circulareconomy.org", role="user", full_name="Report Analytics User"):
    client.post("/api/v1/auth/register", json={
        "email": email,
        "password": "Password123!",
        "full_name": full_name,
        "role": role
    })
    res = client.post("/api/v1/auth/login", json={"email": email, "password": "Password123!"})
    return res.json()["access_token"]

def test_report_generation_and_storage(client):
    token = get_auth_token(client, email="gen_user@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    # Generate daily transactions report
    res1 = client.post("/api/v1/reports/generate", json={"report_type": "transactions", "period": "daily"}, headers=headers)
    assert res1.status_code == status.HTTP_201_CREATED
    data1 = res1.json()
    assert data1["report_type"] == "transactions"
    assert data1["period"] == "daily"
    assert "Daily Transactions Report" in data1["title"]

    # Generate monthly sustainability report
    res2 = client.post("/api/v1/reports/generate", json={"report_type": "sustainability", "period": "monthly"}, headers=headers)
    assert res2.status_code == status.HTTP_201_CREATED
    data2 = res2.json()
    assert data2["report_type"] == "sustainability"
    assert data2["period"] == "monthly"

    # Retrieve stored generated reports
    list_res = client.get("/api/v1/reports/generated", headers=headers)
    assert list_res.status_code == status.HTTP_200_OK
    assert len(list_res.json()) >= 2

def test_dashboard_analytics_overview(client):
    token = get_auth_token(client, email="dash_user@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    # Create a test item & transaction to verify metrics
    item_payload = {
        "item_name": "Solar Generator",
        "category": "Electronics",
        "quantity": 2,
        "price": 499.99,
        "condition": "New",
        "status": "Available"
    }
    item_res = client.post("/api/v1/inventory/", json=item_payload, headers=headers)
    item_id = item_res.json()["id"]

    client.post("/api/v1/transactions/", json={"item_id": item_id, "transaction_type": "sale", "quantity": 1}, headers=headers)

    # Query analytics dashboard
    res = client.get("/api/v1/analytics/dashboard", headers=headers)
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert data["total_users"] >= 1
    assert data["total_items"] >= 1
    assert data["total_transactions"] >= 1
    assert isinstance(data["co2_saved_kg"], float)
    assert isinstance(data["waste_reduced_kg"], float)
    assert isinstance(data["category_statistics"], list)

def test_chart_data_endpoints(client):
    token = get_auth_token(client, email="charts_user@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Transaction trends line chart
    r1 = client.get("/api/v1/analytics/charts/transaction-trends?days=7", headers=headers)
    assert r1.status_code == status.HTTP_200_OK
    assert r1.json()["chart_type"] == "line"
    assert len(r1.json()["labels"]) == 7

    # 2. Category distribution bar chart
    r2 = client.get("/api/v1/analytics/charts/category-distribution", headers=headers)
    assert r2.status_code == status.HTTP_200_OK
    assert r2.json()["chart_type"] == "bar"

    # 3. Recycling distribution pie chart
    r3 = client.get("/api/v1/analytics/charts/recycling-distribution", headers=headers)
    assert r3.status_code == status.HTTP_200_OK
    assert r3.json()["chart_type"] == "pie"

    # 4. Sustainability trends line chart
    r4 = client.get("/api/v1/analytics/charts/sustainability-trends?months=6", headers=headers)
    assert r4.status_code == status.HTTP_200_OK
    assert r4.json()["chart_type"] == "line"
    assert len(r4.json()["labels"]) == 6

def test_csv_export_feature(client):
    token = get_auth_token(client, email="csv_exporter@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    # Sustainability CSV export
    res1 = client.get("/api/v1/reports/export/csv?report_type=sustainability", headers=headers)
    assert res1.status_code == status.HTTP_200_OK
    assert "text/csv" in res1.headers["content-type"]
    assert "Carbon Footprint Reduction" in res1.text

    # Transactions CSV export
    res2 = client.get("/api/v1/reports/export/csv?report_type=transactions", headers=headers)
    assert res2.status_code == status.HTTP_200_OK
    assert "text/csv" in res2.headers["content-type"]
    assert "Transaction ID" in res2.text

def test_pdf_export_feature(client):
    token = get_auth_token(client, email="pdf_exporter@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    # Sustainability PDF export
    res = client.get("/api/v1/reports/export/pdf?report_type=sustainability&period=monthly", headers=headers)
    assert res.status_code == status.HTTP_200_OK
    assert "application/pdf" in res.headers["content-type"]
    assert res.content.startswith(b"%PDF")
