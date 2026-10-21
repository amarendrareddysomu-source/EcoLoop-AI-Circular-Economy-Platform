from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.user import User

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_role(self, db: Session, role: str) -> List[User]:
        return db.query(User).filter(User.role == role).all()

    def get_by_reset_token(self, db: Session, token: str) -> Optional[User]:
        return db.query(User).filter(User.reset_token == token).first()

    def get_by_verification_token(self, db: Session, token: str) -> Optional[User]:
        return db.query(User).filter(User.verification_token == token).first()

    def get_by_refresh_token(self, db: Session, token: str) -> Optional[User]:
        return db.query(User).filter(User.refresh_token == token).first()

user_repository = UserRepository()

