from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

class ReportStatus(str, enum.Enum):
    PENDING = "Pending"
    IN_REVIEW = "In Review"
    RESOLVED = "Resolved"
    DISMISSED = "Dismissed"

class ReportType(str, enum.Enum):
    ITEM_ISSUE = "item_issue"
    USER_BEHAVIOR = "user_behavior"
    TRANSACTION_DISPUTE = "transaction_dispute"
    SYSTEM_FEEDBACK = "system_feedback"
    ENVIRONMENTAL_QUERY = "environmental_query"

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    reporter_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    target_item_id = Column(Integer, ForeignKey("items.id", ondelete="SET NULL"), nullable=True, index=True)
    target_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    report_type = Column(String, nullable=False, index=True, default=ReportType.SYSTEM_FEEDBACK.value)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String, nullable=False, default=ReportStatus.PENDING.value, index=True)
    admin_notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    reporter = relationship("User", foreign_keys=[reporter_id], backref="submitted_reports")
    target_item = relationship("Item", foreign_keys=[target_item_id], backref="reports")
    target_user = relationship("User", foreign_keys=[target_user_id], backref="received_reports")
