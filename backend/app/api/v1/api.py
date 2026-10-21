from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, items, inventory, ai, transactions, ngo, recycling, admin, reports, analytics, algorithms, ml_models

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(items.router, prefix="/items", tags=["Items"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["Inventory Management"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI Engine"])
api_router.include_router(algorithms.router, prefix="/algorithms", tags=["Algorithm Suite"])
api_router.include_router(ml_models.router, prefix="/ml-models", tags=["Machine Learning Models Suite"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
api_router.include_router(ngo.router, prefix="/ngo", tags=["NGO Portal"])
api_router.include_router(recycling.router, prefix="/recycling", tags=["Recycling Center Portal"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin Control Panel"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports & Support"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics Dashboard"])





