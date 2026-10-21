from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Any, Dict
from datetime import datetime

class ReportCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    description: str = Field(..., min_length=10)
    report_type: Optional[str] = "system_feedback"
    target_item_id: Optional[int] = None
    target_user_id: Optional[int] = None

class ReportUpdateStatus(BaseModel):
    status: str # Pending, In Review, Resolved, Dismissed
    admin_notes: Optional[str] = None

class ReportResponse(BaseModel):
    id: int
    reporter_id: int
    target_item_id: Optional[int] = None
    target_user_id: Optional[int] = None
    report_type: str
    title: str
    description: str
    status: str
    admin_notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# Phase 6 Report & Analytics Schemas

class ReportGenerateRequest(BaseModel):
    report_type: str = Field(default="sustainability", description="transactions, inventory, recycling, sustainability")
    period: str = Field(default="monthly", description="daily, weekly, monthly")
    export_format: Optional[str] = Field(default="json", description="json, csv, pdf")

class GeneratedReportResponse(BaseModel):
    id: int
    user_id: int
    title: str
    report_type: str
    period: str
    data_json: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CategoryStat(BaseModel):
    category: str
    item_count: int
    recycled_count: int
    co2_saved_kg: float
    waste_reduced_kg: float

class DashboardAnalyticsResponse(BaseModel):
    total_users: int
    total_items: int
    total_transactions: int
    total_recycled_items: int
    waste_reduced_kg: float
    co2_saved_kg: float
    category_statistics: List[CategoryStat]

class ChartDataset(BaseModel):
    label: str
    data: List[Any]

class ChartDataResponse(BaseModel):
    chart_type: str
    title: str
    labels: List[str]
    datasets: List[ChartDataset]