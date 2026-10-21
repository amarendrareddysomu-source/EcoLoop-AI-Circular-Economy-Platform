from fastapi import status
from datetime import timedelta
from app.core.security import create_access_token, decode_access_token

def test_successful_login(client):
    reg = client.post("/api/v1/auth/register", json={
        "email": "m3_user@test.org",
        "password": "SecurePassword123!",
        "full_name": "M3 Test User",
        "role": "staff"
    })
    assert reg.status_code == status.HTTP_201_CREATED

    res = client.post("/api/v1/auth/login", json={
        "email": "m3_user@test.org",
        "password": "SecurePassword123!"
    })
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["email"] == "m3_user@test.org"
    assert data["user"]["role"] == "staff"

def test_invalid_login(client):
    res = client.post("/api/v1/auth/login", json={
        "email": "nonexistent@test.org",
        "password": "WrongPassword!"
    })
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_jwt_validation_and_me(client):
    client.post("/api/v1/auth/register", json={
        "email": "jwt_user@test.org",
        "password": "SecurePassword123!",
        "full_name": "JWT User",
        "role": "auditor"
    })
    login_res = client.post("/api/v1/auth/login", json={
        "email": "jwt_user@test.org",
        "password": "SecurePassword123!"
    })
    token = login_res.json()["access_token"]

    # Valid token call to GET /auth/me
    res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["email"] == "jwt_user@test.org"

    # Invalid token call
    res_bad = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalid_token_str"})
    assert res_bad.status_code == status.HTTP_401_UNAUTHORIZED

def test_expired_token(client):
    # Create expired token (expires in -10 minutes)
    expired_jwt = create_access_token(subject="9999", expires_delta=timedelta(minutes=-10))
    decoded = decode_access_token(expired_jwt)
    assert decoded is None

    # Call endpoint with expired token
    res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {expired_jwt}"})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_role_access_checks_and_denial(client):
    # Register Super Admin, Staff, and Auditor
    client.post("/api/v1/auth/register", json={
        "email": "super_admin_m3@test.org",
        "password": "Password123!",
        "full_name": "Super Admin",
        "role": "super_admin"
    })
    client.post("/api/v1/auth/register", json={
        "email": "staff_m3@test.org",
        "password": "Password123!",
        "full_name": "Staff Member",
        "role": "staff"
    })
    client.post("/api/v1/auth/register", json={
        "email": "auditor_m3@test.org",
        "password": "Password123!",
        "full_name": "Auditor",
        "role": "auditor"
    })

    admin_token = client.post("/api/v1/auth/login", json={"email": "super_admin_m3@test.org", "password": "Password123!"}).json()["access_token"]
    staff_token = client.post("/api/v1/auth/login", json={"email": "staff_m3@test.org", "password": "Password123!"}).json()["access_token"]
    auditor_token = client.post("/api/v1/auth/login", json={"email": "auditor_m3@test.org", "password": "Password123!"}).json()["access_token"]

    # 1. Super Admin accessing system stats -> 200
    res = client.get("/api/v1/admin/stats", headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == status.HTTP_200_OK

    # 2. Staff accessing admin stats -> 403 Forbidden
    res = client.get("/api/v1/admin/stats", headers={"Authorization": f"Bearer {staff_token}"})
    assert res.status_code == status.HTTP_403_FORBIDDEN

    # 3. Auditor accessing admin stats -> 403 Forbidden
    res = client.get("/api/v1/admin/stats", headers={"Authorization": f"Bearer {auditor_token}"})
    assert res.status_code == status.HTTP_403_FORBIDDEN

def test_user_crud_operations(client):
    # Login Super Admin
    client.post("/api/v1/auth/register", json={
        "email": "crud_admin@test.org",
        "password": "Password123!",
        "full_name": "CRUD Admin",
        "role": "super_admin"
    })
    admin_token = client.post("/api/v1/auth/login", json={"email": "crud_admin@test.org", "password": "Password123!"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {admin_token}"}

    # 1. Create user via POST /api/v1/users
    create_res = client.post("/api/v1/users/", json={
        "email": "created_by_admin@test.org",
        "password": "Password123!",
        "full_name": "Created User",
        "role": "staff"
    }, headers=headers)
    assert create_res.status_code == status.HTTP_201_CREATED
    user_data = create_res.json()
    user_id = user_data["id"]
    assert user_data["email"] == "created_by_admin@test.org"

    # 2. Get user by ID GET /api/v1/users/{id}
    get_res = client.get(f"/api/v1/users/{user_id}", headers=headers)
    assert get_res.status_code == status.HTTP_200_OK
    assert get_res.json()["full_name"] == "Created User"

    # 3. List users GET /api/v1/users
    list_res = client.get("/api/v1/users/", headers=headers)
    assert list_res.status_code == status.HTTP_200_OK
    assert len(list_res.json()) >= 1

    # 4. Update user PUT /api/v1/users/{id}
    update_res = client.put(f"/api/v1/users/{user_id}", json={
        "full_name": "Updated Created User",
        "role": "auditor"
    }, headers=headers)
    assert update_res.status_code == status.HTTP_200_OK
    assert update_res.json()["full_name"] == "Updated Created User"
    assert update_res.json()["role"] == "auditor"

    # 5. Delete user DELETE /api/v1/users/{id}
    del_res = client.delete(f"/api/v1/users/{user_id}", headers=headers)
    assert del_res.status_code == status.HTTP_204_NO_CONTENT

    # 6. Verify deleted GET /api/v1/users/{id} -> 404
    get_after_del = client.get(f"/api/v1/users/{user_id}", headers=headers)
    assert get_after_del.status_code == status.HTTP_404_NOT_FOUND
