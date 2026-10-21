import pytest
import io
from fastapi import status
from app.core.security import create_access_token, create_refresh_token

def test_jwt_tampered_token_rejection(client):
    token = create_access_token(subject="1", role="user")
    tampered_token = token[:-5] + "XXXXX"
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {tampered_token}"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_jwt_refresh_token_used_as_access_token_rejection(client):
    refresh_tok = create_refresh_token(subject="1")
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {refresh_tok}"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_unauthorized_endpoints_access_rejection(client):
    protected_urls = [
        ("/api/v1/auth/me", "GET"),
        ("/api/v1/items/my-items", "GET"),
        ("/api/v1/transactions/", "GET"),
        ("/api/v1/admin/stats", "GET"),
        ("/api/v1/ngo/requests", "GET"),
        ("/api/v1/recycling/processing-queue", "GET"),
    ]
    for url, method in protected_urls:
        if method == "GET":
            res = client.get(url)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_rbac_cross_role_access_prevention(client):
    # Register regular user
    client.post("/api/v1/auth/register", json={
        "email": "audit_user@test.org",
        "password": "Password123!",
        "full_name": "Audit User",
        "role": "user"
    })
    token = client.post("/api/v1/auth/login", json={
        "email": "audit_user@test.org",
        "password": "Password123!"
    }).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Attempt admin endpoint access -> 403
    res = client.get("/api/v1/admin/stats", headers=headers)
    assert res.status_code == status.HTTP_403_FORBIDDEN

    # Attempt NGO endpoint access -> 403
    res = client.get("/api/v1/ngo/donations/available", headers=headers)
    assert res.status_code == status.HTTP_403_FORBIDDEN

    # Attempt Recycler endpoint access -> 403
    res = client.get("/api/v1/recycling/items/available", headers=headers)
    assert res.status_code == status.HTTP_403_FORBIDDEN

def test_file_upload_security_magic_bytes_validation(client):
    # Register user
    client.post("/api/v1/auth/register", json={
        "email": "uploader@test.org",
        "password": "Password123!",
        "full_name": "Uploader User",
        "role": "user"
    })
    token = client.post("/api/v1/auth/login", json={
        "email": "uploader@test.org",
        "password": "Password123!"
    }).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Malicious script file disguised as PNG
    fake_png_content = b"<script>alert('xss')</script>"
    files = {"image": ("malicious.png", io.BytesIO(fake_png_content), "image/png")}
    data = {"title": "Test Item", "category": "Electronics", "condition": "Good", "age_years": "1.0", "original_price": "50"}

    res = client.post("/api/v1/items/upload", data=data, files=files, headers=headers)
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid image file header" in res.json()["detail"]

def test_file_upload_valid_image_success(client):
    # Valid minimal 1x1 PNG image with correct magic bytes
    valid_png = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    
    client.post("/api/v1/auth/register", json={
        "email": "uploader_valid@test.org",
        "password": "Password123!",
        "full_name": "Valid Uploader User",
        "role": "user"
    })
    token = client.post("/api/v1/auth/login", json={
        "email": "uploader_valid@test.org",
        "password": "Password123!"
    }).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    files = {"image": ("valid.png", io.BytesIO(valid_png), "image/png")}
    data = {"title": "Valid Item", "category": "Electronics", "condition": "Good", "age_years": "1.0", "original_price": "50"}

    res = client.post("/api/v1/items/upload", data=data, files=files, headers=headers)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.json()["title"] == "Valid Item"

def test_sql_injection_payload_handled_safely(client):
    sql_inj_input = "' OR '1'='1' --"
    res = client.get(f"/api/v1/items/?category={sql_inj_input}")
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json(), list)

def test_xss_payload_stored_and_returned_safely(client):
    client.post("/api/v1/auth/register", json={
        "email": "xss_user@test.org",
        "password": "Password123!",
        "full_name": "XSS User",
        "role": "user"
    })
    token = client.post("/api/v1/auth/login", json={
        "email": "xss_user@test.org",
        "password": "Password123!"
    }).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    xss_title = "Laptop <script>alert('xss')</script>"
    res = client.post("/api/v1/items/", json={
        "title": xss_title,
        "category": "Electronics",
        "condition": "Good",
        "age_years": 1.0,
        "original_price": 500.0
    }, headers=headers)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.json()["title"] == xss_title

def test_error_response_sanitization(client):
    # Call non-existent endpoint
    res = client.get("/api/v1/nonexistent-route-xyz")
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in res.json()

def test_swagger_docs_csp_exclusion(client):
    # GET /docs should succeed with HTTP 200 and MUST NOT contain Content-Security-Policy header
    res_docs = client.get("/docs")
    assert res_docs.status_code == status.HTTP_200_OK
    assert "content-security-policy" not in res_docs.headers

    # GET /api/v1/items/ MUST retain Content-Security-Policy header
    res_api = client.get("/api/v1/items/")
    assert res_api.status_code == status.HTTP_200_OK
    assert "content-security-policy" in res_api.headers
