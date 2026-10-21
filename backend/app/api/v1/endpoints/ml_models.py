"""
FastAPI Router for Machine Learning Algorithms Suite
File: backend/app/api/v1/endpoints/ml_models.py
"""

from typing import Dict, Any, List
from fastapi import APIRouter, status

from ai_engine.ml_models import (
    random_forest_algorithm,
    svm_algorithm,
    gradient_boosting_algorithm,
    knn_algorithm,
    mlp_neural_network_algorithm
)
from app.schemas.ml_models import (
    RandomForestRequest, RandomForestResponse,
    SVMRequest, SVMResponse,
    GradientBoostingRequest, GradientBoostingResponse,
    KNNRequest, KNNResponse,
    MLPRequest, MLPResponse
)

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
def list_ml_models() -> Dict[str, Any]:
    """
    Returns metadata and catalog of all 5 Machine Learning & AI algorithms implemented in the platform.
    """
    return {
        "platform": "AI-Powered Circular Economy Platform",
        "implemented_ml_algorithms_count": 5,
        "ml_algorithms": [
            {
                "id": "random_forest",
                "name": "Random Forest Classifier & Regressor Algorithm",
                "family": "Ensemble Bagging Decision Trees",
                "endpoint": "/api/v1/ml-models/random-forest"
            },
            {
                "id": "svm_rbf",
                "name": "Support Vector Machine (SVM) Algorithm with RBF Kernel",
                "family": "Kernelized Margin-Based Support Vector Classifier / SVR",
                "endpoint": "/api/v1/ml-models/svm"
            },
            {
                "id": "gradient_boosting",
                "name": "Gradient Boosting Machine (GBM / XGBoost) Algorithm",
                "family": "Sequential Additive Gradient Boosting",
                "endpoint": "/api/v1/ml-models/gradient-boosting"
            },
            {
                "id": "knn_distance",
                "name": "K-Nearest Neighbors (k-NN) Distance Algorithm",
                "family": "Non-Parametric Minkowski Distance Instance Learning",
                "endpoint": "/api/v1/ml-models/knn"
            },
            {
                "id": "mlp_neural_network",
                "name": "Multi-Layer Perceptron (MLP) Artificial Neural Network Algorithm",
                "family": "Deep Feed-Forward Neural Network (ReLU & Adam Optimizer)",
                "endpoint": "/api/v1/ml-models/mlp-neural-network"
            }
        ]
    }

@router.post("/random-forest", response_model=RandomForestResponse, status_code=status.HTTP_200_OK)
def run_random_forest(req: RandomForestRequest) -> RandomForestResponse:
    """
    Executes Machine Learning Algorithm 1: Random Forest Classifier & Regressor.
    """
    res = random_forest_algorithm.predict_item(
        category=req.category,
        original_price=req.original_price,
        age_years=req.age_years,
        condition=req.condition,
        weight_kg=req.weight_kg
    )
    return RandomForestResponse(**res)

@router.post("/svm", response_model=SVMResponse, status_code=status.HTTP_200_OK)
def run_svm(req: SVMRequest) -> SVMResponse:
    """
    Executes Machine Learning Algorithm 2: Support Vector Machine (SVM) with RBF Kernel.
    """
    res = svm_algorithm.predict(
        age_years=req.age_years,
        condition_score=req.condition_score,
        original_price=req.original_price
    )
    return SVMResponse(**res)

@router.post("/gradient-boosting", response_model=GradientBoostingResponse, status_code=status.HTTP_200_OK)
def run_gradient_boosting(req: GradientBoostingRequest) -> GradientBoostingResponse:
    """
    Executes Machine Learning Algorithm 3: Gradient Boosting Machine (GBM / XGBoost).
    """
    res = gradient_boosting_algorithm.predict(
        age_years=req.age_years,
        wear_index=req.wear_index,
        base_co2_factor=req.base_co2_factor
    )
    return GradientBoostingResponse(**res)

@router.post("/knn", response_model=KNNResponse, status_code=status.HTTP_200_OK)
def run_knn(req: KNNRequest) -> KNNResponse:
    """
    Executes Machine Learning Algorithm 4: K-Nearest Neighbors (k-NN) Distance Algorithm.
    """
    res = knn_algorithm.find_k_nearest(
        weight_kg=req.weight_kg,
        volume_m3=req.volume_m3,
        repairability_score=req.repairability_score,
        eco_points=req.eco_points,
        k=req.k_neighbors
    )
    return KNNResponse(**res)

@router.post("/mlp-neural-network", response_model=MLPResponse, status_code=status.HTTP_200_OK)
def run_mlp_neural_network(req: MLPRequest) -> MLPResponse:
    """
    Executes Machine Learning Algorithm 5: Multi-Layer Perceptron (MLP) Artificial Neural Network.
    """
    res = mlp_neural_network_algorithm.predict(
        weight_kg=req.weight_kg,
        age_years=req.age_years,
        condition_score=req.condition_score,
        original_price=req.original_price
    )
    return MLPResponse(**res)
