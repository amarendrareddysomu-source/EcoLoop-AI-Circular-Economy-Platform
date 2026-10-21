import os
import warnings

# Suppress scikit-learn version mismatch and parameter deprecation warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
try:
    from sklearn.exceptions import InconsistentVersionWarning, ConvergenceWarning
    warnings.filterwarnings("ignore", category=InconsistentVersionWarning)
    warnings.filterwarnings("ignore", category=ConvergenceWarning)
except ImportError:
    pass
warnings.filterwarnings("ignore", message=".*unpickle estimator.*")
warnings.filterwarnings("ignore", message=".*probability parameter.*")

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.core.database import Base, engine
from app.core.logging import logger
from app.core.exceptions import (
    AppException, 
    app_exception_handler, 
    validation_exception_handler, 
    sqlalchemy_exception_handler, 
    generic_exception_handler
)
from app.api.v1.api import api_router

# Import all models so Base.metadata knows about them
import app.models # noqa

# Create database tables automatically (for smooth execution with SQLite/Postgres)
# Create database tables automatically (for smooth execution with SQLite/Postgres)
import traceback

try:
    Base.metadata.create_all(bind=engine)
except Exception:
    traceback.print_exc()
    raise

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="2.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="""
### AI-Powered Circular Economy Action Decision Support Platform (Phase 2 Backend)

Comprehensive REST APIs for sustainable material management, AI item evaluation, donation routing, recycling queue processing, and environmental analytics.

#### Key Features:
- **JWT Authentication & RBAC**: Access Tokens, Refresh Tokens, Password Reset, Email Verification across 5 roles (`guest`, `user`, `ngo`, `recycling_center`, `admin`).
- **PostgreSQL & SQLAlchemy Architecture**: Repository Pattern & Clean Architecture.
- **AI Decision Engine**: Multimodal image classification & resale price prediction.
- **Transaction & Logistics Pipeline**: Circular state machine (Reuse, Repair, Donate, Recycle, Sell).
- **Secure Image Uploads**: Extension, MIME, and size validation.
"""
)

# Custom Middleware for Security Headers
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    # Exclude docs and openapi specification endpoints from CSP header so Swagger UI loads external CDN assets
    docs_paths = ["/docs", "/redoc", "/openapi.json", f"{settings.API_V1_STR}/openapi.json"]
    if not any(request.url.path.startswith(p) for p in docs_paths):
        response.headers["Content-Security-Policy"] = "default-src 'self'; img-src 'self' data: blob:; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
    return response

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Exception Handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Mount static upload directory
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/static/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Mount API v1 router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Health & Status"])
def root():
    return {
        "title": settings.PROJECT_NAME,
        "version": "2.0.0",
        "status": "online",
        "docs_url": "/docs",
        "api_v1": settings.API_V1_STR
    }

@app.get("/health", tags=["Health & Status"])
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
