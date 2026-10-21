"""
Pydantic Schemas for Machine Learning Algorithms API Router
File: backend/app/schemas/ml_models.py
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

# 1. Random Forest Schemas
class RandomForestRequest(BaseModel):
    category: str = Field(default="Electronics", json_schema_extra={"example": "Electronics"})
    original_price: float = Field(default=350.0, json_schema_extra={"example": 350.0})
    age_years: float = Field(default=1.5, json_schema_extra={"example": 1.5})
    condition: str = Field(default="Good", json_schema_extra={"example": "Good"})
    weight_kg: float = Field(default=2.5, json_schema_extra={"example": 2.5})

class RandomForestResponse(BaseModel):
    algorithm_name: str
    model_type: str
    predicted_category: str
    classification_confidence: float
    predicted_resale_price: float
    feature_importances: Dict[str, float]
    trees_count: int
    decision_node_split_criterion: str

# 2. SVM Schemas
class SVMRequest(BaseModel):
    age_years: float = Field(default=2.0, json_schema_extra={"example": 2.0})
    condition_score: float = Field(default=75.0, json_schema_extra={"example": 75.0})
    original_price: float = Field(default=500.0, json_schema_extra={"example": 500.0})

class SVMResponse(BaseModel):
    algorithm_name: str
    kernel: str
    hyperplane_regularization_C: float
    gamma_parameter: str
    predicted_circular_pathway: str
    pathway_confidence: float
    predicted_asset_value: float
    support_vectors_count: int
    decision_function_margin: float

# 3. Gradient Boosting Schemas
class GradientBoostingRequest(BaseModel):
    age_years: float = Field(default=1.5, json_schema_extra={"example": 1.5})
    wear_index: float = Field(default=0.20, json_schema_extra={"example": 0.20})
    base_co2_factor: float = Field(default=35.0, json_schema_extra={"example": 35.0})

class GradientBoostingResponse(BaseModel):
    algorithm_name: str
    boosting_stages_estimators: int
    learning_rate_eta: float
    tree_max_depth: int
    predicted_co2_offset_kg: float
    predicted_impact_category: str
    classification_confidence: float
    feature_importances: Dict[str, float]
    final_stage_loss_deviance: float

# 4. K-Nearest Neighbors Schemas
class KNNRequest(BaseModel):
    weight_kg: float = Field(default=3.5, json_schema_extra={"example": 3.5})
    volume_m3: float = Field(default=0.04, json_schema_extra={"example": 0.04})
    repairability_score: float = Field(default=80.0, json_schema_extra={"example": 80.0})
    eco_points: float = Field(default=85.0, json_schema_extra={"example": 85.0})
    k_neighbors: Optional[int] = Field(default=5, json_schema_extra={"example": 5})

class KNNResponse(BaseModel):
    algorithm_name: str
    k_neighbors_count: int
    distance_metric: str
    predicted_category_cluster: str
    nearest_neighbors: List[Dict[str, Any]]
    closest_neighbor_distance: float

# 5. MLP Neural Network Schemas
class MLPRequest(BaseModel):
    weight_kg: float = Field(default=4.0, json_schema_extra={"example": 4.0})
    age_years: float = Field(default=2.0, json_schema_extra={"example": 2.0})
    condition_score: float = Field(default=85.0, json_schema_extra={"example": 85.0})
    original_price: float = Field(default=450.0, json_schema_extra={"example": 450.0})

class MLPResponse(BaseModel):
    algorithm_name: str
    neural_network_architecture: Dict[str, Any]
    predicted_item_archetype: str
    classification_probability: float
    predicted_sustainability_index: float
    neural_network_iterations_to_converge: int
