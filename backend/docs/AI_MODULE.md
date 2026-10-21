# AI Intelligence Module Documentation

## Overview
The **AI Intelligence Module** powers the AI-Powered Circular Economy Platform. It provides machine learning inference engines for:
1. **Sustainability Score Prediction**
2. **Resale Price Estimation** (Scikit-Learn Random Forest ML Model)
3. **Item Condition Classification**
4. **Circular Action Recommendation Engine**

---

## Package Architecture (`app/ml/`)

```text
backend/app/ml/
├── __init__.py
├── preprocessing/
│   └── preprocessing.py     # Feature normalization, categorical encoding, scaling
├── training/
│   └── trainer.py           # Random Forest Model training & serialization
└── inference/
    ├── model_loader.py      # Thread-safe weights loader with fallback
    └── predictor.py         # ML inference engines for price, condition, sustainability & recommendations
```

---

## Inference Workflow

1. **Client Request**: Client issues a JSON payload or image upload to `/api/v1/ai/*`.
2. **Preprocessing**: `DataPreprocessor` normalizes text, maps categorical string inputs, extracts numerical feature vectors, and computes condition multipliers.
3. **Model Loader**: `ModelLoader` retrieves pre-trained models (`.joblib` artifacts) or applies pre-tuned heuristic ML models.
4. **Predictor Execution**: `MLPredictor` computes predictions:
   - **Resale Price**: Computed via `RandomForestRegressor` and demand factor adjustments.
   - **Sustainability Score**: Evaluates condition wear, material recyclability, item weight, and reuse potential (scored 0–100).
   - **Condition Classification**: Synthesizes age, usage level, and user inputs into condition ratings (`Excellent`, `Good`, `Fair`, `Poor`).
   - **Circular Recommendations**: Evaluates optimal action (`Reuse`, `Repair`, `Donate`, `Sell`, `Recycle`) and suggests recycling methods & local NGO routing.
5. **AILog Audit**: Every inference execution is logged into the `ai_logs` PostgreSQL/SQLite database table.

---

## API Endpoints & Payloads

### 1. Sustainability Score Prediction
`POST /api/v1/ai/sustainability-score`

**Request Payload:**
```json
{
  "category": "Furniture",
  "material": "wood",
  "condition": "Excellent",
  "weight_kg": 15.5,
  "reuse_potential": "High"
}
```

**Response Payload:**
```json
{
  "sustainability_score": 88.5,
  "environmental_impact_category": "Exceptional",
  "recommendation": "Optimal circular candidate for immediate reuse and high-impact donation."
}
```

### 2. Resale Price Prediction
`POST /api/v1/ai/predict-price`

**Request Payload:**
```json
{
  "category": "Electronics",
  "brand": "Apple",
  "age_years": 2.0,
  "condition": "Good",
  "original_price": 1000.0,
  "market_factors": { "demand_level": "high" }
}
```

**Response Payload:**
```json
{
  "predicted_resale_price": 598.0,
  "confidence": 0.88,
  "min_price": 508.3,
  "max_price": 687.7
}
```

### 3. Condition Prediction
`POST /api/v1/ai/predict-condition`

**Request Payload:**
```json
{
  "age_years": 0.5,
  "usage_level": "Low",
  "user_stated_condition": "Excellent"
}
```

**Response Payload:**
```json
{
  "predicted_condition": "Excellent",
  "confidence": 0.95
}
```

### 4. Circular Recommendation Engine
`POST /api/v1/ai/recommend`

**Request Payload:**
```json
{
  "category": "Electronics",
  "condition": "Fair",
  "age_years": 3.0,
  "estimated_price": 150.0
}
```

**Response Payload:**
```json
{
  "recommended_action": "Repair",
  "action_reasoning": "Device is in Fair condition with residual resale value. Refurbishment will extend lifetime.",
  "reuse_options": [
    "Direct marketplace listing for peer-to-peer sale",
    "Local community sharing & borrowing network"
  ],
  "recycling_methods": [
    "Certified e-waste component recovery"
  ],
  "suitable_buyers_ngos": [
    "Green Earth Circular NGO",
    "EcoTech Recycling Center"
  ],
  "sustainability_actions": [
    "Upload detailed photographs to increase buyer trust",
    "Choose local pickup to eliminate shipping carbon emissions"
  ]
}
```

---

## Model Training & Serialization

To re-train the Random Forest model and save serialized weights:

```python
from app.ml.training.trainer import trainer

trainer.train_price_model(output_path="app/ml/models/price_model.joblib")
```
