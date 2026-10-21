from typing import List, Optional, Tuple
from datetime import datetime
from sqlalchemy import select, func, or_, asc, desc, cast, String
from sqlalchemy.orm import Session, aliased
from app.repositories.base import BaseRepository
from app.models.transaction import Transaction
from app.models.item import Item
from app.models.user import User
from app.models.organization import Organization

class TransactionRepository(BaseRepository[Transaction]):
    def __init__(self):
        super().__init__(Transaction)

    def get_by_user(self, db: Session, user_id: int) -> List[Transaction]:
        return db.query(Transaction).filter(
            or_(
                Transaction.seller_id == user_id,
                Transaction.buyer_id == user_id,
                Transaction.sender_id == user_id,
                Transaction.receiver_id == user_id
            )
        ).order_by(Transaction.created_at.desc()).all()

    def get_by_receiver(self, db: Session, receiver_id: int) -> List[Transaction]:
        return db.query(Transaction).filter(
            or_(Transaction.buyer_id == receiver_id, Transaction.receiver_id == receiver_id)
        ).order_by(Transaction.created_at.desc()).all()

    def get_by_action_type(self, db: Session, action_type: str) -> List[Transaction]:
        return db.query(Transaction).filter(
            or_(
                func.lower(Transaction.transaction_type) == action_type.lower(),
                func.lower(Transaction.action_type) == action_type.lower()
            )
        ).all()

    def get_transactions_paginated(
        self,
        db: Session,
        *,
        user_id: Optional[int] = None,
        seller_id: Optional[int] = None,
        buyer_id: Optional[int] = None,
        organization_id: Optional[int] = None,
        item_id: Optional[int] = None,
        transaction_type: Optional[str] = None,
        status: Optional[str] = None,
        payment_status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
        sort_by: Optional[str] = "created_at",
        sort_order: Optional[str] = "desc"
    ) -> Tuple[List[Transaction], int]:
        page = max(1, page)
        page_size = max(1, min(page_size, 100))

        # Aliases for joins
        SellerUser = aliased(User, name="seller_user")
        BuyerUser = aliased(User, name="buyer_user")

        query = select(Transaction).outerjoin(Item, Transaction.item_id == Item.id)\
            .outerjoin(SellerUser, or_(Transaction.seller_id == SellerUser.id, Transaction.sender_id == SellerUser.id))\
            .outerjoin(BuyerUser, or_(Transaction.buyer_id == BuyerUser.id, Transaction.receiver_id == BuyerUser.id))\
            .outerjoin(Organization, Transaction.organization_id == Organization.id)

        # Access / Participant filters
        if user_id is not None:
            query = query.where(
                or_(
                    Transaction.seller_id == user_id,
                    Transaction.buyer_id == user_id,
                    Transaction.sender_id == user_id,
                    Transaction.receiver_id == user_id
                )
            )
        if seller_id is not None:
            query = query.where(or_(Transaction.seller_id == seller_id, Transaction.sender_id == seller_id))
        if buyer_id is not None:
            query = query.where(or_(Transaction.buyer_id == buyer_id, Transaction.receiver_id == buyer_id))
        if organization_id is not None:
            query = query.where(Transaction.organization_id == organization_id)
        if item_id is not None:
            query = query.where(Transaction.item_id == item_id)

        # Attribute filters
        if transaction_type:
            tt_lower = transaction_type.lower()
            query = query.where(
                or_(
                    func.lower(Transaction.transaction_type) == tt_lower,
                    func.lower(Transaction.action_type) == tt_lower
                )
            )
        if status:
            st_lower = status.lower()
            query = query.where(
                or_(
                    func.lower(Transaction.transaction_status) == st_lower,
                    func.lower(Transaction.status) == st_lower
                )
            )
        if payment_status:
            query = query.where(func.lower(Transaction.payment_status) == payment_status.lower())

        # Date range filter
        if start_date:
            query = query.where(Transaction.created_at >= start_date)
        if end_date:
            query = query.where(Transaction.created_at <= end_date)

        # Case-insensitive search across Transaction ID, Item name, Seller/Buyer names, Organization name
        if search and search.strip():
            term = f"%{search.strip()}%"
            search_conditions = [
                Item.title.ilike(term),
                Item.item_name.ilike(term),
                SellerUser.full_name.ilike(term),
                BuyerUser.full_name.ilike(term),
                Organization.name.ilike(term),
                cast(Transaction.id, String).ilike(term)
            ]
            query = query.where(or_(*search_conditions))

        # Count matching items using subquery
        subq = query.subquery()
        count_stmt = select(func.count()).select_from(subq)
        total_items = db.execute(count_stmt).scalar() or 0


        # Sorting
        sort_attr_map = {
            "date": Transaction.created_at,
            "created_at": Transaction.created_at,
            "created_date": Transaction.created_at,
            "amount": Transaction.total_amount,
            "total_amount": Transaction.total_amount,
            "agreed_price": Transaction.agreed_price,
            "quantity": Transaction.quantity,
            "status": Transaction.transaction_status,
            "transaction_status": Transaction.transaction_status,
        }

        sort_field_lower = (sort_by or "created_at").lower()
        sort_col = sort_attr_map.get(sort_field_lower, Transaction.created_at)

        if sort_order and sort_order.lower() == "asc":
            query = query.order_by(asc(sort_col), asc(Transaction.id))
        else:
            query = query.order_by(desc(sort_col), desc(Transaction.id))

        # Pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        transactions = db.execute(query).scalars().all()
        return list(transactions), total_items

transaction_repository = TransactionRepository()
