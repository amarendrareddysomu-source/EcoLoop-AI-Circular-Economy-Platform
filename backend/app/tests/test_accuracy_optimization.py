import io
import pytest
from PIL import Image
from fastapi import status
from ai_engine.image_classifier import image_classifier, SUPER_CATEGORIES

def create_test_image(format="JPEG", size=(256, 256), color=(140, 180, 220)):
    buf = io.BytesIO()
    img = Image.new("RGB", size, color=color)
    img.save(buf, format=format)
    buf.seek(0)
    return buf.getvalue()

def test_test_time_augmentation_and_ensemble():
    img_bytes = create_test_image()
    raw_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    scores = image_classifier._run_test_time_augmentation(raw_img)
    assert isinstance(scores, dict)
    assert len(scores) >= 10
    assert abs(sum(scores.values()) - 1.0) < 0.01

def test_fine_grained_disambiguator_plastic_pair():
    img = Image.new("RGB", (224, 224), color=(200, 200, 200))
    cat, prob = image_classifier._secondary_verification_classifier(
        img, "Plastic Bag", "Plastic Cover", 0.42, 0.40
    )
    assert cat in ["Plastic Cover", "Plastic Bag", "Plastic"]
    assert prob >= 0.40

def test_fine_grained_disambiguator_battery_pair():
    img = Image.new("RGB", (100, 250), color=(100, 100, 100))
    cat, prob = image_classifier._secondary_verification_classifier(
        img, "Battery AA", "Battery AAA", 0.44, 0.42
    )
    assert cat in ["Battery AA", "Battery AAA", "Battery"]
    assert prob >= 0.42

def test_hierarchical_super_category_mapping():
    assert "Plastics" in SUPER_CATEGORIES or "Electronics" in SUPER_CATEGORIES
    assert "Plastic Cover" in SUPER_CATEGORIES.get("Plastics", [])
    assert "Battery AA" in SUPER_CATEGORIES.get("Electronics", []) or "Battery AA" in SUPER_CATEGORIES.get("Batteries", [])

def test_full_accuracy_classification_api(client):
    img_bytes = create_test_image("PNG")
    files = {"image": ("accuracy_test.png", img_bytes, "image/png")}
    res = client.post("/api/v1/ai/classify-image", files=files)
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert "predicted_category" in data
    assert "top_5_predictions" in data
    assert len(data["top_5_predictions"]) == 5
    assert "model_info" in data
    assert data["model_info"]["model_version"] in ["3.5.0", "4.5.0", "5.0.0"]
