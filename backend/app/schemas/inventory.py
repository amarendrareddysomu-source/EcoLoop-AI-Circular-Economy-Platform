from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Optional, List, Any
from datetime import datetime

class InventoryItemCreate(BaseModel):
    item_name: Optional[str] = Field(None, min_length=1, max_length=150)
    title: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = ""
    category: str = Field(..., min_length=2)
    quantity: int = Field(default=1, ge=0, description="Quantity must be non-negative")
    unit: str = Field(default="pcs", min_length=1)
    price: float = Field(default=0.0, ge=0.0, description="Price must be non-negative")
    condition: str = Field(default="Used", min_length=2)
    status: str = Field(default="Available", min_length=2)
    organization_id: Optional[int] = None
    brand: Optional[str] = "Generic"
    location: Optional[str] = "Local City"
    image_url: Optional[str] = None
    age_years: float = Field(default=0.0, ge=0.0)
    usage_level: Optional[str] = "Moderate"

    @model_validator(mode="before")
    @classmethod
    def sync_name_and_title(cls, data: Any) -> Any:
        if isinstance(data, dict):
            name = data.get("item_name") or data.get("title")
            if not name:
                raise ValueError("Either 'item_name' or 'title' must be provided.")
            data["item_name"] = name
            data["title"] = name
        return data

class InventoryItemUpdate(BaseModel):
    item_name: Optional[str] = Field(None, min_length=1, max_length=150)
    title: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[int] = Field(None, ge=0, description="Quantity must be non-negative")
    unit: Optional[str] = None
    price: Optional[float] = Field(None, ge=0.0, description="Price must be non-negative")
    condition: Optional[str] = None
    status: Optional[str] = None
    organization_id: Optional[int] = None
    brand: Optional[str] = None
    location: Optional[str] = None
    image_url: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def sync_update_name(cls, data: Any) -> Any:
        if isinstance(data, dict):
            name = data.get("item_name") or data.get("title")
            if name:
                data["item_name"] = name
                data["title"] = name
        return data

class InventoryItemResponse(BaseModel):
    id: int
    item_name: str
    title: str
    description: Optional[str] = ""
    category: str
    quantity: int
    unit: str
    price: float
    condition: str
    status: str
    organization_id: Optional[int] = None
    owner_id: int
    brand: Optional[str] = "Generic"
    location: Optional[str] = "Local City"
    image_url: Optional[str] = None
    recommended_action: Optional[str] = "Reuse"
    co2_saved_kg: float = 0.0
    waste_diverted_kg: float = 0.0
    environmental_impact_points: float = 0.0
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
            data["title"] = val
        return data

class PaginatedInventoryResponse(BaseModel):
    items: List[InventoryItemResponse]
    page: int
    page_size: int
    total_items: int
    total_pages: int

    model_config = ConfigDict(from_attributes=True)
