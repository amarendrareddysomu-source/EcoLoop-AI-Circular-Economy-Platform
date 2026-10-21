from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User, UserRole
from app.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    PaginatedTransactionResponse
)
from app.services.transaction_service import transaction_service

router = APIRouter()

@router.post(
    "/",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new transaction",
    description="Process a transaction (Purchase, Sale, Recycling, Donation, Transfer) with automatic stock validation and inventory updating."
)
def create_transaction(
    tx_in: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    tx = transaction_service.create_transaction(db, current_user, tx_in)
    return TransactionResponse.model_validate(tx)

@router.get(
    "/",
    response_model=PaginatedTransactionResponse,
    summary="List transactions with search, filters, sorting, and pagination",
    description="Search across transaction ID, item name, user names, organization name; filter by type, status, payment status, org, user, item, and date range."
)
def list_transactions(
    transaction_type: Optional[str] = Query(None, description="Filter by type: purchase, sale, recycling, donation, transfer"),
    status: Optional[str] = Query(None, description="Filter by transaction status: Pending, Completed, Cancelled, Failed"),
    payment_status: Optional[str] = Query(None, description="Filter by payment status: Unpaid, Paid, Refunded, N/A"),
    organization_id: Optional[int] = Query(None, description="Filter by organization ID"),
    user_id: Optional[int] = Query(None, description="Filter by user ID (seller or buyer)"),
    seller_id: Optional[int] = Query(None, description="Filter by seller ID"),
    buyer_id: Optional[int] = Query(None, description="Filter by buyer ID"),
    item_id: Optional[int] = Query(None, description="Filter by item ID"),
    start_date: Optional[datetime] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[datetime] = Query(None, description="End date (ISO format)"),
    search: Optional[str] = Query(None, description="Search term for ID, item name, user name, organization name"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    sort_by: Optional[str] = Query("created_at", description="Sort by field: date, amount, quantity, status"),
    sort_order: Optional[str] = Query("desc", description="Sort direction: asc or desc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return transaction_service.list_transactions(
        db,
        current_user,
        transaction_type=transaction_type,
        status_filter=status,
        payment_status=payment_status,
        organization_id=organization_id,
        user_id=user_id,
        seller_id=seller_id,
        buyer_id=buyer_id,
        item_id=item_id,
        start_date=start_date,
        end_date=end_date,
        search=search,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order
    )

@router.get(
    "/my-transactions",
    response_model=PaginatedTransactionResponse,
    summary="List transactions involved by current user"
)
def get_my_transactions(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return transaction_service.list_transactions(
        db,
        current_user,
        user_id=current_user.id,
        page=page,
        page_size=page_size
    )

@router.get(
    "/{tx_id}",
    response_model=TransactionResponse,
    summary="Get details for a specific transaction by ID"
)
def get_transaction_by_id(
    tx_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    tx = transaction_service.get_transaction(db, current_user, tx_id)
    return TransactionResponse.model_validate(tx)

@router.put(
    "/{tx_id}",
    response_model=TransactionResponse,
    summary="Update transaction details"
)
def update_transaction(
    tx_id: int,
    update_in: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    tx = transaction_service.update_transaction(db, current_user, tx_id, update_in)
    return TransactionResponse.model_validate(tx)

@router.put(
    "/{tx_id}/status",
    response_model=TransactionResponse,
    summary="Update transaction status (backward compatibility)"
)
def update_transaction_status(
    tx_id: int,
    update_in: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    tx = transaction_service.update_transaction(db, current_user, tx_id, update_in)
    return TransactionResponse.model_validate(tx)

@router.delete(
    "/{tx_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancel or delete transaction and restore inventory stock"
)
def delete_transaction(
    tx_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    transaction_service.delete_transaction(db, current_user, tx_id)
    return None
