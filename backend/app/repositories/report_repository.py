from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.report import Report
from app.models.generated_report import GeneratedReport

class ReportRepository(BaseRepository[Report]):
    def __init__(self):
        super().__init__(Report)

    def get_by_reporter(self, db: Session, reporter_id: int) -> List[Report]:
        return db.query(Report).filter(Report.reporter_id == reporter_id).order_by(Report.created_at.desc()).all()

    def get_by_status(self, db: Session, status: str) -> List[Report]:
        return db.query(Report).filter(Report.status == status).order_by(Report.created_at.desc()).all()

class GeneratedReportRepository(BaseRepository[GeneratedReport]):
    def __init__(self):
        super().__init__(GeneratedReport)

    def get_by_user(self, db: Session, user_id: int) -> List[GeneratedReport]:
        return db.query(GeneratedReport).filter(GeneratedReport.user_id == user_id).order_by(GeneratedReport.created_at.desc()).all()

    def get_by_type_and_period(self, db: Session, report_type: str, period: str) -> List[GeneratedReport]:
        return db.query(GeneratedReport).filter(
            GeneratedReport.report_type == report_type,
            GeneratedReport.period == period
        ).order_by(GeneratedReport.created_at.desc()).all()

report_repository = ReportRepository()
generated_report_repository = GeneratedReportRepository()
