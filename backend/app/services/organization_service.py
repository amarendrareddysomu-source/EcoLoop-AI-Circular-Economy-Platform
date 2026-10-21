from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.organization_repository import organization_repository
from app.models.organization import Organization

class OrganizationService:
    def get_by_id(self, db: Session, org_id: int) -> Optional[Organization]:
        return organization_repository.get(db, org_id)

    def get_by_user_id(self, db: Session, user_id: int) -> Optional[Organization]:
        return organization_repository.get_by_user_id(db, user_id)

    def get_by_type(self, db: Session, org_type: str) -> List[Organization]:
        return organization_repository.get_by_type(db, org_type)

    def get_all(self, db: Session) -> List[Organization]:
        return organization_repository.get_all(db)

    def update_profile(self, db: Session, user_id: int, update_data: dict) -> Organization:
        org = self.get_by_user_id(db, user_id)
        if not org:
            from app.core.exceptions import NotFoundError
            raise NotFoundError("Organization profile not found for this account")
        return organization_repository.update(db, org, update_data)

organization_service = OrganizationService()

