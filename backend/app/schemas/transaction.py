from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Optional, List, Any
from datetime import datetime

class TransactionCreate(BaseModel):
    item_id: int
    transaction_type: Optional[str] = Field(None, description="purchase, sale, recycling, donation, transfer")
    action_type: Optional[str] = Field(None, description="donate, recycle, sell, repair")
    quantity: int = Field(default=1, ge=1, description="Quantity must be at least 1")
    unit_price: float = Field(default=0.0, ge=0.0, description="Unit price must be non-negative")
    total_amount: Optional[float] = Field(None, ge=0.0)
    agreed_price: Optional[float] = Field(None, ge=0.0)
    seller_id: Optional[int] = None
    sender_id: Optional[int] = None
    buyer_id: Optional[int] = None
    receiver_id: Optional[int] = None
    organization_id: Optional[int] = None
    transaction_status: Optional[str] = Field(default="Pending")
    status: Optional[str] = None
    payment_status: Optional[str] = Field(default="Unpaid")
    notes: Optional[str] = ""

    @model_validator(mode="before")
    @classmethod
    def sync_type_and_participants(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Sync transaction_type and action_type
            tx_type = data.get("transaction_type") or data.get("action_type") or "sale"
            data["transaction_type"] = tx_type.lower()
            data["action_type"] = tx_type.lower()

            # Sync seller/sender
            seller = data.get("seller_id") or data.get("sender_id")
            if seller:
                data["seller_id"] = seller
                data["sender_id"] = seller

            # Sync buyer/receiver
            buyer = data.get("buyer_id") or data.get("receiver_id")
            if buyer:
                data["buyer_id"] = buyer
                data["receiver_id"] = buyer

            # Sync transaction_status / status
            st = data.get("transaction_status") or data.get("status") or "Completed"
            data["transaction_status"] = st
            data["status"] = st

            # Calculate total_amount if missing
            qty = data.get("quantity") or 1
            price = data.get("unit_price") if data.get("unit_price") is not None else (data.get("agreed_price") or 0.0)
            if data.get("total_amount") is None:
                data["total_amount"] = float(qty * price)
            if data.get("agreed_price") is None:
                data["agreed_price"] = data["total_amount"]
        return data

class TransactionUpdate(BaseModel):
    transaction_status: Optional[str] = Field(None, description="Pending, Completed, Cancelled, Failed")
    status: Optional[str] = None
    payment_status: Optional[str] = Field(None, description="Unpaid, Paid, Refunded, N/A")
    quantity: Optional[int] = Field(None, ge=1)
    unit_price: Optional[float] = Field(None, ge=0.0)
    notes: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def sync_update_status(cls, data: Any) -> Any:
        if isinstance(data, dict):
            st = data.get("transaction_status") or data.get("status")
            if st:
                data["transaction_status"] = st
                data["status"] = st
        return data

class TransactionStatusUpdate(TransactionUpdate):
    pass


class TransactionResponse(BaseModel):
    id: int
    item_id: int
    transaction_type: str
    action_type: str
    seller_id: Optional[int] = None
    sender_id: Optional[int] = None
    buyer_id: Optional[int] = None
    receiver_id: Optional[int] = None
    organization_id: Optional[int] = None
    quantity: int = 1
    unit_price: float = 0.0
    total_amount: float = 0.0
    agreed_price: float = 0.0
    transaction_status: str
    status: str
    payment_status: str
    notes: Optional[str] = ""
    co2_saved_kg: float = 0.0
    waste_diverted_kg: float = 0.0
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def populate_fallback_fields(cls, data: Any) -> Any:
        if hasattr(data, "transaction_type") and hasattr(data, "action_type"):
            tx_type = getattr(data, "transaction_type") or getattr(data, "action_type") or "sale"
            setattr(data, "transaction_type", tx_type)
            setattr(data, "action_type", tx_type)

            seller = getattr(data, "seller_id", None) or getattr(data, "sender_id", None)
            setattr(data, "seller_id", seller)
            setattr(data, "sender_id", seller)

            buyer = getattr(data, "buyer_id", None) or getattr(data, "receiver_id", None)
            setattr(data, "buyer_id", buyer)
            setattr(data, "receiver_id", buyer)

            st = getattr(data, "transaction_status", None) or getattr(data, "status", None) or "Completed"
            setattr(data, "transaction_status", st)
            setattr(data, "status", st)
        elif isinstance(data, dict):
            tx_type = data.get("transaction_type") or data.get("action_type") or "sale"
            data["transaction_type"] = tx_type
            data["action_type"] = tx_type
            
            seller = data.get("seller_id") or data.get("sender_id")
            data["seller_id"] = seller
            data["sender_id"] = seller
            
            buyer = data.get("buyer_id") or data.get("receiver_id")
            data["buyer_id"] = buyer
            data["receiver_id"] = buyer

            st = data.get("transaction_status") or data.get("status") or "Completed"
            data["transaction_status"] = st
            data["status"] = st
        return data

class PaginatedTransactionResponse(BaseModel):
    items: List[TransactionResponse]
    page: int
    page_size: int
    total_items: int
    total_pages: int

    model_config = ConfigDict(from_attributes=True)