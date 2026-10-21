from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.organization import Organization

class OrganizationRepository(BaseRepository[Organization]):
    def __init__(self):
        super().__init__(Organization)

    def get_by_user_id(self, db: Session, user_id: int) -> Optional[Organization]:
        return db.query(Organization).filter(Organization.user_id == user_id).first()

    def get_by_type(self, db: Session, org_type: str) -> List[Organization]:
        return db.query(Organization).filter(Organization.org_type == org_type).all()

organization_repository = OrganizationRepository()
