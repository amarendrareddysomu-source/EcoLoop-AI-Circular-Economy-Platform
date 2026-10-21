import io
import pytest
from PIL import Image
from ai_engine.image_classifier import image_classifier, STAGE_1_BROAD_CATEGORIES
from ai_engine.continuous_learning import continuous_learning_store

def test_two_stage_broad_category_grouping():
    assert "Electronics" in STAGE_1_BROAD_CATEGORIES or "Batteries" in STAGE_1_BROAD_CATEGORIES
    assert "Battery AA" in STAGE_1_BROAD_CATEGORIES.get("Electronics", []) or "Battery AA" in STAGE_1_BROAD_CATEGORIES.get("Batteries", [])
    assert "Plastics" in STAGE_1_BROAD_CATEGORIES
    assert "Plastic Cover" in STAGE_1_BROAD_CATEGORIES["Plastics"]

def test_secondary_verification_phone_vs_mouse():
    # Elongated image (aspect ratio 2.0) should select Phone over Mouse
    img = Image.new("RGB", (150, 300), color=(50, 50, 50))
    cat, prob = image_classifier._secondary_verification_classifier(
        img, "Mouse", "Phone", 0.42, 0.40
    )
    assert cat == "Phone"
    assert prob > 0.42

def test_secondary_verification_battery_vs_envelope():
    img = Image.new("RGB", (100, 250), color=(180, 180, 180))
    cat, prob = image_classifier._secondary_verification_classifier(
        img, "Envelope", "Battery AA", 0.44, 0.42
    )
    assert cat == "Battery AA"
    assert prob > 0.44

def test_secondary_verification_laptop_vs_keyboard():
    img = Image.new("RGB", (300, 260), color=(100, 100, 100))
    cat, prob = image_classifier._secondary_verification_classifier(
        img, "Keyboard", "Laptop", 0.45, 0.43
    )
    assert cat == "Laptop"
    assert prob > 0.45

def test_continuous_learning_store_record():
    res = continuous_learning_store.record_correction(
        image_bytes=b"dummy_image_data_test",
        predicted_label="Mouse",
        user_correct_label="Phone",
        confidence=0.68
    )
    assert res["predicted_label"] == "Mouse"
    assert res["user_correct_label"] == "Phone"

    summary = continuous_learning_store.get_hard_negatives_summary()
    assert summary["total_corrections_recorded"] >= 1
