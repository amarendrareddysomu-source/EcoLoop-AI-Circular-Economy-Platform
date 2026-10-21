import io
import pytest
from PIL import Image
from fastapi import status

def create_sample_image(format="PNG", size=(200, 200), color=(100, 150, 200)):
    buf = io.BytesIO()
    img = Image.new("RGB", size, color=color)
    img.save(buf, format=format)
    buf.seek(0)
    return buf.getvalue()

def test_phase_1_vision_identify_endpoint(client):
    img_bytes = create_sample_image("PNG")
    files = {"image": ("vision_test.png", img_bytes, "image/png")}
    res = client.post("/api/v1/ai/vision-identify", files=files)
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert "detected_object" in data
    assert "primary_material" in data
    assert "product_category" in data
    assert "confidence_score" in data
    assert "top_5_predictions" in data
    assert len(data["top_5_predictions"]) >= 1

def test_phase_3_hybrid_predict_endpoint(client):
    payload = {
        "product_name": "Dell XPS 15 Laptop",
        "brand": "Dell",
        "material": "Aluminum",
        "category": "Electronics",
        "approximate_age": 2.0,
        "weight_kg": 1.8,
        "dimensions": "35 x 24 x 1.8 cm",
        "color": "Silver",
        "purchase_year": 2023,
        "original_price": 1200.0,
        "current_usage": "Moderate",
        "working_condition": "Fully Functional",
        "physical_description": "Minor chassis scuffs",
        "visible_damage": "Minor Scratches",
        "missing_parts": "None",
        "battery_included": True,
        "power_status": "Powers On",
        "accessories_included": True,
        "packaging_available": False,
        "warranty_available": False,
        "storage_capacity": "512GB SSD",
        "model_number": "XPS-9520",
        "serial_number": "DL-99812",
        "additional_notes": "Great working laptop"
    }

    res = client.post("/api/v1/ai/hybrid-predict", json=payload)
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert data["detected_object"] == "Dell XPS 15 Laptop"
    assert data["product_category"] == "Electronics"
    assert data["estimated_condition"] in ["Excellent", "Good", "Fair", "Poor"]
    assert data["repairability_score"] > 0
    assert data["predicted_resale_price"] > 0
    assert data["sustainability_score"] > 0
    assert data["recommended_action"] in ["Sell", "Repair", "Donate", "Reuse", "Recycle"]
    assert data["model_info"]["model_name"] == "Hybrid_Fusion_CV_Metadata_v4.0"
    assert data["model_info"]["metadata_fields_evaluated"] == 25

def test_phase_4_condition_fusion_laptop_cracked_screen(client):
    # Laptop with cracked screen & dead battery should evaluate to Fair/Poor condition
    payload = {
        "product_name": "Broken Screen Laptop",
        "category": "Electronics",
        "working_condition": "Partially Functional",
        "visible_damage": "Cracked Screen",
        "power_status": "Does Not Power On",
        "battery_included": False,
        "approximate_age": 4.0,
        "original_price": 900.0
    }
    res = client.post("/api/v1/ai/hybrid-predict", json=payload)
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert data["estimated_condition"] in ["Fair", "Poor", "Damaged"]

def test_phase_6_plastic_cover_non_resale_rule(client):
    # Packaging / Plastic Cover should return Resale Value: Not Applicable
    payload = {
        "product_name": "Plastic Cover Sheet",
        "category": "Plastics",
        "material": "Polyethylene",
        "approximate_age": 0.1,
        "weight_kg": 0.2,
        "original_price": 1.0,
        "working_condition": "Non-Functional"
    }
    res = client.post("/api/v1/ai/hybrid-predict", json=payload)
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert data["is_resale_applicable"] is False
    assert data["resale_value_display"] == "Not Applicable"
    assert data["recommended_action"] in ["Recycle", "Dispose Safely"]
