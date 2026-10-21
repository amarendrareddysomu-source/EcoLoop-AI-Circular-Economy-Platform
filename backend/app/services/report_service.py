import io
import csv
import json
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from app.models.user import User
from app.models.item import Item
from app.models.transaction import Transaction
from app.models.report import Report, ReportStatus, ReportType
from app.models.generated_report import GeneratedReport
from app.repositories.report_repository import report_repository, generated_report_repository
from app.schemas.report import ReportCreate, ReportUpdateStatus, ReportGenerateRequest, GeneratedReportResponse
from app.services.analytics_service import analytics_service

class ReportService:
    # --- User Support & Issue Tickets ---
    def create_report(self, db: Session, reporter_id: int, report_in: ReportCreate) -> Report:
        db_report = Report(
            reporter_id=reporter_id,
            target_item_id=report_in.target_item_id,
            target_user_id=report_in.target_user_id,
            report_type=report_in.report_type or ReportType.SYSTEM_FEEDBACK.value,
            title=report_in.title,
            description=report_in.description,
            status=ReportStatus.PENDING.value
        )
        return report_repository.create(db, db_report)

    def list_user_reports(self, db: Session, user_id: int) -> List[Report]:
        return report_repository.get_by_reporter(db, user_id)

    def list_all_reports(self, db: Session, status_filter: Optional[str] = None) -> List[Report]:
        if status_filter:
            return report_repository.get_by_status(db, status_filter)
        return report_repository.get_all(db)

    def get_report(self, db: Session, report_id: int) -> Report:
        report = report_repository.get(db, report_id)
        if not report:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
        return report

    def update_report_status(self, db: Session, report_id: int, status_update: ReportUpdateStatus) -> Report:
        report = self.get_report(db, report_id)
        report.status = status_update.status
        if status_update.admin_notes:
            report.admin_notes = status_update.admin_notes
        db.add(report)
        db.commit()
        db.refresh(report)
        return report

    def delete_report(self, db: Session, report_id: int) -> bool:
        report = self.get_report(db, report_id)
        report_repository.delete(db, report.id)
        return True

    # --- System Analytical Report Generation & Storage ---
    def generate_report(self, db: Session, current_user: User, req: ReportGenerateRequest) -> GeneratedReport:
        report_type = req.report_type.lower()
        period = req.period.lower()

        if report_type not in ["transactions", "inventory", "recycling", "sustainability"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid report_type '{report_type}'. Must be one of: transactions, inventory, recycling, sustainability")

        if period not in ["daily", "weekly", "monthly"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid period '{period}'. Must be one of: daily, weekly, monthly")

        now = datetime.utcnow()
        if period == "daily":
            start_date = now - timedelta(days=1)
        elif period == "weekly":
            start_date = now - timedelta(weeks=1)
        else:
            start_date = now - timedelta(days=30)

        report_data: Dict[str, Any] = {
            "period": period,
            "report_type": report_type,
            "generated_at": now.isoformat(),
            "generated_by": current_user.full_name
        }

        if report_type == "transactions":
            txs = db.execute(
                select(Transaction).where(Transaction.created_at >= start_date).order_by(Transaction.created_at.desc())
            ).scalars().all()
            report_data["total_records"] = len(txs)
            report_data["total_amount"] = sum(t.total_amount for t in txs)
            report_data["rows"] = [
                {
                    "id": t.id,
                    "type": t.transaction_type or t.action_type or "sale",
                    "item_id": t.item_id,
                    "quantity": t.quantity,
                    "unit_price": t.unit_price,
                    "total_amount": t.total_amount,
                    "status": t.transaction_status or t.status,
                    "created_at": t.created_at.isoformat() if t.created_at else ""
                }
                for t in txs[:50]
            ]
        elif report_type == "inventory":
            items = db.execute(
                select(Item).where(Item.created_at >= start_date).order_by(Item.created_at.desc())
            ).scalars().all()
            report_data["total_records"] = len(items)
            report_data["total_quantity"] = sum(i.quantity for i in items)
            report_data["rows"] = [
                {
                    "id": i.id,
                    "name": i.item_name or i.title,
                    "category": i.category,
                    "quantity": i.quantity,
                    "unit": i.unit,
                    "price": i.price,
                    "condition": i.condition,
                    "status": i.status,
                    "created_at": i.created_at.isoformat() if i.created_at else ""
                }
                for i in items[:50]
            ]
        elif report_type == "recycling":
            recycled_items = db.execute(
                select(Item).where(
                    or_(func.lower(Item.status) == "recycled", func.lower(Item.status) == "pending recycling")
                )
            ).scalars().all()
            report_data["total_records"] = len(recycled_items)
            report_data["waste_diverted_kg"] = sum(i.waste_diverted_kg for i in recycled_items)
            report_data["rows"] = [
                {
                    "id": i.id,
                    "name": i.item_name or i.title,
                    "category": i.category,
                    "quantity": i.quantity,
                    "status": i.status,
                    "waste_diverted_kg": i.waste_diverted_kg,
                    "created_at": i.created_at.isoformat() if i.created_at else ""
                }
                for i in recycled_items[:50]
            ]
        elif report_type == "sustainability":
            overview = analytics_service.get_dashboard_analytics(db)
            report_data["co2_saved_kg"] = overview.co2_saved_kg
            report_data["waste_reduced_kg"] = overview.waste_reduced_kg
            report_data["total_recycled_items"] = overview.total_recycled_items
            report_data["category_stats"] = [cs.model_dump() for cs in overview.category_statistics]

        db_report = GeneratedReport(
            user_id=current_user.id,
            title=f"{period.capitalize()} {report_type.capitalize()} Report",
            report_type=report_type,
            period=period,
            data_json=json.dumps(report_data)
        )
        return generated_report_repository.create(db, db_report)

    def get_user_generated_reports(self, db: Session, user_id: int) -> List[GeneratedReport]:
        return generated_report_repository.get_by_user(db, user_id)

    # --- CSV Export ---
    def export_csv(self, db: Session, report_type: str = "sustainability", period: str = "monthly") -> str:
        output = io.StringIO()
        writer = csv.writer(output)

        report_type = report_type.lower()
        if report_type == "transactions":
            writer.writerow(["Transaction ID", "Type", "Item ID", "Seller ID", "Buyer ID", "Quantity", "Unit Price ($)", "Total Amount ($)", "Status", "Created Date"])
            txs = db.execute(select(Transaction).order_by(Transaction.created_at.desc())).scalars().all()
            for t in txs:
                writer.writerow([t.id, t.transaction_type or t.action_type, t.item_id, t.seller_id or t.sender_id, t.buyer_id or t.receiver_id, t.quantity, t.unit_price, t.total_amount, t.transaction_status or t.status, t.created_at])
        elif report_type == "inventory":
            writer.writerow(["Item ID", "Item Name", "Category", "Quantity", "Unit", "Price ($)", "Condition", "Status", "CO2 Saved (kg)", "Waste Diverted (kg)", "Created Date"])
            items = db.execute(select(Item).order_by(Item.created_at.desc())).scalars().all()
            for i in items:
                writer.writerow([i.id, i.item_name or i.title, i.category, i.quantity, i.unit, i.price, i.condition, i.status, i.co2_saved_kg, i.waste_diverted_kg, i.created_at])
        elif report_type == "recycling":
            writer.writerow(["Item ID", "Item Name", "Category", "Quantity", "Unit", "Status", "Recommended Action", "Waste Diverted (kg)", "Created Date"])
            items = db.execute(
                select(Item).where(or_(func.lower(Item.status) == "recycled", func.lower(Item.status) == "pending recycling"))
            ).scalars().all()
            for i in items:
                writer.writerow([i.id, i.item_name or i.title, i.category, i.quantity, i.unit, i.status, i.recommended_action, i.waste_diverted_kg, i.created_at])
        else: # sustainability
            writer.writerow(["Metric Name", "Value", "Unit", "Description"])
            overview = analytics_service.get_dashboard_analytics(db)
            writer.writerow(["Carbon Footprint Reduction", overview.co2_saved_kg, "kg CO2e", "Total carbon emissions prevented through reuse & recycling"])
            writer.writerow(["Waste Reduction", overview.waste_reduced_kg, "kg", "Total waste diverted from landfills"])
            writer.writerow(["Total Recycled Items", overview.total_recycled_items, "items", "Count of processed recycled materials"])
            writer.writerow(["Total Registered Items", overview.total_items, "items", "Total active catalog inventory items"])
            writer.writerow(["Total Completed Transactions", overview.total_transactions, "transactions", "Circular marketplace transaction volume"])

        return output.getvalue()

    # --- PDF Export ---
    def export_pdf(self, db: Session, report_type: str = "sustainability", period: str = "monthly") -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontSize=18,
            leading=22,
            textColor=colors.HexColor('#1E293B'),
            spaceAfter=12
        )
        subtitle_style = ParagraphStyle(
            'ReportSubtitle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#64748B'),
            spaceAfter=18
        )

        elements = []
        report_title = f"AI Circular Economy Platform — {period.capitalize()} {report_type.capitalize()} Report"
        elements.append(Paragraph(report_title, title_style))
        elements.append(Paragraph(f"Generated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}", subtitle_style))
        elements.append(Spacer(1, 10))

        report_type = report_type.lower()
        if report_type == "transactions":
            txs = db.execute(select(Transaction).order_by(Transaction.created_at.desc()).limit(30)).scalars().all()
            data = [["ID", "Type", "Item ID", "Qty", "Price", "Total", "Status"]]
            for t in txs:
                data.append([str(t.id), str(t.transaction_type or t.action_type or "sale"), str(t.item_id), str(t.quantity), f"${t.unit_price:.2f}", f"${t.total_amount:.2f}", str(t.transaction_status or t.status)])
        elif report_type == "inventory":
            items = db.execute(select(Item).order_by(Item.created_at.desc()).limit(30)).scalars().all()
            data = [["ID", "Name", "Category", "Qty", "Price", "Condition", "Status"]]
            for i in items:
                data.append([str(i.id), (i.item_name or i.title)[:20], str(i.category), str(i.quantity), f"${i.price:.2f}", str(i.condition), str(i.status)])
        elif report_type == "recycling":
            items = db.execute(select(Item).where(or_(func.lower(Item.status) == "recycled", func.lower(Item.status) == "pending recycling")).limit(30)).scalars().all()
            data = [["ID", "Name", "Category", "Qty", "Waste Diverted", "Status"]]
            for i in items:
                data.append([str(i.id), (i.item_name or i.title)[:20], str(i.category), str(i.quantity), f"{i.waste_diverted_kg:.1f} kg", str(i.status)])
        else: # sustainability
            overview = analytics_service.get_dashboard_analytics(db)
            data = [
                ["Sustainability Metric", "Value", "Unit"],
                ["Carbon Footprint Reduction", f"{overview.co2_saved_kg:.2f}", "kg CO2e"],
                ["Waste Reduction Statistics", f"{overview.waste_reduced_kg:.2f}", "kg"],
                ["Total Recycled Items", str(overview.total_recycled_items), "items"],
                ["Total Platform Items", str(overview.total_items), "items"],
                ["Total Transactions Count", str(overview.total_transactions), "transactions"]
            ]

        t_table = Table(data, colWidths=None)
        t_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8FAFC')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ]))
        elements.append(t_table)

        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()

report_service = ReportService()
