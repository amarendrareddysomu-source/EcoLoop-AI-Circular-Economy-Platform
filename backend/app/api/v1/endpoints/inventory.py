from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.schemas.inventory import (
    InventoryItemCreate,
    InventoryItemUpdate,
    InventoryItemResponse,
    PaginatedInventoryResponse
)
from app.services.inventory_service import inventory_service

router = APIRouter()

@router.post(
    "/",
    response_model=InventoryItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new inventory item",
    description="Create an inventory item with quantity, unit, price, condition, status, and organization assignment."
)
def create_inventory_item(
    item_in: InventoryItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    item = inventory_service.create_inventory_item(db, current_user, item_in)
    return InventoryItemResponse.model_validate(item)

@router.get(
    "/",
    response_model=PaginatedInventoryResponse,
    summary="List inventory items with search, filters, sorting, and pagination",
    description="Query inventory with advanced filtering (category, status, condition, org, owner, price/quantity range), case-insensitive search, pagination, and sorting."
)
def list_inventory_items(
    category: Optional[str] = Query(None, description="Filter by category"),
    status: Optional[str] = Query(None, description="Filter by status (Available, Reserved, Sold, Recycled)"),
    condition: Optional[str] = Query(None, description="Filter by condition (New, Used, Damaged, Recycled)"),
    organization_id: Optional[int] = Query(None, description="Filter by organization ID"),
    owner_id: Optional[int] = Query(None, description="Filter by owner ID"),
    min_price: Optional[float] = Query(None, ge=0.0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0.0, description="Maximum price"),
    min_quantity: Optional[int] = Query(None, ge=0, description="Minimum quantity"),
    max_quantity: Optional[int] = Query(None, ge=0, description="Maximum quantity"),
    search: Optional[str] = Query(None, description="Search term for item name or description"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    sort_by: Optional[str] = Query("created_at", description="Sort by field: name, price, quantity, created_at, updated_at"),
    sort_order: Optional[str] = Query("desc", description="Sort direction: asc or desc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return inventory_service.list_inventory(
        db,
        current_user,
        category=category,
        status_filter=status,
        condition=condition,
        organization_id=organization_id,
        owner_id=owner_id,
        min_price=min_price,
        max_price=max_price,
        min_quantity=min_quantity,
        max_quantity=max_quantity,
        search=search,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order
    )

@router.get(
    "/{item_id}",
    response_model=InventoryItemResponse,
    summary="Get inventory item details by ID",
    description="Retrieve a specific inventory item. Users can only access items in their organization or owned by them unless Admin."
)
def get_inventory_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    item = inventory_service.get_inventory_item(db, current_user, item_id)
    return InventoryItemResponse.model_validate(item)

@router.put(
    "/{item_id}",
    response_model=InventoryItemResponse,
    summary="Update an existing inventory item",
    description="Update item details. Requires ownership or organization access/Admin rights."
)
def update_inventory_item(
    item_id: int,
    item_update: InventoryItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    item = inventory_service.update_inventory_item(db, current_user, item_id, item_update)
    return InventoryItemResponse.model_validate(item)

@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an inventory item by ID",
    description="Delete an item from inventory. Requires ownership or organization access/Admin rights."
)
def delete_inventory_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    inventory_service.delete_inventory_item(db, current_user, item_id)
    return None
