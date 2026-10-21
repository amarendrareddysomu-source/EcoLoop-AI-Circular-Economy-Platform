import pytest
from fastapi import status

def test_predict_price_api(client):
    payload = {
        "category": "Electronics",
        "brand": "Apple",
        "age_years": 2.0,
        "condition": "Good",
        "original_price": 1000.0,
        "market_factors": {"demand_level": "high"}
    }
    res = client.post("/api/v1/ai/predict-price", json=payload)
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert data["predicted_resale_price"] > 0
    assert data["confidence"] > 0
    assert data["min_price"] <= data["predicted_resale_price"] <= data["max_price"]

def test_predict_condition_api(client):
    payload = {
        "age_years": 0.5,
        "usage_level": "Low",
        "user_stated_condition": "Excellent",
        "description": "Mint condition smartphone"
    }
    res = client.post("/api/v1/ai/predict-condition", json=payload)
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert data["predicted_condition"] in ["Excellent", "Good", "Fair", "Poor", "New", "Used"]
    assert data["confidence"] > 0

def test_sustainability_score_api(client):
    payload = {
        "category": "Furniture",
        "material": "wood",
        "condition": "Excellent",
        "weight_kg": 15.5,
        "reuse_potential": "High",
        "description": "Solid teak dining table"
    }
    res = client.post("/api/v1/ai/sustainability-score", json=payload)
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert 0.0 <= data["sustainability_score"] <= 100.0
    assert data["environmental_impact_category"] in ["Exceptional", "High Impact", "Medium Impact", "Low Impact"]
    assert len(data["recommendation"]) > 5

def test_recommendation_api(client):
    payload = {
        "category": "Electronics",
        "condition": "Fair",
        "age_years": 3.0,
        "estimated_price": 150.0,
        "location": "Downtown Metro"
    }
    res = client.post("/api/v1/ai/recommend", json=payload)
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert data["recommended_action"] in ["Reuse", "Repair", "Donate", "Sell", "Recycle"]
    assert len(data["reuse_options"]) >= 1
    assert len(data["recycling_methods"]) >= 1
    assert len(data["suitable_buyers_ngos"]) >= 1
    assert len(data["sustainability_actions"]) >= 1

def test_ai_invalid_input_handling(client):
    # Invalid negative age
    res1 = client.post("/api/v1/ai/predict-price", json={"category": "Electronics", "age_years": -3.0})
    assert res1.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Invalid negative weight
    res2 = client.post("/api/v1/ai/sustainability-score", json={"category": "Plastic", "weight_kg": -10.0})
    assert res2.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Invalid empty category string
    res3 = client.post("/api/v1/ai/recommend", json={"category": ""})
    assert res3.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
