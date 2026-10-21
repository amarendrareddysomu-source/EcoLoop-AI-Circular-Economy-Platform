"""
FastAPI Router for Platform Algorithm Suite
File: backend/app/api/v1/endpoints/algorithms.py
"""

from typing import Dict, Any, List
from fastapi import APIRouter, status

from ai_engine.algorithms import (
    ahp_algorithm,
    haversine_routing_algorithm,
    exponential_depreciation_algorithm,
    bin_packing_algorithm
)
from app.schemas.algorithms import (
    AHPRequest, AHPResponse,
    HaversineRoutingRequest, HaversineRoutingResponse,
    ExponentialDepreciationRequest, ExponentialDepreciationResponse,
    BinPackingRequest, BinPackingResponse
)

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
def list_algorithms() -> Dict[str, Any]:
    """
    Returns metadata and list of all implemented algorithms in the platform.
    """
    return {
        "platform": "AI-Powered Circular Economy Platform",
        "implemented_algorithms_count": 4,
        "algorithms": [
            {
                "id": "ahp_circular_decision",
                "name": "Analytic Hierarchy Process (AHP) Circular Priority Matrix Algorithm",
                "type": "Multi-Criteria Decision Analysis (MCDM)",
                "endpoint": "/api/v1/algorithms/ahp-decision"
            },
            {
                "id": "haversine_routing",
                "name": "Haversine & Capacity Weighted Optimal Logistics Routing Algorithm",
                "type": "Geographic Logistics & Pareto Optimization",
                "endpoint": "/api/v1/algorithms/haversine-routing"
            },
            {
                "id": "exponential_depreciation",
                "name": "Exponential Decay Asset Market Valuation & Depreciation Algorithm",
                "type": "Non-Linear Asset Valuation & Material Scrap Floor",
                "endpoint": "/api/v1/algorithms/exponential-depreciation"
            },
            {
                "id": "bin_packing_optimizer",
                "name": "Greedy Best-Fit Decreasing (BFD) Waste Bin-Packing Algorithm",
                "type": "Combinatorial Multi-Constraint Bin Packing",
                "endpoint": "/api/v1/algorithms/bin-packing"
            }
        ]
    }

@router.post("/ahp-decision", response_model=AHPResponse, status_code=status.HTTP_200_OK)
def run_ahp_decision_algorithm(req: AHPRequest) -> AHPResponse:
    """
    Executes Algorithm 1: Analytic Hierarchy Process (AHP) Circular Priority Matrix Algorithm.
    """
    res = ahp_algorithm.evaluate(
        category=req.category,
        condition=req.condition,
        age_years=req.age_years,
        estimated_price=req.estimated_price,
        co2_saved_kg=req.co2_saved_kg,
        repairability_score=req.repairability_score,
        ngo_demand_score=req.ngo_demand_score,
        urgency_score=req.urgency_score
    )
    return AHPResponse(**res)

@router.post("/haversine-routing", response_model=HaversineRoutingResponse, status_code=status.HTTP_200_OK)
def run_haversine_routing_algorithm(req: HaversineRoutingRequest) -> HaversineRoutingResponse:
    """
    Executes Algorithm 2: Haversine & Capacity Weighted Optimal Logistics Routing Algorithm.
    """
    facilities_list = [f.model_dump() for f in req.facilities]
    if not facilities_list:
        # Default mock facilities if empty list passed
        facilities_list = [
            {"id": "FAC-01", "name": "Green Earth Recycling Hub", "type": "Recycling Center", "latitude": 12.9716, "longitude": 77.5946, "capacity_max_kg": 2000.0, "capacity_current_kg": 400.0, "accepted_materials": ["electronics", "plastic"]},
            {"id": "FAC-02", "name": "Hope Community NGO Shelter", "type": "NGO", "latitude": 12.9400, "longitude": 77.6100, "capacity_max_kg": 1500.0, "capacity_current_kg": 300.0, "accepted_materials": ["clothes", "furniture", "electronics"]},
            {"id": "FAC-03", "name": "Metropolitan E-Waste Depot", "type": "Recycling Center", "latitude": 13.0100, "longitude": 77.5500, "capacity_max_kg": 5000.0, "capacity_current_kg": 4500.0, "accepted_materials": ["electronics", "metal"]}
        ]

    res = haversine_routing_algorithm.route_and_match(
        user_lat=req.user_latitude,
        user_lon=req.user_longitude,
        item_material=req.item_material,
        item_weight_kg=req.item_weight_kg,
        facilities=facilities_list
    )
    return HaversineRoutingResponse(**res)

@router.post("/exponential-depreciation", response_model=ExponentialDepreciationResponse, status_code=status.HTTP_200_OK)
def run_exponential_depreciation_algorithm(req: ExponentialDepreciationRequest) -> ExponentialDepreciationResponse:
    """
    Executes Algorithm 3: Exponential Decay Asset Market Valuation & Depreciation Algorithm.
    """
    res = exponential_depreciation_algorithm.calculate_valuation(
        category=req.category,
        original_price=req.original_price,
        age_years=req.age_years,
        condition=req.condition,
        wear_index=req.wear_index,
        market_demand_index=req.market_demand_index
    )
    return ExponentialDepreciationResponse(**res)

@router.post("/bin-packing", response_model=BinPackingResponse, status_code=status.HTTP_200_OK)
def run_bin_packing_algorithm(req: BinPackingRequest) -> BinPackingResponse:
    """
    Executes Algorithm 4: Greedy Best-Fit Decreasing (BFD) Waste Bin-Packing Algorithm.
    """
    items_list = [i.model_dump() for i in req.items]
    if not items_list:
        # Default mock items batch if empty list passed
        items_list = [
            {"id": "ITEM-1", "category": "Plastic Bottles", "weight_kg": 12.0, "volume_m3": 0.10},
            {"id": "ITEM-2", "category": "Cardboard Sheets", "weight_kg": 8.5, "volume_m3": 0.15},
            {"id": "ITEM-3", "category": "Scrap Metal", "weight_kg": 25.0, "volume_m3": 0.05},
            {"id": "ITEM-4", "category": "E-Waste Batteries", "weight_kg": 15.0, "volume_m3": 0.04},
            {"id": "ITEM-5", "category": "Glass Containers", "weight_kg": 18.0, "volume_m3": 0.08}
        ]

    res = bin_packing_algorithm.pack_items(
        items=items_list,
        bin_capacity_kg=req.bin_capacity_kg,
        bin_capacity_m3=req.bin_capacity_m3,
        max_available_bins=req.max_available_bins
    )
    return BinPackingResponse(**res)
