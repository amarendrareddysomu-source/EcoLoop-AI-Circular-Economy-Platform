from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List

class ImageAnalysisRequest(BaseModel):
    image_url: Optional[str] = None
    age_years: float = 1.0
    usage_level: str = "Moderate"
    original_price: float = 100.0
    category: Optional[str] = None

class AIAnalysisResult(BaseModel):
    classified_category: str
    category_confidence: float
    predicted_condition: str
    condition_confidence: float
    recommended_action: str
    action_reasoning: str
    estimated_resale_price: float
    co2_saved_kg: float
    waste_diverted_kg: float
    environmental_impact_points: float

class AILogResponse(BaseModel):
    id: int
    module_name: str
    model_version: str
    execution_time_ms: float
    confidence_score: Optional[float]
    status: str
    created_at: Any

    model_config = ConfigDict(from_attributes=True)

# --- Phase 7 ML Schemas ---

class AISustainabilityRequest(BaseModel):
    category: str = Field(..., min_length=2)
    material: Optional[str] = Field("plastic", min_length=2)
    condition: Optional[str] = "Good"
    weight_kg: float = Field(1.0, ge=0.0, description="Weight in kg must be non-negative")
    reuse_potential: Optional[str] = "High"
    description: Optional[str] = None

class AISustainabilityResponse(BaseModel):
    sustainability_score: float
    environmental_impact_category: str
    recommendation: str

class PricePredictionRequest(BaseModel):
    category: str = Field(..., min_length=2)
    brand: Optional[str] = "Generic"
    age_years: float = Field(1.0, ge=0.0, description="Age must be non-negative")
    condition: str = Field("Good", min_length=2)
    original_price: float = Field(100.0, ge=0.0, description="Original price must be non-negative")
    market_factors: Optional[Dict[str, Any]] = None

class PricePredictionResponse(BaseModel):
    predicted_resale_price: float
    resale_value_display: Optional[str] = "Not Applicable"
    is_resale_applicable: Optional[bool] = False
    recycling_value_inr: Optional[str] = "₹0"
    recycling_value_usd: Optional[str] = "$0.00"
    confidence: float = 0.92
    min_price: float = 0.0
    max_price: float = 0.0


class ConditionPredictionRequest(BaseModel):
    age_years: float = Field(1.0, ge=0.0, description="Age must be non-negative")
    usage_level: Optional[str] = "Moderate"
    user_stated_condition: Optional[str] = None
    description: Optional[str] = None

class ConditionPredictionResponse(BaseModel):
    predicted_condition: str
    confidence: float

class RecommendationRequest(BaseModel):
    category: str = Field(..., min_length=2)
    condition: Optional[str] = "Good"
    age_years: float = Field(1.0, ge=0.0)
    estimated_price: float = Field(50.0, ge=0.0)
    location: Optional[str] = "Local City"
    target_org_type: Optional[str] = None

class RecommendationResponse(BaseModel):
    recommended_action: str
    action_reasoning: str
    reuse_options: List[str]
    recycling_methods: List[str]
    suitable_buyers_ngos: List[str]
    sustainability_actions: List[str]

class ImageClassificationResponse(BaseModel):
    predicted_category: str
    confidence_score: float
    is_low_confidence: bool = False
    low_confidence_warning: Optional[str] = None
    detected_objects: List[Dict[str, Any]] = []
    top_5_predictions: List[Dict[str, Any]] = []
    condition: str
    visual_defects_detected: List[str] = []
    repairability_score: float
    repairability_rating: str = "Medium"
    repairability_reasoning: Optional[str] = None
    sustainability_score: float
    predicted_price: float
    resale_value_display: str = "Not Applicable"
    is_resale_applicable: bool = True
    recycling_value: float = 0.0
    recycling_value_inr: str = "₹0"
    recycling_value_usd: str = "$0.00"
    recommendation: str
    image_url: Optional[str] = None
    co2_saved_kg: Optional[float] = 0.0
    waste_diverted_kg: Optional[float] = 0.0
    gradcam_base64: Optional[str] = None
    explanation_text: Optional[str] = None
    model_info: Optional[Dict[str, Any]] = None
    details: Optional[Dict[str, Any]] = None

