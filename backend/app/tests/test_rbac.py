from fastapi import status

def get_auth_token(client, email, password, role="user"):
    client.post("/api/v1/auth/register", json={
        "email": email,
        "password": password,
        "full_name": f"{role.capitalize()} User",
        "role": role
    })
    res = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    return res.json()["access_token"]

def test_rbac_admin_endpoint(client):
    user_token = get_auth_token(client, "regular_user@test.org", "Pass123!", "user")
    admin_token = get_auth_token(client, "admin_user@test.org", "Pass123!", "admin")

    # Regular user accessing admin stats -> 403
    res = client.get("/api/v1/admin/stats", headers={"Authorization": f"Bearer {user_token}"})
    assert res.status_code == status.HTTP_403_FORBIDDEN

    # Admin accessing admin stats -> 200
    res = client.get("/api/v1/admin/stats", headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == status.HTTP_200_OK

def test_rbac_ngo_endpoint(client):
    user_token = get_auth_token(client, "user_for_ngo@test.org", "Pass123!", "user")
    ngo_token = get_auth_token(client, "ngo_official@test.org", "Pass123!", "ngo")

    # Regular user accessing NGO donations feed -> 403
    res = client.get("/api/v1/ngo/donations/available", headers={"Authorization": f"Bearer {user_token}"})
    assert res.status_code == status.HTTP_403_FORBIDDEN

    # NGO accessing NGO donations feed -> 200
    res = client.get("/api/v1/ngo/donations/available", headers={"Authorization": f"Bearer {ngo_token}"})
    assert res.status_code == status.HTTP_200_OK

def test_rbac_recycling_endpoint(client):
    user_token = get_auth_token(client, "user_for_recycling@test.org", "Pass123!", "user")
    recycler_token = get_auth_token(client, "recycler_official@test.org", "Pass123!", "recycling_center")

    # Regular user accessing Recycling items feed -> 403
    res = client.get("/api/v1/recycling/items/available", headers={"Authorization": f"Bearer {user_token}"})
    assert res.status_code == status.HTTP_403_FORBIDDEN

    # Recycler accessing Recycling items feed -> 200
    res = client.get("/api/v1/recycling/items/available", headers={"Authorization": f"Bearer {recycler_token}"})
    assert res.status_code == status.HTTP_200_OK
