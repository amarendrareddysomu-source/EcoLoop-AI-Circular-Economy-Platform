from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

class OrgType(str, enum.Enum):
    NGO = "ngo"
    RECYCLING_CENTER = "recycling_center"

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", use_alter=True, name="fk_organizations_user_id"), unique=True, nullable=False, index=True)
    name = Column(String, nullable=False, index=True)
    org_type = Column(String, nullable=False, index=True) # ngo or recycling_center
    description = Column(Text, nullable=True)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    capacity_kg_per_month = Column(Integer, default=1000)
    accepted_categories = Column(String, nullable=False, default="Electronics,Plastic,Paper,Clothing,Books,Furniture,Glass,Metal,Appliances")
    is_verified = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", foreign_keys=[user_id], backref="organization_profile")


