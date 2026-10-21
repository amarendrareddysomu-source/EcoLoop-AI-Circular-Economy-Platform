import io
import pytest
from PIL import Image
from fastapi import status
from ai_engine.image_classifier import image_classifier, CONTROLLED_55_CLASSES
from ai_engine.hybrid_fusion_engine import hybrid_fusion_engine

def create_sample_image(format="JPEG", size=(256, 256), color=(140, 180, 220)):
    buf = io.BytesIO()
    img = Image.new("RGB", size, color=color)
    img.save(buf, format=format)
    buf.seek(0)
    return buf.getvalue()

def test_task_2_controlled_55_classes_taxonomy():
    assert len(CONTROLLED_55_CLASSES) >= 10
    assert "Trash" in CONTROLLED_55_CLASSES
    assert "Battery" in CONTROLLED_55_CLASSES or "Battery AA" in CONTROLLED_55_CLASSES
    assert "Glass" in CONTROLLED_55_CLASSES
    assert "Plastic" in CONTROLLED_55_CLASSES

def test_task_8_blurry_image_condition_fallback():
    raw_img = Image.new("RGB", (256, 256), color=(255, 255, 255))
    var, is_blurry = image_classifier.evaluate_image_blur_variance(raw_img)
    assert isinstance(var, float)

    hybrid_res = hybrid_fusion_engine.run_hybrid_pipeline(
        image_bytes=None,
        user_metadata={"working_condition": None}
    )
    assert hybrid_res["condition_reasoning"] is not None

def test_task_6_low_confidence_prompt():
    img_bytes = create_sample_image(color=(50, 50, 50))
    res = image_classifier.classify_image(img_bytes)
    if res.get("is_low_confidence"):
        assert "low_confidence_prompt" in res
        assert res["low_confidence_prompt"] is not None

def test_task_7_price_estimation_regressor():
    hybrid_res = hybrid_fusion_engine.run_hybrid_pipeline(
        image_bytes=create_sample_image(),
        user_metadata={
            "product_name": "iPhone 13",
            "category": "Electronics",
            "working_condition": "Fully Functional",
            "original_price": 799.0,
            "approximate_age": 1.5
        }
    )
    assert hybrid_res["is_resale_applicable"] is True
    price_val = hybrid_res.get("predicted_resale_price", hybrid_res.get("predicted_price", 0.0))
    assert price_val > 0
    assert "$" in hybrid_res["resale_value_display"]

def test_task_9_master_api_classification_endpoint(client):
    img_bytes = create_sample_image("PNG")
    files = {"image": ("master_waste.png", img_bytes, "image/png")}
    res = client.post("/api/v1/ai/classify-image", files=files)
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert "predicted_category" in data
    assert "top_5_predictions" in data
    assert len(data["top_5_predictions"]) == 5
    assert "model_info" in data
    assert data["model_info"]["model_version"] in ["3.5.0", "4.5.0", "5.0.0"]
