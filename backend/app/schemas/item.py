from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Optional, Any
from datetime import datetime

class ItemCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    item_name: Optional[str] = None
    description: Optional[str] = ""
    category: str = Field(..., min_length=2)
    brand: Optional[str] = "Generic"
    age_years: float = Field(..., ge=0.0, description="Age in years must be non-negative")
    usage_level: Optional[str] = "Moderate"
    condition: str = Field(..., min_length=2)
    original_price: float = Field(..., ge=0.0, description="Original price must be non-negative")
    price: Optional[float] = Field(default=0.0, ge=0.0)
    quantity: int = Field(default=1, ge=0)
    unit: str = "pcs"
    organization_id: Optional[int] = None
    location: Optional[str] = "Local City"
    image_url: Optional[str] = None

class ItemUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=150)
    item_name: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = None
    condition: Optional[str] = None
    status: Optional[str] = None
    estimated_price: Optional[float] = Field(None, ge=0.0)
    price: Optional[float] = Field(None, ge=0.0)
    quantity: Optional[int] = Field(None, ge=0)
    unit: Optional[str] = None
    organization_id: Optional[int] = None

class ItemResponse(BaseModel):
    id: int
    owner_id: int
    organization_id: Optional[int] = None
    title: str
    item_name: Optional[str] = None
    description: Optional[str]
    category: str
    quantity: int = 1
    unit: str = "pcs"
    price: float = 0.0
    brand: Optional[str]
    image_url: Optional[str]
    age_years: float
    usage_level: Optional[str]
    condition: str
    original_price: float
    estimated_price: float
    location: str
    predicted_category: Optional[str]
    predicted_condition: Optional[str]
    recommended_action: str
    ai_confidence: Optional[float]
    co2_saved_kg: float
    waste_diverted_kg: float
    environmental_impact_points: float
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def populate_item_name(cls, data: Any) -> Any:
        if hasattr(data, "item_name") and hasattr(data, "title"):
            item_name_val = getattr(data, "item_name") or getattr(data, "title") or ""
            setattr(data, "item_name", item_name_val)
        elif isinstance(data, dict):
            val = data.get("item_name") or data.get("title") or ""
            data["item_name"] = val
        return data