from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import require_role
from app.schemas.item import ItemResponse
from app.schemas.transaction import TransactionResponse, TransactionStatusUpdate
from app.schemas.organization import OrganizationResponse
from app.repositories.item_repository import item_repository
from app.repositories.organization_repository import organization_repository
from app.services.organization_service import organization_service
from app.services.transaction_service import transaction_service
from app.models.user import User, UserRole

router = APIRouter()

@router.get("/list", response_model=List[OrganizationResponse], summary="Public list of registered Recycling Centers")
def list_recycling_centers(db: Session = Depends(get_db)):
    return organization_repository.get_by_type(db, org_type=UserRole.RECYCLING_CENTER.value)

@router.put("/profile", response_model=OrganizationResponse, summary="Update current Recycling Center organization profile")
def update_recycling_profile(
    update_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.RECYCLING_CENTER.value]))
):
    return organization_service.update_profile(db, current_user.id, update_data)

@router.get("/items/available", response_model=List[ItemResponse], summary="List available items recommended for recycling")
def list_available_recyclables(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.RECYCLING_CENTER.value]))
):
    return item_repository.get_available_for_action(db, recommended_action="Recycle")

@router.get("/processing-queue", response_model=List[TransactionResponse], summary="Get recycling processing queue assigned to current center")
def get_recycling_queue(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.RECYCLING_CENTER.value]))
):
    return transaction_service.get_receiver_transactions(db, current_user.id)

@router.put("/processing-queue/{tx_id}/status", response_model=TransactionResponse, summary="Update recycling processing item status")
def update_processing_status(
    tx_id: int,
    status_update: TransactionStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.RECYCLING_CENTER.value]))
):
    return transaction_service.update_transaction_status(db, tx_id, current_user.id, status_update)

@router.get("/{recycler_id}", response_model=OrganizationResponse, summary="Get Recycling Center profile by ID")
def get_recycling_center_by_id(recycler_id: int, db: Session = Depends(get_db)):
    org = organization_service.get_by_id(db, recycler_id)
    if not org or org.org_type != UserRole.RECYCLING_CENTER.value:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recycling center organization not found")
    return org
