from fastapi import status

def test_register_and_login_flow(client):
    # Register user
    reg_payload = {
        "email": "authtest@circulareconomy.org",
        "password": "Password123!",
        "full_name": "Auth Test User",
        "role": "user",
        "location": "Eco City"
    }
    response = client.post("/api/v1/auth/register", json=reg_payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "authtest@circulareconomy.org"

    # Login
    login_payload = {
        "email": "authtest@circulareconomy.org",
        "password": "Password123!"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == status.HTTP_200_OK
    token_data = response.json()
    assert "access_token" in token_data
    assert "refresh_token" in token_data
    assert token_data["user"]["email"] == "authtest@circulareconomy.org"

    # Refresh Token
    refresh_payload = {
        "refresh_token": token_data["refresh_token"]
    }
    response = client.post("/api/v1/auth/refresh", json=refresh_payload)
    assert response.status_code == status.HTTP_200_OK
    refreshed_data = response.json()
    assert "access_token" in refreshed_data

    # Logout
    access_token = refreshed_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/api/v1/auth/logout", headers=headers)
    assert response.status_code == status.HTTP_200_OK

def test_login_invalid_password(client):
    login_payload = {
        "email": "authtest@circulareconomy.org",
        "password": "WrongPassword!"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_password_reset_flow(client):
    # Register target user
    client.post("/api/v1/auth/register", json={
        "email": "resetuser@circulareconomy.org",
        "password": "OldPassword123!",
        "full_name": "Reset User",
        "role": "user"
    })

    # Request reset
    response = client.post("/api/v1/auth/password-reset", json={"email": "resetuser@circulareconomy.org"})
    assert response.status_code == status.HTTP_200_OK
    res_json = response.json()
    assert "simulated_reset_token" in res_json
    reset_token = res_json["simulated_reset_token"]

    # Confirm reset
    confirm_payload = {
        "token": reset_token,
        "new_password": "NewSecretPassword123!"
    }
    response = client.post("/api/v1/auth/password-reset/confirm", json=confirm_payload)
    assert response.status_code == status.HTTP_200_OK

    # Login with new password
    response = client.post("/api/v1/auth/login", json={
        "email": "resetuser@circulareconomy.org",
        "password": "NewSecretPassword123!"
    })
    assert response.status_code == status.HTTP_200_OK


def test_email_verification(client):
    response = client.get("/api/v1/auth/verify-email?token=test_token_sample")
    assert response.status_code == status.HTTP_200_OK
