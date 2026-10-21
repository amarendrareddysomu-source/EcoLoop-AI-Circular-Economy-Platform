from typing import List, Optional, Tuple
from sqlalchemy import select, func, or_, asc, desc
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.item import Item

class ItemRepository(BaseRepository[Item]):
    def __init__(self):
        super().__init__(Item)

    def get_by_owner(self, db: Session, owner_id: int) -> List[Item]:
        return db.query(Item).filter(Item.owner_id == owner_id).order_by(Item.created_at.desc()).all()

    def get_by_category(self, db: Session, category: str) -> List[Item]:
        return db.query(Item).filter(Item.category == category).all()

    def get_by_status(self, db: Session, status: str) -> List[Item]:
        return db.query(Item).filter(Item.status == status).order_by(Item.created_at.desc()).all()

    def get_available_for_action(self, db: Session, recommended_action: str) -> List[Item]:
        return db.query(Item).filter(
            Item.recommended_action == recommended_action,
            Item.status == "Available"
        ).order_by(Item.created_at.desc()).all()

    def get_inventory_paginated(
        self,
        db: Session,
        *,
        owner_id: Optional[int] = None,
        organization_id: Optional[int] = None,
        category: Optional[str] = None,
        status: Optional[str] = None,
        condition: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_quantity: Optional[int] = None,
        max_quantity: Optional[int] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
        sort_by: Optional[str] = "created_at",
        sort_order: Optional[str] = "desc"
    ) -> Tuple[List[Item], int]:
        page = max(1, page)
        page_size = max(1, min(page_size, 100))

        query = select(Item)

        # Access filters
        if owner_id is not None and organization_id is not None:
            query = query.where(or_(Item.owner_id == owner_id, Item.organization_id == organization_id))
        elif owner_id is not None:
            query = query.where(Item.owner_id == owner_id)
        elif organization_id is not None:
            query = query.where(Item.organization_id == organization_id)

        # Metadata filters
        if category:
            query = query.where(func.lower(Item.category) == category.lower())
        if status:
            query = query.where(func.lower(Item.status) == status.lower())
        if condition:
            query = query.where(func.lower(Item.condition) == condition.lower())
        if min_price is not None:
            query = query.where(Item.price >= min_price)
        if max_price is not None:
            query = query.where(Item.price <= max_price)
        if min_quantity is not None:
            query = query.where(Item.quantity >= min_quantity)
        if max_quantity is not None:
            query = query.where(Item.quantity <= max_quantity)

        # Case-insensitive partial search
        if search and search.strip():
            search_pattern = f"%{search.strip()}%"
            query = query.where(
                or_(
                    Item.item_name.ilike(search_pattern),
                    Item.title.ilike(search_pattern),
                    Item.description.ilike(search_pattern)
                )
            )

        # Count query
        count_stmt = select(func.count()).select_from(query.subquery())
        total_items = db.execute(count_stmt).scalar() or 0

        # Sorting
        sort_attr_map = {
            "name": Item.title,
            "title": Item.title,
            "item_name": Item.title,
            "price": Item.price,
            "quantity": Item.quantity,
            "created_at": Item.created_at,
            "created_date": Item.created_at,
            "updated_at": Item.updated_at,
            "updated_date": Item.updated_at,
        }

        sort_field_lower = (sort_by or "created_at").lower()
        sort_col = sort_attr_map.get(sort_field_lower, Item.created_at)

        if sort_order and sort_order.lower() == "asc":
            query = query.order_by(asc(sort_col))
        else:
            query = query.order_by(desc(sort_col))

        # Pagination offset/limit
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        items = db.execute(query).scalars().all()
        return list(items), total_items

item_repository = ItemRepository()

