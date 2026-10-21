from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

class TransactionType(str, enum.Enum):
    PURCHASE = "purchase"
    SALE = "sale"
    RECYCLING = "recycling"
    DONATION = "donation"
    TRANSFER = "transfer"
    # Backwards compatibility
    DONATE = "donate"
    RECYCLE = "recycle"
    SELL = "sell"
    REPAIR = "repair"

class TransactionStatus(str, enum.Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    FAILED = "Failed"
    # Backwards compatibility
    REQUESTED = "Requested"
    ACCEPTED = "Accepted"
    IN_PROCESSING = "In Processing"

class PaymentStatus(str, enum.Enum):
    UNPAID = "Unpaid"
    PAID = "Paid"
    REFUNDED = "Refunded"
    NOT_APPLICABLE = "N/A"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"), nullable=False, index=True)
    
    transaction_type = Column(String, nullable=True, index=True)
    action_type = Column(String, nullable=True, index=True)
    
    seller_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    
    buyer_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True, index=True)
    
    quantity = Column(Integer, nullable=False, default=1, index=True)
    unit_price = Column(Float, nullable=False, default=0.0, index=True)
    total_amount = Column(Float, nullable=False, default=0.0, index=True)
    agreed_price = Column(Float, default=0.0)
    
    transaction_status = Column(String, nullable=False, default=TransactionStatus.PENDING.value, index=True)
    status = Column(String, nullable=False, default=TransactionStatus.PENDING.value, index=True)
    payment_status = Column(String, nullable=False, default=PaymentStatus.UNPAID.value, index=True)
    
    notes = Column(String, nullable=True)
    co2_saved_kg = Column(Float, default=0.0)
    waste_diverted_kg = Column(Float, default=0.0)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    item = relationship("Item", backref="transactions")
    seller = relationship("User", foreign_keys=[seller_id])
    buyer = relationship("User", foreign_keys=[buyer_id])
    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
    organization = relationship("Organization", foreign_keys=[organization_id], backref="transactions")


