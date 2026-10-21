"""
Pydantic Schemas for AI Algorithms Endpoint
File: backend/app/schemas/algorithms.py
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

# 1. AHP Algorithm Schemas
class AHPRequest(BaseModel):
    category: str = Field(default="Electronics", json_schema_extra={"example": "Electronics"})
    condition: str = Field(default="Good", json_schema_extra={"example": "Good"})
    age_years: float = Field(default=1.5, json_schema_extra={"example": 1.5})
    estimated_price: float = Field(default=120.0, json_schema_extra={"example": 120.0})
    co2_saved_kg: float = Field(default=8.5, json_schema_extra={"example": 8.5})
    repairability_score: float = Field(default=75.0, json_schema_extra={"example": 75.0})
    ngo_demand_score: float = Field(default=60.0, json_schema_extra={"example": 60.0})
    urgency_score: float = Field(default=30.0, json_schema_extra={"example": 30.0})

class AHPResponse(BaseModel):
    algorithm_name: str
    recommended_action: str
    ahp_score: float
    ranked_action_scores: Dict[str, float]
    criteria_weights: Dict[str, float]
    matrix_consistency: Dict[str, Any]

# 2. Haversine Routing Schemas
class FacilityItem(BaseModel):
    id: Optional[str] = "FAC-1"
    name: str = Field(default="Green Earth Recycling Hub")
    type: str = Field(default="Recycling Center")
    latitude: float = Field(default=12.9716)
    longitude: float = Field(default=77.5946)
    capacity_max_kg: float = Field(default=1000.0)
    capacity_current_kg: float = Field(default=250.0)
    accepted_materials: List[str] = Field(default_factory=lambda: ["electronics", "plastic", "metal"])

class HaversineRoutingRequest(BaseModel):
    user_latitude: float = Field(default=12.9352)
    user_longitude: float = Field(default=77.6245)
    item_material: str = Field(default="electronics")
    item_weight_kg: float = Field(default=5.0)
    facilities: List[FacilityItem] = Field(default_factory=list)

class HaversineRoutingResponse(BaseModel):
    algorithm_name: str
    user_coordinates: Dict[str, float]
    item_specs: Dict[str, Any]
    facilities_evaluated_count: int
    facilities_in_range_count: int
    optimal_facility: Optional[Dict[str, Any]]
    ranked_facilities: List[Dict[str, Any]]

# 3. Exponential Depreciation Schemas
class ExponentialDepreciationRequest(BaseModel):
    category: str = Field(default="Laptop")
    original_price: float = Field(default=800.0)
    age_years: float = Field(default=2.5)
    condition: str = Field(default="Good")
    wear_index: float = Field(default=0.15)
    market_demand_index: float = Field(default=0.05)

class ExponentialDepreciationResponse(BaseModel):
    algorithm_name: str
    category: str
    original_price: float
    age_years: float
    condition: str
    decay_constant_lambda: float
    exponential_decay_factor: float
    estimated_market_price: float
    scrap_material_floor: float
    depreciation_percentage: float
    valuation_confidence_range: Dict[str, float]
    formula_expression: str

# 4. Bin Packing Schemas
class PackingItem(BaseModel):
    id: str = Field(default="ITEM-101")
    category: str = Field(default="Plastic Bottle")
    weight_kg: float = Field(default=2.5)
    volume_m3: float = Field(default=0.02)

class BinPackingRequest(BaseModel):
    bin_capacity_kg: float = Field(default=50.0)
    bin_capacity_m3: float = Field(default=0.3)
    max_available_bins: int = Field(default=5)
    items: List[PackingItem] = Field(default_factory=list)

class BinPackingResponse(BaseModel):
    algorithm_name: str
    items_processed_count: int
    bins_used_count: int
    packed_bins: List[Dict[str, Any]]
    unpacked_overflow_items: List[Dict[str, Any]]
    total_packed_weight_kg: float
    space_utilization_efficiency_pct: float
