from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.item_repository import item_repository
from app.schemas.item import ItemCreate, ItemUpdate
from app.models.item import Item, ItemStatus
from app.services.ai_service import ai_service

class ItemService:
    def create_item(self, db: Session, owner_id: int, item_in: ItemCreate, image_bytes: Optional[bytes] = None) -> Item:
        # Run AI Pipeline Analysis
        ai_res = ai_service.analyze_item(
            db=db,
            image_bytes=image_bytes,
            category_hint=item_in.category,
            brand=item_in.brand or "Generic",
            age_years=item_in.age_years,
            usage_level=item_in.usage_level or "Moderate",
            original_price=item_in.original_price,
            user_stated_condition=item_in.condition
        )

        db_item = Item(
            owner_id=owner_id,
            organization_id=getattr(item_in, "organization_id", None),
            title=item_in.title,
            item_name=getattr(item_in, "item_name", None) or item_in.title,
            description=item_in.description,
            category=ai_res["classified_category"],
            quantity=getattr(item_in, "quantity", 1),
            unit=getattr(item_in, "unit", "pcs"),
            price=getattr(item_in, "price", 0.0) or item_in.original_price,
            brand=item_in.brand or "Generic",
            image_url=item_in.image_url,
            age_years=item_in.age_years,
            usage_level=item_in.usage_level or "Moderate",
            condition=item_in.condition,
            original_price=item_in.original_price,
            estimated_price=ai_res["estimated_resale_price"],
            location=item_in.location or "Local City",
            predicted_category=ai_res["classified_category"],
            predicted_condition=ai_res["predicted_condition"],
            recommended_action=ai_res["recommended_action"],
            ai_confidence=ai_res["category_confidence"],
            co2_saved_kg=ai_res["co2_saved_kg"],
            waste_diverted_kg=ai_res["waste_diverted_kg"],
            environmental_impact_points=ai_res["environmental_impact_points"],
            status=ItemStatus.AVAILABLE.value
        )
        return item_repository.create(db, db_item)

    def get_item(self, db: Session, item_id: int) -> Item:
        item = item_repository.get(db, item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return item

    def get_user_items(self, db: Session, user_id: int) -> List[Item]:
        return item_repository.get_by_owner(db, user_id)

    def get_all_items(self, db: Session, category: Optional[str] = None, status_filter: Optional[str] = None) -> List[Item]:
        if category:
            return item_repository.get_by_category(db, category)
        if status_filter:
            return item_repository.get_by_status(db, status_filter)
        return item_repository.get_all(db)

    def update_item(self, db: Session, item_id: int, owner_id: int, item_update: ItemUpdate, is_admin: bool = False) -> Item:
        item = self.get_item(db, item_id)
        if item.owner_id != owner_id and not is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to edit this item")
        return item_repository.update(db, item, item_update)

    def delete_item(self, db: Session, item_id: int, owner_id: int, is_admin: bool = False) -> bool:
        item = self.get_item(db, item_id)
        if item.owner_id != owner_id and not is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this item")
        item_repository.delete(db, item.id)
        return True

item_service = ItemService()

