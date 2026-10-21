from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.deps import require_role
from app.schemas.user import UserResponse
from app.schemas.item import ItemResponse
from app.schemas.ai import AILogResponse
from app.schemas.analytics import SystemStatsResponse
from app.repositories.user_repository import user_repository
from app.repositories.item_repository import item_repository
from app.repositories.transaction_repository import transaction_repository
from app.repositories.organization_repository import organization_repository
from app.repositories.ai_log_repository import ai_log_repository
from app.models.user import User, UserRole
from app.models.item import Item
from app.models.transaction import Transaction

router = APIRouter()

@router.get("/stats", response_model=SystemStatsResponse, summary="Get system aggregated analytics and metrics")
def get_system_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN.value]))
):
    users_count = len(user_repository.get_all(db))
    ngos_count = len(organization_repository.get_by_type(db, UserRole.NGO.value))
    recyclers_count = len(organization_repository.get_by_type(db, UserRole.RECYCLING_CENTER.value))
    items = item_repository.get_all(db)
    transactions = transaction_repository.get_all(db)

    total_co2 = sum(item.co2_saved_kg for item in items if item.status not in ["Available"])
    total_waste = sum(item.waste_diverted_kg for item in items if item.status not in ["Available"])

    # Category Breakdown
    cat_dist = {}
    for item in items:
        cat_dist[item.category] = cat_dist.get(item.category, 0) + 1

    # Action Breakdown
    act_dist = {}
    for item in items:
        act_dist[item.recommended_action] = act_dist.get(item.recommended_action, 0) + 1

    ai_logs = ai_log_repository.get_recent_logs(db, limit=100)

    return SystemStatsResponse(
        total_users=users_count,
        total_ngos=ngos_count,
        total_recycling_centers=recyclers_count,
        total_items_uploaded=len(items),
        total_co2_saved_kg=round(total_co2, 2),
        total_waste_diverted_kg=round(total_waste, 2),
        total_transactions=len(transactions),
        category_distribution=cat_dist,
        action_recommendation_distribution=act_dist,
        recent_ai_logs_count=len(ai_logs)
    )

@router.get("/users", response_model=List[UserResponse], summary="List all registered system users (Admin only)")
def list_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN.value]))
):
    return user_repository.get_all(db)

@router.get("/items", response_model=List[ItemResponse], summary="List all system items (Admin only)")
def list_all_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN.value]))
):
    return item_repository.get_all(db)

@router.get("/ai-logs", response_model=List[AILogResponse], summary="List AI prediction logs (Admin only)")
def list_ai_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN.value]))
):
    return ai_log_repository.get_recent_logs(db, limit=50)

@router.delete("/ai-logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an AI log entry (Admin only)")
def delete_ai_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN.value]))
):
    log_entry = ai_log_repository.get(db, log_id)
    if not log_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AI Log not found")
    ai_log_repository.delete(db, log_id)
    return None
