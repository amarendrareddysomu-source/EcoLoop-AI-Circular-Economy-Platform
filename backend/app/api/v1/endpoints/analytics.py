from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.schemas.report import DashboardAnalyticsResponse, ChartDataResponse
from app.services.analytics_service import analytics_service

router = APIRouter()

@router.get(
    "/dashboard",
    response_model=DashboardAnalyticsResponse,
    summary="Get overall platform analytics overview",
    description="Retrieve high-level statistics: total users, items, transactions, recycled items, waste reduced (kg), CO2 saved (kg), and category breakdown."
)
def get_dashboard_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return analytics_service.get_dashboard_analytics(db)

@router.get(
    "/charts/transaction-trends",
    response_model=ChartDataResponse,
    summary="Get transaction trends line chart data"
)
def get_transaction_trends_chart(
    days: int = Query(7, ge=1, le=365, description="Number of past days"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return analytics_service.get_transaction_trends_chart(db, days=days)

@router.get(
    "/charts/category-distribution",
    response_model=ChartDataResponse,
    summary="Get item category distribution bar chart data"
)
def get_category_distribution_chart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return analytics_service.get_category_distribution_chart(db)

@router.get(
    "/charts/recycling-distribution",
    response_model=ChartDataResponse,
    summary="Get recycling distribution pie chart data"
)
def get_recycling_distribution_chart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return analytics_service.get_recycling_distribution_chart(db)

@router.get(
    "/charts/sustainability-trends",
    response_model=ChartDataResponse,
    summary="Get monthly sustainability trends line chart data"
)
def get_sustainability_trends_chart(
    months: int = Query(6, ge=1, le=24, description="Number of past months"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return analytics_service.get_sustainability_trends_chart(db, months=months)
