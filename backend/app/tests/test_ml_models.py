"""
PyTest Suite for Machine Learning Models Suite
File: backend/app/tests/test_ml_models.py
Tests 100% of all 5 Machine Learning & AI algorithms & FastAPI API endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from ai_engine.ml_models import (
    random_forest_algorithm,
    svm_algorithm,
    gradient_boosting_algorithm,
    knn_algorithm,
    mlp_neural_network_algorithm
)

client = TestClient(app)

# -----------------------------------------------------------------------------
# 1. ML Model 1: Random Forest Classifier & Regressor
# -----------------------------------------------------------------------------
def test_random_forest_unit():
    res = random_forest_algorithm.predict_item(
        category="Electronics",
        original_price=500.0,
        age_years=1.5,
        condition="Good",
        weight_kg=3.0
    )
    assert res["predicted_category"] is not None
    assert res["classification_confidence"] > 0.0
    assert res["predicted_resale_price"] > 0.0
    assert "feature_importances" in res

def test_random_forest_api():
    payload = {
        "category": "Electronics",
        "original_price": 400.0,
        "age_years": 1.0,
        "condition": "Excellent",
        "weight_kg": 2.0
    }
    response = client.post("/api/v1/ml-models/random-forest", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["trees_count"] == 50
    assert data["predicted_resale_price"] > 0.0

# -----------------------------------------------------------------------------
# 2. ML Model 2: Support Vector Machine (SVM)
# -----------------------------------------------------------------------------
def test_svm_unit():
    res = svm_algorithm.predict(
        age_years=2.0,
        condition_score=80.0,
        original_price=600.0
    )
    assert res["kernel"] == "Radial Basis Function (RBF)"
    assert res["predicted_circular_pathway"] in ["Recycle", "Reuse / Sell", "Repair / Donate"]
    assert res["support_vectors_count"] > 0

def test_svm_api():
    payload = {
        "age_years": 1.5,
        "condition_score": 85.0,
        "original_price": 450.0
    }
    response = client.post("/api/v1/ml-models/svm", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["pathway_confidence"] > 0.0
    assert data["predicted_asset_value"] >= 0.0

# -----------------------------------------------------------------------------
# 3. ML Model 3: Gradient Boosting Machine (GBM / XGBoost)
# -----------------------------------------------------------------------------
def test_gradient_boosting_unit():
    res = gradient_boosting_algorithm.predict(
        age_years=2.0,
        wear_index=0.15,
        base_co2_factor=30.0
    )
    assert res["boosting_stages_estimators"] == 60
    assert res["predicted_co2_offset_kg"] > 0.0
    assert "feature_importances" in res

def test_gradient_boosting_api():
    payload = {
        "age_years": 1.0,
        "wear_index": 0.10,
        "base_co2_factor": 40.0
    }
    response = client.post("/api/v1/ml-models/gradient-boosting", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["learning_rate_eta"] == 0.1
    assert data["classification_confidence"] > 0.0

# -----------------------------------------------------------------------------
# 4. ML Model 4: K-Nearest Neighbors (k-NN)
# -----------------------------------------------------------------------------
def test_knn_unit():
    res = knn_algorithm.find_k_nearest(
        weight_kg=4.0,
        volume_m3=0.05,
        repairability_score=85.0,
        eco_points=90.0,
        k=5
    )
    assert res["k_neighbors_count"] == 5
    assert len(res["nearest_neighbors"]) == 5
    assert res["closest_neighbor_distance"] >= 0.0

def test_knn_api():
    payload = {
        "weight_kg": 2.0,
        "volume_m3": 0.02,
        "repairability_score": 75.0,
        "eco_points": 80.0,
        "k_neighbors": 3
    }
    response = client.post("/api/v1/ml-models/knn", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["k_neighbors_count"] == 3
    assert len(data["nearest_neighbors"]) == 3

# -----------------------------------------------------------------------------
# 5. ML Model 5: Multi-Layer Perceptron (MLP) Neural Network
# -----------------------------------------------------------------------------
def test_mlp_neural_network_unit():
    res = mlp_neural_network_algorithm.predict(
        weight_kg=5.0,
        age_years=2.0,
        condition_score=80.0,
        original_price=300.0
    )
    assert "neural_network_architecture" in res
    assert res["neural_network_architecture"]["hidden_layer_1_nodes"] == 64
    assert res["predicted_sustainability_index"] >= 0.0

def test_mlp_neural_network_api():
    payload = {
        "weight_kg": 3.0,
        "age_years": 1.0,
        "condition_score": 90.0,
        "original_price": 500.0
    }
    response = client.post("/api/v1/ml-models/mlp-neural-network", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["classification_probability"] > 0.0
    assert data["predicted_sustainability_index"] > 0.0

# -----------------------------------------------------------------------------
# 6. ML Models Suite Catalog Discovery API Test
# -----------------------------------------------------------------------------
def test_list_ml_models_api():
    response = client.get("/api/v1/ml-models/")
    assert response.status_code == 200
    data = response.json()
    assert data["implemented_ml_algorithms_count"] == 5
    assert len(data["ml_algorithms"]) == 5
