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

@router.get("/list", response_model=List[OrganizationResponse], summary="Public list of registered NGOs")
def list_ngos(db: Session = Depends(get_db)):
    return organization_repository.get_by_type(db, org_type=UserRole.NGO.value)

@router.put("/profile", response_model=OrganizationResponse, summary="Update current NGO organization profile")
def update_ngo_profile(
    update_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.NGO.value]))
):
    return organization_service.update_profile(db, current_user.id, update_data)

@router.get("/donations/available", response_model=List[ItemResponse], summary="List available items recommended for donation")
def list_available_donations(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.NGO.value]))
):
    return item_repository.get_available_for_action(db, recommended_action="Donate")

@router.get("/requests", response_model=List[TransactionResponse], summary="Get donation requests assigned to current NGO")
def get_ngo_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.NGO.value]))
):
    return transaction_service.get_receiver_transactions(db, current_user.id)

@router.put("/requests/{tx_id}/status", response_model=TransactionResponse, summary="Update donation request processing status")
def update_ngo_request_status(
    tx_id: int,
    status_update: TransactionStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.NGO.value]))
):
    return transaction_service.update_transaction_status(db, tx_id, current_user.id, status_update)

@router.get("/{ngo_id}", response_model=OrganizationResponse, summary="Get NGO profile by ID")
def get_ngo_by_id(ngo_id: int, db: Session = Depends(get_db)):
    org = organization_service.get_by_id(db, ngo_id)
    if not org or org.org_type != UserRole.NGO.value:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NGO organization not found")
    return org
