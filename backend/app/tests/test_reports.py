from fastapi import status

def get_user_and_admin_tokens(client):
    client.post("/api/v1/auth/register", json={
        "email": "reporter@test.org",
        "password": "Password123!",
        "full_name": "Reporter User",
        "role": "user"
    })
    res_user = client.post("/api/v1/auth/login", json={"email": "reporter@test.org", "password": "Password123!"})
    user_token = res_user.json()["access_token"]

    client.post("/api/v1/auth/register", json={
        "email": "report_admin@test.org",
        "password": "Password123!",
        "full_name": "Report Admin",
        "role": "admin"
    })
    res_admin = client.post("/api/v1/auth/login", json={"email": "report_admin@test.org", "password": "Password123!"})
    admin_token = res_admin.json()["access_token"]

    return user_token, admin_token

def test_report_lifecycle(client):
    user_token, admin_token = get_user_and_admin_tokens(client)

    # 1. Submit report
    report_payload = {
        "title": "Broken item classification query",
        "description": "The AI classifier predicted plastic instead of glass.",
        "report_type": "system_feedback"
    }
    res = client.post(
        "/api/v1/reports/",
        json=report_payload,
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert res.status_code == status.HTTP_201_CREATED
    report_data = res.json()
    assert report_data["title"] == "Broken item classification query"
    report_id = report_data["id"]

    # 2. List user's reports
    res = client.get("/api/v1/reports/my-reports", headers={"Authorization": f"Bearer {user_token}"})
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) >= 1

    # 3. Admin list all reports
    res = client.get("/api/v1/reports/", headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) >= 1

    # 4. Admin update report status
    res = client.put(
        f"/api/v1/reports/{report_id}/status",
        json={"status": "Resolved", "admin_notes": "Classification rules tuned."},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["status"] == "Resolved"
