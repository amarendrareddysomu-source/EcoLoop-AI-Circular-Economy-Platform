from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class OrganizationCreate(BaseModel):
    name: str
    org_type: str  # ngo or recycling_center
    description: Optional[str] = None
    address: str
    phone: str
    capacity_kg_per_month: Optional[int] = 1000
    accepted_categories: Optional[str] = (
        "Electronics,Plastic,Paper,Clothing,Books,Furniture,Glass,Metal,Appliances"
    )


class OrganizationResponse(BaseModel):
    id: int
    user_id: int
    name: str
    org_type: str
    description: Optional[str]
    address: str
    phone: str
    capacity_kg_per_month: int
    accepted_categories: str
    is_verified: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)