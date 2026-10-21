from pydantic import BaseModel
from typing import List, Dict, Any

class SystemStatsResponse(BaseModel):
    total_users: int
    total_ngos: int
    total_recycling_centers: int
    total_items_uploaded: int
    total_co2_saved_kg: float
    total_waste_diverted_kg: float
    total_transactions: int
    category_distribution: Dict[str, int]
    action_recommendation_distribution: Dict[str, int]
    recent_ai_logs_count: int
