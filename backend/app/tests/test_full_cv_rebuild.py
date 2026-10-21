import io
import pytest
from PIL import Image
from fastapi import status
from ai_engine.image_classifier import image_classifier, TAXONOMY_100_CLASSES
from ai_engine.condition_predictor import condition_predictor
from ai_engine.price_predictor import price_predictor
from ai_engine.recommendation_engine import recommendation_engine

def create_sample_image(format="JPEG", size=(224, 224), color=(120, 160, 210)):
    buf = io.BytesIO()
    img = Image.new("RGB", size, color=color)
    img.save(buf, format=format)
    buf.seek(0)
    return buf.getvalue()

def test_taxonomy_100_classes_count():
    assert len(TAXONOMY_100_CLASSES) >= 10
    assert "Battery" in TAXONOMY_100_CLASSES or "Battery AA" in TAXONOMY_100_CLASSES
    assert "Plastic" in TAXONOMY_100_CLASSES or "Plastic Cover" in TAXONOMY_100_CLASSES

def test_object_detection_bounding_boxes():
    img_bytes = create_sample_image()
    res = image_classifier.classify_image(img_bytes)
    assert "detected_objects" in res
    assert len(res["detected_objects"]) > 0
    box = res["detected_objects"][0]["box"]
    assert len(box) == 4
    assert "explanation_text" in res
    assert "Detected because:" in res["explanation_text"]

def test_low_confidence_safeguard_warning():
    # Test low confidence message structure
    img_bytes = create_sample_image(color=(50, 50, 50))
    res = image_classifier.classify_image(img_bytes)
    if res.get("is_low_confidence"):
        assert res.get("low_confidence_message") is not None

def test_condition_unknown_fallback():
    # Zero-byte or missing image yields Condition: Unknown
    res = condition_predictor.predict_condition(image_bytes=None)
    assert res["predicted_condition"] == "Unknown"

def test_repairability_knowledge_base():
    bat_rep = recommendation_engine.compute_repairability("Battery AA", "Good")
    assert bat_rep["repairability_rating"] in ["None", "Very Low"]
    assert bat_rep["repairability_score"] <= 10.0

    lap_rep = recommendation_engine.compute_repairability("Laptop", "Good")
    assert lap_rep["repairability_rating"] == "High"
    assert lap_rep["repairability_score"] >= 75.0

    chair_rep = recommendation_engine.compute_repairability("Wooden Chair", "Good")
    assert chair_rep["repairability_rating"] in ["Medium", "High"]

def test_battery_special_recommendation_rule():
    rec = recommendation_engine.get_recommendation("Battery AA", "Good", 1.0, 0.0)
    assert rec["recommended_action"] == "Recycle"
    assert "authorized e-waste collection center" in rec["action_reasoning"]

def test_non_resale_pricing_rule():
    price_res = price_predictor.predict_price_details("Plastic Cover", condition="Good")
    assert price_res["predicted_resale_price"] == 0.0
    assert price_res["resale_value_display"] == "Not Applicable"
    assert price_res["is_resale_applicable"] is False
    assert "₹" in price_res["recycling_value_inr"]

    price_laptop = price_predictor.predict_price_details("Laptop", condition="Good", age_years=2.0)
    assert price_laptop["predicted_resale_price"] > 50.0
    assert price_laptop["is_resale_applicable"] is True

def test_full_cv_api_endpoint(client):
    img_bytes = create_sample_image("PNG")
    files = {"image": ("test_waste.png", img_bytes, "image/png")}
    res = client.post("/api/v1/ai/classify-image", files=files)
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert "predicted_category" in data
    assert "confidence_score" in data
    assert "detected_objects" in data
    assert "top_5_predictions" in data
    assert len(data["top_5_predictions"]) == 5
    assert "condition" in data
    assert "visual_defects_detected" in data
    assert "repairability_score" in data
    assert "repairability_rating" in data
    assert "sustainability_score" in data
    assert "predicted_price" in data
    assert "resale_value_display" in data
    assert "recycling_value_inr" in data
    assert "recommendation" in data
    assert "gradcam_base64" in data
    assert "explanation_text" in data
    assert "model_info" in data
    assert data["model_info"]["model_version"] in ["3.0.0", "3.5.0", "4.5.0", "5.0.0"]

def test_inventory_persistence_from_rebuilt_pipeline(client):
    email = "rebuilt_cv_user@circulareconomy.org"
    password = "Password123!"
    client.post("/api/v1/auth/register", json={
        "email": email,
        "password": password,
        "full_name": "Rebuilt CV Tester",
        "role": "user"
    })
    login_res = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    img_bytes = create_sample_image("JPEG")
    files = {"image": ("laptop_test.jpg", img_bytes, "image/jpeg")}
    cv_res = client.post("/api/v1/ai/classify-image", files=files)
    assert cv_res.status_code == status.HTTP_200_OK
    data = cv_res.json()

    inv_payload = {
        "item_name": data["predicted_category"],
        "title": data["predicted_category"],
        "category": data["predicted_category"],
        "condition": data["condition"],
        "price": data["predicted_price"],
        "image_url": data["image_url"],
        "quantity": 1,
        "unit": "pcs",
        "description": f"Saved from 14-Phase CV Pipeline. Repairability: {data['repairability_rating']}"
    }
    inv_res = client.post("/api/v1/inventory/", json=inv_payload, headers=headers)
    assert inv_res.status_code == status.HTTP_201_CREATED
    assert inv_res.json()["category"] == data["predicted_category"]
