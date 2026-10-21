from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_active_user, require_role
from app.schemas.report import (
    ReportCreate,
    ReportResponse,
    ReportUpdateStatus,
    ReportGenerateRequest,
    GeneratedReportResponse
)
from app.services.report_service import report_service
from app.models.user import User, UserRole

router = APIRouter()

# --- System Analytical Reports & Export Features ---

@router.post(
    "/generate",
    response_model=GeneratedReportResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate and store an analytical report (daily, weekly, monthly)",
    description="Generates an analytical summary for transactions, inventory, recycling, or sustainability metrics, saving it to database."
)
def generate_report(
    req: ReportGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    tx_report = report_service.generate_report(db, current_user, req)
    return GeneratedReportResponse.model_validate(tx_report)

@router.get(
    "/generated",
    response_model=List[GeneratedReportResponse],
    summary="List generated analytical reports for current user"
)
def list_generated_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    reports = report_service.get_user_generated_reports(db, current_user.id)
    return [GeneratedReportResponse.model_validate(r) for r in reports]

@router.get(
    "/export/csv",
    summary="Export report as CSV file",
    description="Returns a downloadable CSV file containing transactions, inventory, recycling, or sustainability metrics."
)
def export_report_csv(
    report_type: str = Query("sustainability", description="transactions, inventory, recycling, sustainability"),
    period: str = Query("monthly", description="daily, weekly, monthly"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    csv_data = report_service.export_csv(db, report_type=report_type, period=period)
    filename = f"{report_type}_{period}_report.csv"
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get(
    "/export/pdf",
    summary="Export report as PDF file",
    description="Returns a downloadable PDF report formatted with reportlab tables and headers."
)
def export_report_pdf(
    report_type: str = Query("sustainability", description="transactions, inventory, recycling, sustainability"),
    period: str = Query("monthly", description="daily, weekly, monthly"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    pdf_bytes = report_service.export_pdf(db, report_type=report_type, period=period)
    filename = f"{report_type}_{period}_report.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# --- User Support & Issue Tickets ---

@router.post("/", response_model=ReportResponse, status_code=status.HTTP_201_CREATED, summary="Submit a new report or system feedback")
def create_report(
    report_in: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return report_service.create_report(db, current_user.id, report_in)

@router.get("/my-reports", response_model=List[ReportResponse], summary="List reports submitted by current logged-in user")
def list_my_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return report_service.list_user_reports(db, current_user.id)

@router.get("/", response_model=List[ReportResponse], summary="List all reports (Admin only)")
def list_all_reports(
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN.value]))
):
    return report_service.list_all_reports(db, status_filter=status_filter)

@router.get("/{report_id}", response_model=ReportResponse, summary="Get report details by ID")
def get_report_by_id(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return report_service.get_report(db, report_id)

@router.put("/{report_id}/status", response_model=ReportResponse, summary="Update report resolution status (Admin only)")
def update_report_status(
    report_id: int,
    status_update: ReportUpdateStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN.value]))
):
    return report_service.update_report_status(db, report_id, status_update)

@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete report (Admin only)")
def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN.value]))
):
    report_service.delete_report(db, report_id)
    return None
