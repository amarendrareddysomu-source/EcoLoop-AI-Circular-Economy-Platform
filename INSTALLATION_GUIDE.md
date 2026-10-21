# Installation & Setup Guide

**Platform**: AI-Powered Circular Economy Action Decision Support Platform  
**Version**: 2.0.0  

---

## 1. System Requirements

### Hardware Requirements
- **CPU**: Dual-core 2.0 GHz or higher (x86_64 or ARM64)
- **RAM**: Minimum 4GB (8GB recommended for Docker containerization)
- **Disk**: 5GB free storage

### Software Requirements
- **Operating System**: macOS (12+), Ubuntu Linux (20.04/22.04 LTS), or Windows 11 (WSL2)
- **Python**: Version `3.11.x`
- **Node.js**: Version `18.x` or `20.x` & npm `9+`
- **Docker & Docker Compose**: `24.0+` (Optional for containerized deployment)

---

## 2. Local Virtual Environment Setup

### 2.1 Open Local Project Directory
Navigate directly into your local project root folder:
```bash
cd SE
```
*(Or use the absolute path to your local project folder)*

### 2.2 Backend Environment Setup
```bash
# 1. Create Python Virtual Environment
python3 -m venv backend/venv

# 2. Activate Virtual Environment
# macOS / Linux:
source backend/venv/bin/activate
# Windows PowerShell:
# .\backend\venv\Scripts\Activate.ps1

# 3. Upgrade Pip & Install Dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt
```

### 2.3 Frontend Environment Setup
```bash
cd frontend
npm install
cd ..
```

---

## 3. Environment Configuration

Copy `.env.development` to `.env` in the project root:

```bash
cp .env.development .env
```

Ensure `.env` contains the following key settings:

```env
PROJECT_NAME="AI-Powered Circular Economy Platform"
ENVIRONMENT="development"
DEBUG=true
PORT=8000

SECRET_KEY="dev-secret-key-circular-economy-local"
DATABASE_URL="sqlite:///./circular_economy.db"
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://127.0.0.1:5173","http://localhost:3000"]
UPLOAD_DIR="uploads"
MAX_UPLOAD_SIZE_MB=10

VITE_API_URL="http://localhost:8000"
```

---

## 4. Running the Application Locally

### 4.1 Start FastAPI Backend Server
```bash
# From project root directory:
source backend/venv/bin/activate
uvicorn backend.app.main:app --reload --port 8000
```
- Backend REST API will start at: `http://localhost:8000`
- Interactive Swagger UI: `http://localhost:8000/docs`
- OpenAPI Specification: `http://localhost:8000/api/v1/openapi.json`

### 4.2 Start React Frontend Server
Open a new terminal window:
```bash
cd frontend
npm run dev
```
- Frontend application will start at: `http://localhost:5173`

---

## 5. Docker Production Deployment

To run the complete production container stack (PostgreSQL, Backend, Frontend, Nginx Proxy):

```bash
# 1. Copy Production Environment Config
cp .env.production .env

# 2. Launch Docker Compose Stack
docker-compose up --build -d

# 3. Verify Container Status
docker-compose ps
```

The production application will be accessible at `http://localhost`.

---

## 6. Running Automated Tests

To execute the 89 automated PyTest test suites:

```bash
source backend/venv/bin/activate
PYTHONPATH=backend pytest backend/app/tests
```

All 89 test suites will pass 100% cleanly in ~42 seconds.
