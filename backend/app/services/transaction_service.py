import math
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.transaction import Transaction, TransactionStatus, PaymentStatus, TransactionType
from app.models.item import Item, ItemStatus
from app.models.user import User, UserRole
from app.repositories.transaction_repository import transaction_repository
from app.repositories.item_repository import item_repository
from app.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    PaginatedTransactionResponse
)
from app.core.deps import ADMIN_ROLES

class TransactionService:
    def _is_admin(self, user: User) -> bool:
        return user.role in ADMIN_ROLES or user.role == UserRole.ADMIN.value or user.role == UserRole.SUPER_ADMIN.value

    def _check_access_permission(self, tx: Transaction, user: User) -> None:
        if self._is_admin(user):
            return
        
        # Check participant match
        is_participant = (
            tx.seller_id == user.id or
            tx.buyer_id == user.id or
            tx.sender_id == user.id or
            tx.receiver_id == user.id
        )
        if is_participant:
            return

        # Check organization match
        if user.organization_id is not None and tx.organization_id == user.organization_id:
            return

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You do not have permission to view or manage this transaction."
        )

    def create_transaction(self, db: Session, current_user: User, tx_in: TransactionCreate) -> Transaction:
        item = item_repository.get(db, tx_in.item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with ID {tx_in.item_id} not found")

        tx_type = (tx_in.transaction_type or tx_in.action_type or "sale").lower()
        requested_qty = tx_in.quantity

        # Determine seller and buyer
        seller_id = tx_in.seller_id or tx_in.sender_id
        buyer_id = tx_in.buyer_id or tx_in.receiver_id

        if not seller_id and tx_type in ["sale", "sell", "donation", "donate", "recycling", "recycle", "transfer"]:
            seller_id = item.owner_id
        if not buyer_id and tx_type in ["purchase", "buy"]:
            buyer_id = current_user.id

        if not seller_id:
            seller_id = current_user.id

        org_id = tx_in.organization_id or current_user.organization_id or item.organization_id

        # Business Rule: Validate Stock Availability for Outgoing Operations
        outgoing_types = ["sale", "sell", "donation", "donate", "recycling", "recycle", "transfer"]
        if tx_type in outgoing_types:
            if item.quantity < requested_qty:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient inventory stock. Available: {item.quantity}, Requested: {requested_qty}"
                )

        unit_price = tx_in.unit_price if tx_in.unit_price is not None else (tx_in.agreed_price or item.price or item.estimated_price or 0.0)
        total_amount = tx_in.total_amount if tx_in.total_amount is not None else float(requested_qty * unit_price)

        co2_saved = float(item.co2_saved_kg * requested_qty)
        waste_diverted = float(item.waste_diverted_kg * requested_qty)

        tx_status = tx_in.transaction_status or tx_in.status or TransactionStatus.COMPLETED.value
        pay_status = tx_in.payment_status or (PaymentStatus.PAID.value if total_amount > 0 else PaymentStatus.NOT_APPLICABLE.value)

        # Atomic Execution of Transaction & Inventory Updates
        try:
            db_tx = Transaction(
                item_id=item.id,
                transaction_type=tx_type,
                action_type=tx_type,
                seller_id=seller_id,
                sender_id=seller_id,
                buyer_id=buyer_id,
                receiver_id=buyer_id,
                organization_id=org_id,
                quantity=requested_qty,
                unit_price=unit_price,
                total_amount=total_amount,
                agreed_price=total_amount,
                transaction_status=tx_status,
                status=tx_status,
                payment_status=pay_status,
                notes=tx_in.notes or "",
                co2_saved_kg=co2_saved,
                waste_diverted_kg=waste_diverted
            )

            # Apply stock updates if transaction status is Completed or Requested/Accepted
            active_statuses = [TransactionStatus.COMPLETED.value, TransactionStatus.ACCEPTED.value, TransactionStatus.REQUESTED.value]
            if tx_status in active_statuses:
                if tx_type in ["sale", "sell"]:
                    item.quantity = max(0, item.quantity - requested_qty)
                    if item.quantity == 0:
                        item.status = ItemStatus.SOLD.value
                elif tx_type in ["donation", "donate"]:
                    item.quantity = max(0, item.quantity - requested_qty)
                    if item.quantity == 0:
                        item.status = ItemStatus.DONATED.value
                elif tx_type in ["recycling", "recycle"]:
                    item.quantity = max(0, item.quantity - requested_qty)
                    if item.quantity == 0:
                        item.status = ItemStatus.RECYCLED.value
                elif tx_type in ["purchase", "buy"]:
                    item.quantity += requested_qty
                    if item.quantity > 0:
                        item.status = ItemStatus.AVAILABLE.value
                elif tx_type == "transfer":
                    item.quantity = max(0, item.quantity - requested_qty)
                    if buyer_id:
                        item.owner_id = buyer_id
                    if item.quantity == 0:
                        item.status = ItemStatus.SOLD.value

            db.add(item)
            db.add(db_tx)
            db.commit()
            db.refresh(db_tx)
            db.refresh(item)
            return db_tx
        except Exception as e:
            db.rollback()
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to process transaction: {str(e)}"
            )

    def get_transaction(self, db: Session, current_user: User, tx_id: int) -> Transaction:
        tx = transaction_repository.get(db, tx_id)
        if not tx:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Transaction with ID {tx_id} not found")
        self._check_access_permission(tx, current_user)
        return tx

    def list_transactions(
        self,
        db: Session,
        current_user: User,
        *,
        transaction_type: Optional[str] = None,
        status_filter: Optional[str] = None,
        payment_status: Optional[str] = None,
        organization_id: Optional[int] = None,
        user_id: Optional[int] = None,
        seller_id: Optional[int] = None,
        buyer_id: Optional[int] = None,
        item_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
        sort_by: Optional[str] = "created_at",
        sort_order: Optional[str] = "desc"
    ) -> PaginatedTransactionResponse:
        
        # RBAC Filtering
        if self._is_admin(current_user):
            filter_user_id = user_id
            filter_org_id = organization_id
        else:
            if current_user.organization_id is not None:
                filter_org_id = current_user.organization_id
                filter_user_id = user_id
            else:
                filter_user_id = current_user.id
                filter_org_id = None

        transactions, total_items = transaction_repository.get_transactions_paginated(
            db,
            user_id=filter_user_id,
            seller_id=seller_id,
            buyer_id=buyer_id,
            organization_id=filter_org_id,
            item_id=item_id,
            transaction_type=transaction_type,
            status=status_filter,
            payment_status=payment_status,
            start_date=start_date,
            end_date=end_date,
            search=search,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_order=sort_order
        )

        total_pages = math.ceil(total_items / page_size) if total_items > 0 else 0

        response_items = [TransactionResponse.model_validate(tx) for tx in transactions]

        return PaginatedTransactionResponse(
            items=response_items,
            page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages
        )

    def update_transaction(
        self,
        db: Session,
        current_user: User,
        tx_id: int,
        update_in: TransactionUpdate
    ) -> Transaction:
        tx = self.get_transaction(db, current_user, tx_id)
        update_dict = update_in.model_dump(exclude_unset=True)

        if "transaction_status" in update_dict or "status" in update_dict:
            st = update_dict.get("transaction_status") or update_dict.get("status")
            update_dict["transaction_status"] = st
            update_dict["status"] = st

        return transaction_repository.update(db, tx, update_dict)

    def cancel_transaction(self, db: Session, current_user: User, tx_id: int) -> Transaction:
        tx = self.get_transaction(db, current_user, tx_id)

        if tx.transaction_status == TransactionStatus.CANCELLED.value:
            return tx

        try:
            item = item_repository.get(db, tx.item_id)
            if item:
                # Restore stock if transaction was outgoing
                outgoing_types = ["sale", "sell", "donation", "donate", "recycling", "recycle", "transfer"]
                tx_type = (tx.transaction_type or tx.action_type or "").lower()
                if tx_type in outgoing_types:
                    item.quantity += tx.quantity
                    if item.quantity > 0:
                        item.status = ItemStatus.AVAILABLE.value
                elif tx_type in ["purchase", "buy"]:
                    item.quantity = max(0, item.quantity - tx.quantity)
                
                db.add(item)

            tx.transaction_status = TransactionStatus.CANCELLED.value
            tx.status = TransactionStatus.CANCELLED.value
            db.add(tx)
            db.commit()
            db.refresh(tx)
            return tx
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to cancel transaction: {str(e)}"
            )

    def delete_transaction(self, db: Session, current_user: User, tx_id: int) -> bool:
        tx = self.get_transaction(db, current_user, tx_id)
        self.cancel_transaction(db, current_user, tx_id)
        transaction_repository.delete(db, tx.id)
        return True

transaction_service = TransactionService()
