from typing import List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.item import Item, ItemStatus
from app.models.transaction import Transaction
from app.schemas.report import (
    DashboardAnalyticsResponse,
    CategoryStat,
    ChartDataResponse,
    ChartDataset
)

class AnalyticsService:
    def get_dashboard_analytics(self, db: Session) -> DashboardAnalyticsResponse:
        # Aggregates using SQLAlchemy 2.0
        total_users = db.execute(select(func.count(User.id))).scalar() or 0
        total_items = db.execute(select(func.count(Item.id))).scalar() or 0
        total_transactions = db.execute(select(func.count(Transaction.id))).scalar() or 0

        # Recycled items count
        recycled_items_stmt = select(func.count(Item.id)).where(
            or_(
                func.lower(Item.status) == "recycled",
                func.lower(Item.status) == "pending recycling"
            )
        )
        total_recycled_items = db.execute(recycled_items_stmt).scalar() or 0

        # CO2 saved & Waste reduced sums
        item_co2 = db.execute(select(func.coalesce(func.sum(Item.co2_saved_kg), 0.0))).scalar() or 0.0
        tx_co2 = db.execute(select(func.coalesce(func.sum(Transaction.co2_saved_kg), 0.0))).scalar() or 0.0
        co2_saved_kg = round(float(item_co2 + tx_co2), 2)

        item_waste = db.execute(select(func.coalesce(func.sum(Item.waste_diverted_kg), 0.0))).scalar() or 0.0
        tx_waste = db.execute(select(func.coalesce(func.sum(Transaction.waste_diverted_kg), 0.0))).scalar() or 0.0
        waste_reduced_kg = round(float(item_waste + tx_waste), 2)

        # Category-wise statistics
        categories_query = db.execute(
            select(
                Item.category,
                func.count(Item.id).label("item_count"),
                func.coalesce(func.sum(Item.co2_saved_kg), 0.0).label("co2_sum"),
                func.coalesce(func.sum(Item.waste_diverted_kg), 0.0).label("waste_sum")
            ).group_by(Item.category)
        ).all()

        category_stats = []
        for cat, item_cnt, c_sum, w_sum in categories_query:
            recycled_cnt = db.execute(
                select(func.count(Item.id)).where(
                    Item.category == cat,
                    or_(func.lower(Item.status) == "recycled", func.lower(Item.status) == "pending recycling")
                )
            ).scalar() or 0

            category_stats.append(
                CategoryStat(
                    category=cat,
                    item_count=item_cnt,
                    recycled_count=recycled_cnt,
                    co2_saved_kg=round(float(c_sum), 2),
                    waste_reduced_kg=round(float(w_sum), 2)
                )
            )

        return DashboardAnalyticsResponse(
            total_users=total_users,
            total_items=total_items,
            total_transactions=total_transactions,
            total_recycled_items=total_recycled_items,
            waste_reduced_kg=waste_reduced_kg,
            co2_saved_kg=co2_saved_kg,
            category_statistics=category_stats
        )

    def get_transaction_trends_chart(self, db: Session, days: int = 7) -> ChartDataResponse:
        now = datetime.utcnow()
        start_date = now - timedelta(days=days - 1)

        dates = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]
        volume_data = []
        amount_data = []

        for d_str in dates:
            d_start = datetime.strptime(d_str, "%Y-%m-%d")
            d_end = d_start + timedelta(days=1)

            count_val = db.execute(
                select(func.count(Transaction.id)).where(
                    Transaction.created_at >= d_start,
                    Transaction.created_at < d_end
                )
            ).scalar() or 0

            amount_val = db.execute(
                select(func.coalesce(func.sum(Transaction.total_amount), 0.0)).where(
                    Transaction.created_at >= d_start,
                    Transaction.created_at < d_end
                )
            ).scalar() or 0.0

            volume_data.append(count_val)
            amount_data.append(round(float(amount_val), 2))

        return ChartDataResponse(
            chart_type="line",
            title="Transaction Volume & Amount Trends",
            labels=dates,
            datasets=[
                ChartDataset(label="Transaction Count", data=volume_data),
                ChartDataset(label="Total Amount ($)", data=amount_data)
            ]
        )

    def get_category_distribution_chart(self, db: Session) -> ChartDataResponse:
        results = db.execute(
            select(Item.category, func.count(Item.id)).group_by(Item.category)
        ).all()

        labels = [r[0] for r in results]
        counts = [r[1] for r in results]

        if not labels:
            labels = ["Battery", "Biological", "Cardboard", "Clothes", "Glass", "Metal", "Paper", "Plastic", "Shoes", "Trash"]
            counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        return ChartDataResponse(
            chart_type="bar",
            title="Item Categories Distribution",
            labels=labels,
            datasets=[ChartDataset(label="Item Count", data=counts)]
        )

    def get_recycling_distribution_chart(self, db: Session) -> ChartDataResponse:
        statuses = ["Available", "Pending Recycling", "Recycled", "Donated", "Sold"]
        counts = []

        for st in statuses:
            c = db.execute(
                select(func.count(Item.id)).where(func.lower(Item.status) == st.lower())
            ).scalar() or 0
            counts.append(c)

        return ChartDataResponse(
            chart_type="pie",
            title="Recycling & Item Lifecycle Distribution",
            labels=statuses,
            datasets=[ChartDataset(label="Item Distribution", data=counts)]
        )

    def get_sustainability_trends_chart(self, db: Session, months: int = 6) -> ChartDataResponse:
        now = datetime.utcnow()
        month_labels = []
        co2_data = []
        waste_data = []

        for i in range(months - 1, -1, -1):
            m_date = now - timedelta(days=i * 30)
            m_str = m_date.strftime("%b %Y")
            month_labels.append(m_str)

            m_start = datetime(m_date.year, m_date.month, 1)
            next_m = m_date.month % 12 + 1
            next_y = m_date.year + (1 if m_date.month == 12 else 0)
            m_end = datetime(next_y, next_m, 1)

            c_val = db.execute(
                select(func.coalesce(func.sum(Item.co2_saved_kg), 0.0)).where(
                    Item.created_at >= m_start, Item.created_at < m_end
                )
            ).scalar() or 0.0

            w_val = db.execute(
                select(func.coalesce(func.sum(Item.waste_diverted_kg), 0.0)).where(
                    Item.created_at >= m_start, Item.created_at < m_end
                )
            ).scalar() or 0.0

            co2_data.append(round(float(c_val), 2))
            waste_data.append(round(float(w_val), 2))

        return ChartDataResponse(
            chart_type="line",
            title="Monthly Sustainability Impact Trends",
            labels=month_labels,
            datasets=[
                ChartDataset(label="CO2 Saved (kg)", data=co2_data),
                ChartDataset(label="Waste Diverted (kg)", data=waste_data)
            ]
        )

analytics_service = AnalyticsService()
