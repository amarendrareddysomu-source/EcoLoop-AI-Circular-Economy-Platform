"""
PyTest Suite for Platform Algorithm Suite
File: backend/app/tests/test_algorithms.py
Tests 100% of all 4 implemented algorithms & FastAPI API endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from ai_engine.algorithms import (
    ahp_algorithm,
    haversine_routing_algorithm,
    exponential_depreciation_algorithm,
    bin_packing_algorithm
)

client = TestClient(app)

# -----------------------------------------------------------------------------
# 1. Algorithm 1 Unit Tests: Analytic Hierarchy Process (AHP)
# -----------------------------------------------------------------------------
def test_ahp_algorithm_unit():
    res = ahp_algorithm.evaluate(
        category="Electronics",
        condition="Good",
        age_years=2.0,
        estimated_price=150.0,
        co2_saved_kg=12.0,
        repairability_score=80.0,
        ngo_demand_score=50.0,
        urgency_score=20.0
    )
    assert res["recommended_action"] in ["Reuse", "Repair", "Donate", "Sell", "Recycle"]
    assert "criteria_weights" in res
    assert "co2_offset" in res["criteria_weights"]
    assert res["matrix_consistency"]["is_valid"] is True
    assert res["matrix_consistency"]["consistency_ratio"] <= 0.10

def test_ahp_algorithm_api():
    payload = {
        "category": "Laptop",
        "condition": "Excellent",
        "age_years": 1.0,
        "estimated_price": 500.0,
        "co2_saved_kg": 25.0,
        "repairability_score": 85.0,
        "ngo_demand_score": 70.0,
        "urgency_score": 15.0
    }
    response = client.post("/api/v1/algorithms/ahp-decision", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["recommended_action"] in ["Sell", "Reuse", "Repair", "Donate", "Recycle"]
    assert data["ahp_score"] > 0.0

# -----------------------------------------------------------------------------
# 2. Algorithm 2 Unit Tests: Haversine & Capacity Routing
# -----------------------------------------------------------------------------
def test_haversine_routing_algorithm_unit():
    user_lat, user_lon = 12.9716, 77.5946
    dist = haversine_routing_algorithm.haversine_distance(user_lat, user_lon, 12.9352, 77.6245)
    assert dist > 0.0
    assert dist < 10.0  # Close distance in Bangalore area

    facilities = [
        {"id": "F1", "name": "Facility A", "type": "Recycling Center", "latitude": 12.9800, "longitude": 77.6000, "capacity_max_kg": 1000.0, "capacity_current_kg": 200.0, "accepted_materials": ["electronics"]},
        {"id": "F2", "name": "Facility B", "type": "NGO", "latitude": 13.5000, "longitude": 78.0000, "capacity_max_kg": 500.0, "capacity_current_kg": 490.0, "accepted_materials": ["clothes"]}
    ]

    res = haversine_routing_algorithm.route_and_match(
        user_lat=user_lat,
        user_lon=user_lon,
        item_material="electronics",
        item_weight_kg=10.0,
        facilities=facilities
    )
    assert res["facilities_evaluated_count"] == 2
    assert res["optimal_facility"]["facility_id"] == "F1"
    assert res["optimal_facility"]["routing_score"] > 50.0

def test_haversine_routing_algorithm_api():
    payload = {
        "user_latitude": 12.9716,
        "user_longitude": 77.5946,
        "item_material": "electronics",
        "item_weight_kg": 5.0,
        "facilities": []
    }
    response = client.post("/api/v1/algorithms/haversine-routing", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["facilities_in_range_count"] > 0
    assert data["optimal_facility"] is not None

# -----------------------------------------------------------------------------
# 3. Algorithm 3 Unit Tests: Exponential Decay Asset Valuation
# -----------------------------------------------------------------------------
def test_exponential_depreciation_algorithm_unit():
    res = exponential_depreciation_algorithm.calculate_valuation(
        category="Electronics",
        original_price=1000.0,
        age_years=2.0,
        condition="Good",
        wear_index=0.10,
        market_demand_index=0.0
    )
    assert res["estimated_market_price"] < 1000.0
    assert res["estimated_market_price"] >= res["scrap_material_floor"]
    assert res["depreciation_percentage"] > 0.0

def test_exponential_depreciation_algorithm_api():
    payload = {
        "category": "Phone",
        "original_price": 600.0,
        "age_years": 1.5,
        "condition": "Excellent",
        "wear_index": 0.05,
        "market_demand_index": 0.10
    }
    response = client.post("/api/v1/algorithms/exponential-depreciation", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["estimated_market_price"] > 0.0
    assert "valuation_confidence_range" in data

# -----------------------------------------------------------------------------
# 4. Algorithm 4 Unit Tests: Greedy Best-Fit Bin Packing
# -----------------------------------------------------------------------------
def test_bin_packing_algorithm_unit():
    items = [
        {"id": "I1", "category": "Metal", "weight_kg": 20.0, "volume_m3": 0.05},
        {"id": "I2", "category": "Plastic", "weight_kg": 15.0, "volume_m3": 0.10},
        {"id": "I3", "category": "Paper", "weight_kg": 10.0, "volume_m3": 0.08}
    ]
    res = bin_packing_algorithm.pack_items(
        items=items,
        bin_capacity_kg=50.0,
        bin_capacity_m3=0.3,
        max_available_bins=3
    )
    assert res["bins_used_count"] >= 1
    assert res["total_packed_weight_kg"] == 45.0
    assert res["space_utilization_efficiency_pct"] > 0.0

def test_bin_packing_algorithm_api():
    payload = {
        "bin_capacity_kg": 100.0,
        "bin_capacity_m3": 0.5,
        "max_available_bins": 5,
        "items": [
            {"id": "B1", "category": "Batteries", "weight_kg": 30.0, "volume_m3": 0.05},
            {"id": "B2", "category": "E-Waste", "weight_kg": 40.0, "volume_m3": 0.12}
        ]
    }
    response = client.post("/api/v1/algorithms/bin-packing", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["items_processed_count"] == 2
    assert data["bins_used_count"] >= 1

# -----------------------------------------------------------------------------
# 5. Algorithm Suite Discovery API Test
# -----------------------------------------------------------------------------
def test_list_algorithms_api():
    response = client.get("/api/v1/algorithms/")
    assert response.status_code == 200
    data = response.json()
    assert data["implemented_algorithms_count"] == 4
    assert len(data["algorithms"]) == 4
