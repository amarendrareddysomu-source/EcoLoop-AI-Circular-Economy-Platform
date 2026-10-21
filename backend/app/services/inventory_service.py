import math
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.item import Item, ItemStatus, ItemCondition
from app.models.user import User, UserRole
from app.repositories.item_repository import item_repository
from app.schemas.inventory import (
    InventoryItemCreate,
    InventoryItemUpdate,
    InventoryItemResponse,
    PaginatedInventoryResponse
)
from app.services.ai_service import ai_service
from app.core.deps import ADMIN_ROLES

class InventoryService:
    def _is_admin(self, user: User) -> bool:
        return user.role in ADMIN_ROLES or user.role == UserRole.ADMIN.value or user.role == UserRole.SUPER_ADMIN.value

    def _check_access_permission(self, item: Item, user: User) -> None:
        if self._is_admin(user):
            return
        
        # User owns the item
        if item.owner_id == user.id:
            return
        
        # Item belongs to user's organization
        if user.organization_id is not None and item.organization_id == user.organization_id:
            return
            
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access items within your organization or owned by you."
        )

    def create_inventory_item(self, db: Session, current_user: User, item_in: InventoryItemCreate) -> Item:
        item_name = item_in.item_name or item_in.title or "Untitled Item"
        org_id = item_in.organization_id if item_in.organization_id is not None else current_user.organization_id

        # Optional AI analysis call for enhanced impact scores
        ai_res = ai_service.analyze_item(
            db=db,
            image_bytes=None,
            category_hint=item_in.category,
            brand=item_in.brand or "Generic",
            age_years=item_in.age_years,
            usage_level=item_in.usage_level or "Moderate",
            original_price=item_in.price,
            user_stated_condition=item_in.condition
        )

        db_item = Item(
            owner_id=current_user.id,
            organization_id=org_id,
            title=item_name,
            item_name=item_name,
            description=item_in.description or "",
            category=item_in.category,
            quantity=item_in.quantity,
            unit=item_in.unit or "pcs",
            price=item_in.price,
            brand=item_in.brand or "Generic",
            image_url=item_in.image_url,
            age_years=item_in.age_years,
            usage_level=item_in.usage_level or "Moderate",
            condition=item_in.condition or ItemCondition.USED.value,
            original_price=item_in.price,
            estimated_price=ai_res.get("estimated_resale_price", item_in.price),
            location=item_in.location or "Local City",
            predicted_category=ai_res.get("classified_category", item_in.category),
            predicted_condition=ai_res.get("predicted_condition", item_in.condition),
            recommended_action=ai_res.get("recommended_action", "Reuse"),
            ai_confidence=ai_res.get("category_confidence", 0.85),
            co2_saved_kg=ai_res.get("co2_saved_kg", 0.0),
            waste_diverted_kg=ai_res.get("waste_diverted_kg", 0.0),
            environmental_impact_points=ai_res.get("environmental_impact_points", 0.0),
            status=item_in.status or ItemStatus.AVAILABLE.value
        )
        return item_repository.create(db, db_item)

    def get_inventory_item(self, db: Session, current_user: User, item_id: int) -> Item:
        item = item_repository.get(db, item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found")
        self._check_access_permission(item, current_user)
        return item

    def list_inventory(
        self,
        db: Session,
        current_user: User,
        *,
        category: Optional[str] = None,
        status_filter: Optional[str] = None,
        condition: Optional[str] = None,
        organization_id: Optional[int] = None,
        owner_id: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_quantity: Optional[int] = None,
        max_quantity: Optional[int] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
        sort_by: Optional[str] = "created_at",
        sort_order: Optional[str] = "desc"
    ) -> PaginatedInventoryResponse:
        
        # Authorization enforcement for listing
        if self._is_admin(current_user):
            effective_owner_id = owner_id
            effective_org_id = organization_id
        else:
            # Non-admin user can only view items belonging to their organization or own items
            if current_user.organization_id is not None:
                effective_org_id = current_user.organization_id
                effective_owner_id = owner_id if owner_id == current_user.id else current_user.id
            else:
                effective_owner_id = current_user.id
                effective_org_id = None

        items, total_items = item_repository.get_inventory_paginated(
            db,
            owner_id=effective_owner_id,
            organization_id=effective_org_id,
            category=category,
            status=status_filter,
            condition=condition,
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

        total_pages = math.ceil(total_items / page_size) if total_items > 0 else 0

        # Transform items into Pydantic models ensuring item_name is populated
        response_items = []
        for item in items:
            item_resp = InventoryItemResponse.model_validate(item)
            response_items.append(item_resp)

        return PaginatedInventoryResponse(
            items=response_items,
            page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages
        )

    def update_inventory_item(
        self,
        db: Session,
        current_user: User,
        item_id: int,
        item_update: InventoryItemUpdate
    ) -> Item:
        item = self.get_inventory_item(db, current_user, item_id)

        update_dict = item_update.model_dump(exclude_unset=True)
        if "item_name" in update_dict or "title" in update_dict:
            name = update_dict.get("item_name") or update_dict.get("title")
            if name:
                update_dict["item_name"] = name
                update_dict["title"] = name

        return item_repository.update(db, item, update_dict)

    def delete_inventory_item(self, db: Session, current_user: User, item_id: int) -> bool:
        item = self.get_inventory_item(db, current_user, item_id)
        item_repository.delete(db, item.id)
        return True

inventory_service = InventoryService()
