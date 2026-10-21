import io
import pytest
from PIL import Image
from fastapi import status

def create_dummy_image(format="JPEG", size=(100, 100), color=(255, 0, 0)):
    buf = io.BytesIO()
    img = Image.new("RGB", size, color=color)
    img.save(buf, format=format)
    buf.seek(0)
    return buf.getvalue()

def test_classify_image_valid(client):
    img_bytes = create_dummy_image("PNG")
    files = {
        "image": ("test_item.png", img_bytes, "image/png")
    }
    response = client.post("/api/v1/ai/classify-image", files=files)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "predicted_category" in data
    assert "confidence_score" in data
    assert "condition" in data
    assert "repairability_score" in data
    assert "sustainability_score" in data
    assert "predicted_price" in data
    assert "recommendation" in data
    assert "image_url" in data
    assert data["repairability_score"] > 0
    assert data["sustainability_score"] > 0
    assert data["predicted_price"] >= 0

def test_classify_image_invalid_extension(client):
    files = {
        "image": ("document.pdf", b"%PDF-1.4 fake pdf data", "application/pdf")
    }
    response = client.post("/api/v1/ai/classify-image", files=files)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert "detail" in data
    assert "extension" in data["detail"].lower() or "mime" in data["detail"].lower() or "invalid" in data["detail"].lower()

def test_classify_image_large_file(client):
    # 11 MB dummy file
    large_bytes = b"0" * (11 * 1024 * 1024)
    files = {
        "image": ("large_image.jpg", large_bytes, "image/jpeg")
    }
    response = client.post("/api/v1/ai/classify-image", files=files)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert "exceeds" in data["detail"].lower() or "limit" in data["detail"].lower()

def test_classify_image_corrupted(client):
    # Valid JPG header magic bytes but corrupted body content
    corrupted_bytes = b"\xff\xd8\xff\xe0" + b"corrupted payload data 12345"
    files = {
        "image": ("corrupted.jpg", corrupted_bytes, "image/jpeg")
    }
    response = client.post("/api/v1/ai/classify-image", files=files)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert "corrupted" in data["detail"].lower() or "invalid" in data["detail"].lower()

def test_inventory_integration_after_prediction(client):
    # 0. Register and login to get auth token
    email = "ai_pipe_user@circulareconomy.org"
    password = "Password123!"
    client.post("/api/v1/auth/register", json={
        "email": email,
        "password": password,
        "full_name": "AI Pipeline User",
        "role": "user"
    })
    login_res = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    token = login_res.json()["access_token"]
    auth_headers = {"Authorization": f"Bearer {token}"}

    # 1. Run AI Image Pipeline
    img_bytes = create_dummy_image("JPEG")
    files = {
        "image": ("sample_laptop.jpg", img_bytes, "image/jpeg")
    }
    classify_res = client.post("/api/v1/ai/classify-image", files=files)
    assert classify_res.status_code == status.HTTP_200_OK
    data = classify_res.json()

    # 2. Save prediction results directly to Inventory
    inventory_payload = {
        "item_name": data["predicted_category"],
        "title": data["predicted_category"],
        "category": data["predicted_category"],
        "condition": data["condition"],
        "price": data["predicted_price"],
        "image_url": data["image_url"],
        "quantity": 1,
        "unit": "pcs",
        "description": f"Saved from AI prediction pipeline. Repairability: {data['repairability_score']}"
    }
    create_res = client.post("/api/v1/inventory/", json=inventory_payload, headers=auth_headers)
    assert create_res.status_code == status.HTTP_201_CREATED
    inv_data = create_res.json()
    assert inv_data["category"] == data["predicted_category"]
    assert inv_data["condition"] == data["condition"]
    assert inv_data["price"] == data["predicted_price"]

