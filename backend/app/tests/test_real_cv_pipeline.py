import io
import pytest
from PIL import Image
from fastapi import status
from ai_engine.image_classifier import image_classifier
from ai_engine.price_predictor import price_predictor

def create_sample_image(format="JPEG", size=(224, 224), color=(100, 150, 200)):
    buf = io.BytesIO()
    img = Image.new("RGB", size, color=color)
    img.save(buf, format=format)
    buf.seek(0)
    return buf.getvalue()

def test_pytorch_cv_classifier_inference():
    img_bytes = create_sample_image()
    res = image_classifier.classify_image(img_bytes)
    assert "category" in res
    assert "confidence" in res
    assert "top_5_predictions" in res
    assert len(res["top_5_predictions"]) == 5
    assert isinstance(res["confidence"], float)
    assert 0.0 <= res["confidence"] <= 1.0
    assert "gradcam_base64" in res

def test_price_predictor_plastic_cover_zero_resale():
    price_res = price_predictor.predict_price_details("Plastic Cover", condition="Good")
    assert price_res["predicted_resale_price"] == 0.0
    assert price_res["recycling_value"] >= 0.0

def test_price_predictor_laptop_realistic_resale():
    price_res = price_predictor.predict_price_details("Laptop", condition="Good", age_years=2.0)
    assert price_res["predicted_resale_price"] > 50.0

def test_classify_image_api_full_pipeline(client):
    img_bytes = create_sample_image("PNG")
    files = {
        "image": ("plastic_cover_sample.png", img_bytes, "image/png")
    }
    res = client.post("/api/v1/ai/classify-image", files=files)
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert "predicted_category" in data
    assert "confidence_score" in data
    assert "top_5_predictions" in data
    assert len(data["top_5_predictions"]) == 5
    assert "condition" in data
    assert "visual_defects_detected" in data
    assert "repairability_score" in data
    assert "sustainability_score" in data
    assert "predicted_price" in data
    assert "recommendation" in data
    assert "gradcam_base64" in data
    assert "model_info" in data
    assert data["model_info"]["model_version"] in ["2.1.0", "3.0.0", "3.5.0", "4.5.0", "5.0.0"]

def test_inventory_persistence_from_real_cv_pipeline(client):
    # 1. Register & login
    email = "real_cv_user@circulareconomy.org"
    password = "Password123!"
    client.post("/api/v1/auth/register", json={
        "email": email,
        "password": password,
        "full_name": "CV Pipeline Tester",
        "role": "user"
    })
    login_res = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Run real PyTorch classification
    img_bytes = create_sample_image("JPEG")
    files = {
        "image": ("test_laptop.jpg", img_bytes, "image/jpeg")
    }
    cv_res = client.post("/api/v1/ai/classify-image", files=files)
    assert cv_res.status_code == status.HTTP_200_OK
    data = cv_res.json()

    # 3. Save item to inventory
    inv_payload = {
        "item_name": data["predicted_category"],
        "title": data["predicted_category"],
        "category": data["predicted_category"],
        "condition": data["condition"],
        "price": data["predicted_price"],
        "image_url": data["image_url"],
        "quantity": 1,
        "unit": "pcs",
        "description": f"Saved from PyTorch CV pipeline. Repairability: {data['repairability_score']}"
    }
    inv_res = client.post("/api/v1/inventory/", json=inv_payload, headers=headers)
    assert inv_res.status_code == status.HTTP_201_CREATED
    assert inv_res.json()["category"] == data["predicted_category"]
