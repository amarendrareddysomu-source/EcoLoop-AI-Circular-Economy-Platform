from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

class ItemCategory(str, enum.Enum):
    ELECTRONICS = "Electronics"
    PLASTIC = "Plastic"
    PAPER = "Paper"
    FURNITURE = "Furniture"
    BOOKS = "Books"
    CLOTHING = "Clothing"
    GLASS = "Glass"
    METAL = "Metal"
    APPLIANCES = "Appliances"

class ItemCondition(str, enum.Enum):
    NEW = "New"
    USED = "Used"
    DAMAGED = "Damaged"
    RECYCLED = "Recycled"
    EXCELLENT = "Excellent"
    GOOD = "Good"
    FAIR = "Fair"
    POOR = "Poor"

class RecommendedAction(str, enum.Enum):
    REPAIR = "Repair"
    REUSE = "Reuse"
    DONATE = "Donate"
    SELL = "Sell"
    RECYCLE = "Recycle"

class ItemStatus(str, enum.Enum):
    AVAILABLE = "Available"
    RESERVED = "Reserved"
    SOLD = "Sold"
    RECYCLED = "Recycled"
    PENDING_DONATION = "Pending Donation"
    DONATED = "Donated"
    PENDING_RECYCLING = "Pending Recycling"
    REPAIRED = "Repaired"

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True, index=True)
    
    title = Column(String, nullable=False, index=True)
    item_name = Column(String, nullable=True, index=True)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=1, index=True)
    unit = Column(String, nullable=False, default="pcs")
    price = Column(Float, nullable=False, default=0.0, index=True)
    brand = Column(String, nullable=True, default="Generic")
    image_url = Column(String, nullable=True)
    age_years = Column(Float, nullable=False, default=0.0)
    usage_level = Column(String, nullable=True, default="Moderate") # Low, Moderate, Heavy
    condition = Column(String, nullable=False) # New, Used, Damaged, Recycled, Excellent, Good, Fair, Poor
    original_price = Column(Float, nullable=False, default=0.0)
    estimated_price = Column(Float, nullable=False, default=0.0)
    location = Column(String, nullable=False, default="Local City")
    
    # AI Analysis Output
    predicted_category = Column(String, nullable=True)
    predicted_condition = Column(String, nullable=True)
    recommended_action = Column(String, nullable=False, default=RecommendedAction.REUSE.value, index=True)
    ai_confidence = Column(Float, nullable=True, default=0.85)
    co2_saved_kg = Column(Float, nullable=False, default=0.0)
    waste_diverted_kg = Column(Float, nullable=False, default=0.0)
    environmental_impact_points = Column(Float, nullable=False, default=0.0)

    status = Column(String, nullable=False, default=ItemStatus.AVAILABLE.value, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User", backref="items")
    organization = relationship("Organization", foreign_keys=[organization_id], backref="inventory_items")


