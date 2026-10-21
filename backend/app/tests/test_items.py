from fastapi import status

def get_auth_token(client, email="itemuser@circulareconomy.org", role="user"):
    client.post("/api/v1/auth/register", json={
        "email": email,
        "password": "Password123!",
        "full_name": "Item User",
        "role": role
    })
    res = client.post("/api/v1/auth/login", json={"email": email, "password": "Password123!"})
    return res.json()["access_token"]

def test_create_and_list_item(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    item_payload = {
        "title": "Vintage Oak Coffee Table",
        "description": "Solid oak table in great shape.",
        "category": "Furniture",
        "brand": "IKEA",
        "age_years": 3.0,
        "usage_level": "Moderate",
        "condition": "Good",
        "original_price": 250.0,
        "location": "Downtown"
    }

    response = client.post("/api/v1/items/", json=item_payload, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Vintage Oak Coffee Table"
    assert data["category"] == "Furniture"
    assert data["recommended_action"] in ["Repair", "Reuse", "Donate", "Sell", "Recycle"]
    assert data["co2_saved_kg"] > 0

    list_res = client.get("/api/v1/items/")
    assert list_res.status_code == status.HTTP_200_OK
    assert len(list_res.json()) >= 1
