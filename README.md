# AI-Powered Circular Economy Action Decision Support Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI: 0.110.0](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg)](https://fastapi.tiangolo.com/)
[![React: 18.2](https://img.shields.io/badge/React-18.2-61DAFB.svg)](https://reactjs.org/)
[![Vite: 5.4](https://img.shields.io/badge/Vite-5.4-646CFF.svg)](https://vitejs.dev/)
[![Docker: 24.0+](https://img.shields.io/badge/Docker-24.0+-2496ED.svg)](https://www.docker.com/)
[![Build: Passing](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()
[![Tests: 51/51 Passed](https://img.shields.io/badge/PyTest-51%2F51%20Passed-success.svg)]()

An enterprise-grade, full-stack decision support platform leveraging multi-model artificial intelligence, computer vision, and machine learning to optimize post-consumer material management along circular economy pathways: **Reuse, Repair, Donate, Sell, or Recycle**.

---

## Table of Contents
- [Executive Overview](#executive-overview)
- [Architecture & Key Features](#architecture--key-features)
- [Multi-Model AI Decision Engine](#multi-model-ai-decision-engine)
- [Role-Based Access Control (RBAC)](#role-based-access-control-rbac)
- [Technology Stack](#technology-stack)
- [Project Directory Structure](#project-directory-structure)
- [Quick Start & Local Setup](#quick-start--local-setup)
- [Docker Production Deployment](#docker-production-deployment)
- [Testing & Quality Assurance](#testing--quality-assurance)
- [Documentation Index](#documentation-index)
- [License & Acknowledgments](#license--acknowledgments)

---

## Executive Overview

Improper post-consumer waste management leads to accelerated landfill growth, raw material depletion, and severe environmental pollution. The **AI-Powered Circular Economy Action Decision Support Platform** addresses this challenge by providing individuals, NGOs, recycling facilities, and administrators with automated, data-driven disposition recommendations.

By uploading a single item image, users receive:
1. **Multimodal Computer Vision Classification** across 9 circular material categories.
2. **Transfer Learning Condition & Wear Assessment** (Excellent, Good, Fair, Poor).
3. **Random Forest Resale Value Prediction** trained on historical market depreciation curves.
4. **Landfill Diversion & CO₂ Carbon Offset Calculations**.
5. **Strategy-Driven Recommendation Routing** prioritizing high-value economic recovery and social donation over low-grade recycling.

---

## Architecture & Key Features

```
                      [ Client Web Browsers (React 18 / Vite) ]
                                         │
                                         ▼ (Port 80 / 443 HTTPS)
                           ┌───────────────────────────┐
                           │   Nginx Edge Proxy        │
                           │   (Reverse Proxy & SSL)   │
                           └─────────────┬─────────────┘
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 ▼                                               ▼
┌─────────────────────────┐                     ┌─────────────────────────┐
│  Frontend Container     │                     │  Backend Container      │
│  (Nginx Static Dist)    │                     │  (FastAPI + Uvicorn)    │
└─────────────────────────┘                     └────────────┬────────────┘
                                                             │
                                                             ▼
                                                ┌─────────────────────────┐
                                                │  PostgreSQL Container   │
                                                │  (Postgres 15 Alpine)   │
                                                └─────────────────────────┘
```

- **Clean Architecture & Repository Pattern**: Decoupled FastAPI controllers, service layers, SQLAlchemy repositories, and domain models.
- **Stateless Bearer JWT Authentication**: Access tokens, refresh tokens, password hashing via bcrypt, and secure revocation.
- **N+1 Query Elimination**: Standardized SQLAlchemy `joinedload` and `selectinload` queries.
- **Multi-Stage Containerization**: Minimal non-root Docker builds for Backend and Frontend static distribution.
- **Hardened Security**: Binary magic header byte inspection, SQL injection protection, XSS escaping, and CSP headers.

---

## Real PyTorch Computer Vision AI Pipeline

The platform runs a production-grade **PyTorch Computer Vision Deep Learning Pipeline** (`POST /api/v1/ai/classify-image`) leveraging pre-trained CNN architectures (MobileNetV3 / ResNet-50) mapped to a 35-class Circular Economy Waste Taxonomy (`CircularWasteNet-v2.5`):

```
User Uploads Image
       │
       ▼
Automated Validation (MIME, Magic Bytes, 10MB Limit, Structural Integrity)
       │
       ▼
Torchvision Preprocessing (256 Resize, 224 Center Crop, ImageNet Normalization)
       │
       ▼
PyTorch Neural Network Forward Pass ──▶ Grad-CAM Explainability Heatmap Overlay
       │
       ▼
Softmax Probability Distribution ──▶ Top-5 Class Predictions (Low-Conf Alert <60%)
       │
       ▼
Visual Wear & Condition Analyzer (Edge Sharpness, Texture Roughness, HSV Rust/Discoloration)
       │
       ▼
Trained Random Forest Resale Regressor ($0 for Plastic Cover/Bag/Bottle; Market Rate for Electronics)
       │
       ▼
LCA Carbon Offset & Sustainability Score (0-100 Gauge, CO₂ Saved kg, Waste Diverted kg)
       │
       ▼
Dynamic Circular Strategy Recommendation (Sell, Repair, Donate, Reuse, Recycle, Dispose Responsibly)
```

### AI Suite Architecture & Models

| AI Subsystem | Architecture / Algorithm | Function & Capabilities |
| :--- | :--- | :--- |
| **CV Classifier** | MobileNetV3 / ResNet-50 (PyTorch) | Predicts Top-1 and Top-5 class probabilities across 35 categories with low confidence alerts (< 60%). |
| **Grad-CAM Engine** | Gradient Class Activation Mapping | Generates visual attention heatmaps highlighting image regions influencing AI classification. |
| **Condition Analyzer** | Edge Sharpness & HSV Color Entropy | Analyzes cracks, tears, rust, discoloration, and surface wear defects to assign visual condition ratings. |
| **Price Regressor** | Scikit-Learn Random Forest Regressor | Models realistic resale values ($0 for disposable packaging/covers; market rates for laptops/phones). |
| **LCA Calculator** | Life Cycle Carbon LCA Factors | Computes CO₂ carbon offset (kg), landfill waste diverted (kg), and material recyclability %. |
| **Recommendation Engine** | Dynamic Strategy Pattern | Selects optimal circular pathway (**Sell, Repair, Donate, Reuse, Recycle, Dispose Responsibly**). |

---

## Role-Based Access Control (RBAC)

1. **Guest**: Public homepage, impact statistics, and circular economy metrics.
2. **User**: Item upload, AI inference trigger, personal impact tracking, and transaction management.
3. **NGO**: Donation claims queue, incoming inventory management, and community distribution logs.
4. **Recycling Center**: Recyclable material processing queue, processing status management, and capacity metrics.
5. **Admin / Super Admin**: System-wide analytics, user directory management, category performance, and audit logs.

---

## Technology Stack

- **Backend**: Python 3.11, FastAPI 0.110.0, SQLAlchemy 2.0.28, PyJWT 2.8.0, PyTest 9.1.1.
- **Frontend**: React 18.2, Vite 5.4, TailwindCSS 3.4, Lucide React, Recharts 2.12.
- **Machine Learning**: PyTorch 2.2, Torchvision 0.17, Scikit-Learn 1.4, Pillow 10.2, NumPy 1.26.
- **Database**: PostgreSQL 15 Alpine (Production), SQLite (Testing/Dev).
- **DevOps & Infrastructure**: Docker, Docker Compose, Nginx Alpine Edge Proxy, GitHub Actions CI/CD.

---

## Project Directory Structure

```text
/Users/akashreddy/Desktop/SE
├── ai_engine/                    # Standalone Multimodal AI Suite
│   ├── condition_predictor.py
│   ├── image_classifier.py
│   ├── price_predictor.py
│   ├── recommendation_engine.py
│   ├── sustainability_calculator.py
│   └── models_store/             # Serialized Scikit-Learn Models (.pkl)
├── backend/                      # FastAPI Backend Application
│   ├── app/
│   │   ├── api/v1/endpoints/     # REST API Route Controllers
│   │   ├── core/                 # Auth, Security, Database, Exceptions
│   │   ├── models/               # SQLAlchemy ORM Data Models
│   │   ├── repositories/         # Database Access Layer
│   │   ├── services/             # Business Logic & AI Integration
│   │   └── tests/                # 51 PyTest Automated Test Suites
│   ├── Dockerfile                # Multi-stage Python 3.11 Slim Build
│   └── requirements.txt          # Python Dependencies
├── frontend/                     # React 18 / Vite Web Frontend
│   ├── src/
│   │   ├── components/           # Reusable UI Controls & Layouts
│   │   ├── context/              # Auth & Theme Context Providers
│   │   ├── pages/                # Page Views & Portals
│   │   └── routes/               # Lazy-loaded App Route Definitions
│   ├── Dockerfile                # Multi-stage Nginx Static Build
│   └── vite.config.js            # Rollup Chunk Splitting Configuration
├── nginx/                        # Nginx Edge Proxy Configuration
│   ├── nginx.conf
│   └── conf.d/default.conf
├── scripts/                      # Operational & Backup Scripts
│   ├── backup_db.sh              # Automated PostgreSQL Backup Script
│   └── restore_db.sh             # Automated Database Restoration Script
├── .github/workflows/ci-cd.yml   # GitHub Actions CI/CD Pipeline
├── docker-compose.yml            # Multi-Container Orchestration File
├── PHASE_13_DEPLOYMENT_REPORT.md # Deployment & Infrastructure Report
├── DEPLOYMENT_GUIDE.md           # Step-by-Step Production Setup Guide
├── FINAL_PROJECT_REPORT.md       # Comprehensive Academic Thesis Report
├── UML_DIAGRAMS.md               # Complete System UML Diagrams
├── DATABASE_DOCUMENTATION.md     # Relational Database Schema Specification
├── TEST_REPORT.md                # Automated Testing & Security Audit Report
├── USER_MANUAL.md                # End-User Operational Manual
├── INSTALLATION_GUIDE.md        # System Installation & Setup Manual
└── PRESENTATION_CONTENT.md       # Academic Presentation Deck Content
```

---

## Quick Start & Local Setup

### Prerequisites
- Python `3.11+`
- Node.js `18+` & npm `9+`

### 1. Backend Setup
```bash
# Activate Virtual Environment
source backend/venv/bin/activate

# Run Automated Test Suite
pytest

# Start Backend Server
uvicorn backend.app.main:app --reload --port 8000
```
Backend server will start at `http://localhost:8000` with Swagger UI at `http://localhost:8000/docs`.

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend development server will launch at `http://localhost:5173`.

---

## Docker Production Deployment

To run the complete production stack (PostgreSQL, Backend, Frontend, and Nginx Reverse Proxy):

```bash
# Build and launch all containers
docker-compose up --build -d

# Verify container status
docker-compose ps
```

Access the application at `http://localhost` (or configured domain name).

---

## Testing & Quality Assurance

The codebase includes 51 automated PyTest test suites covering authentication, RBAC authorization, magic byte upload security, AI classification accuracy, price prediction bounds, transaction state machines, and environmental reports:

```bash
# Run pytest suite
./backend/venv/bin/pytest
```

**Result**: `51 passed in 19.07s (100% Pass Rate)`.

---

## Documentation Index

- [FINAL_PROJECT_REPORT.md](FINAL_PROJECT_REPORT.md): Complete academic thesis report.
- [UML_DIAGRAMS.md](UML_DIAGRAMS.md): Full Mermaid architectural and UML diagrams.
- [DATABASE_DOCUMENTATION.md](DATABASE_DOCUMENTATION.md): Relational schema, tables, indexes, and constraints.
- [TEST_REPORT.md](TEST_REPORT.md): Complete test suite analysis and security audit results.
- [USER_MANUAL.md](USER_MANUAL.md): Step-by-step user operational manual.
- [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md): Environment setup and installation instructions.
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md): Production cloud and Nginx deployment guide.
- [PRESENTATION_CONTENT.md](PRESENTATION_CONTENT.md): Presentation deck content for defense.

---

## License & Acknowledgments

This project is released under the **MIT License**. Created for the Advanced Software Engineering & AI Decision Systems Academic Curriculum (2026).