# --- Major Hybrid AI System Schemas (CV + User Metadata) ---

class HybridVisionIdentifyResponse(BaseModel):
    detected_object: str
    primary_material: str
    product_category: str
    confidence_score: float
    is_low_confidence: bool = False
    low_confidence_warning: Optional[str] = None
    bounding_boxes: List[Dict[str, Any]] = []
    top_5_predictions: List[Dict[str, Any]] = []
    image_url: Optional[str] = None
    gradcam_base64: Optional[str] = None
    explanation_text: Optional[str] = None

class HybridAnalysisRequest(BaseModel):
    image_url: Optional[str] = None
    product_name: str = "Laptop"
    brand: Optional[str] = "Generic"
    material: Optional[str] = "Aluminum"
    category: Optional[str] = "Electronics"
    approximate_age: float = 1.0
    weight_kg: float = 1.5
    dimensions: Optional[str] = "30 x 20 x 2 cm"
    color: Optional[str] = "Silver"
    purchase_year: Optional[int] = 2024
    original_price: float = 800.0
    current_usage: str = "Moderate"
    working_condition: str = "Fully Functional"
    physical_description: Optional[str] = "Standard usage wear"
    visible_damage: Optional[str] = "Minor Scratches"
    missing_parts: Optional[str] = "None"
    battery_included: bool = True
    power_status: str = "Powers On"
    accessories_included: bool = True
    packaging_available: bool = False
    warranty_available: bool = False
    storage_capacity: Optional[str] = "512GB SSD"
    model_number: Optional[str] = "N/A"
    serial_number: Optional[str] = "N/A"
    additional_notes: Optional[str] = None

class HybridAnalysisResponse(BaseModel):
    detected_object: str
    confidence_score: float
    is_low_confidence: bool = False
    low_confidence_warning: Optional[str] = None
    primary_material: str
    product_category: str
    top_5_predictions: List[Dict[str, Any]] = []
    bounding_boxes: List[Dict[str, Any]] = []
    estimated_condition: str
    condition_reasoning: str
    visual_defects_detected: List[str] = []
    repairability_score: float
    repairability_rating: str
    repairability_reasoning: str
    predicted_resale_price: float
    resale_value_display: str
    is_resale_applicable: bool
    recycling_value_inr: str
    recycling_value_usd: str
    sustainability_score: float
    co2_saved_kg: float
    waste_diverted_kg: float
    recommended_action: str
    action_reasoning: str
    image_url: Optional[str] = None
    gradcam_base64: Optional[str] = None
    explanation_text: Optional[str] = None
    model_info: Dict[str, Any]

class ManualClassificationRequest(BaseModel):
    item_name: str = Field(..., min_length=2, description="Name or description of the item")
    category: Optional[str] = Field("Plastic Bottle", description="Taxonomy material category")
    condition: Optional[str] = Field("Good", description="Item visual condition")
    weight_kg: float = Field(0.5, ge=0.0, description="Item weight in kilograms")
    age_years: float = Field(1.0, ge=0.0, description="Item age in years")
    original_price: float = Field(50.0, ge=0.0, description="Original retail price")

class ManualClassificationResponse(BaseModel):
    item_name: str
    predicted_category: str
    confidence_score: float = 0.965
    broad_category: str
    condition: str
    weight_kg: float
    repairability_score: float
    repairability_rating: str
    repairability_reasoning: str
    predicted_price: float
    resale_value_display: str
    is_resale_applicable: bool
    recycling_value_inr: str
    recycling_value_usd: str
    sustainability_score: float
    co2_saved_kg: float
    waste_diverted_kg: float
    recommendation: Dict[str, Any]
    explanation_text: str
    top_5_predictions: List[Dict[str, Any]] = []
    model_info: Dict[str, Any]