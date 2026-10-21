from typing import List
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.ai_log import AILog

class AILogRepository(BaseRepository[AILog]):
    def __init__(self):
        super().__init__(AILog)

    def get_recent_logs(self, db: Session, limit: int = 50) -> List[AILog]:
        return db.query(AILog).order_by(AILog.created_at.desc()).limit(limit).all()

ai_log_repository = AILogRepository()
