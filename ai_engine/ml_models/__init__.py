"""
AI-Powered Circular Economy Machine Learning Algorithms Package
Package: ai_engine/ml_models

Contains 5 explicit Machine Learning & Artificial Intelligence model implementations:
1. Random Forest Classifier & Regressor Algorithm
2. Support Vector Machine (SVM) Algorithm with RBF Kernel
3. Gradient Boosting Machine (GBM / XGBoost) Algorithm
4. K-Nearest Neighbors (k-NN) Distance Algorithm
5. Multi-Layer Perceptron (MLP) Artificial Neural Network Algorithm
"""

from ai_engine.ml_models.random_forest_model import random_forest_algorithm, RandomForestAlgorithm
from ai_engine.ml_models.svm_model import svm_algorithm, SupportVectorMachineAlgorithm
from ai_engine.ml_models.gradient_boosting_model import gradient_boosting_algorithm, GradientBoostingAlgorithm
from ai_engine.ml_models.knn_model import knn_algorithm, KNearestNeighborsAlgorithm
from ai_engine.ml_models.mlp_neural_network import mlp_neural_network_algorithm, MultiLayerPerceptronAlgorithm

__all__ = [
    "random_forest_algorithm",
    "RandomForestAlgorithm",
    "svm_algorithm",
    "SupportVectorMachineAlgorithm",
    "gradient_boosting_algorithm",
    "GradientBoostingAlgorithm",
    "knn_algorithm",
    "KNearestNeighborsAlgorithm",
    "mlp_neural_network_algorithm",
    "MultiLayerPerceptronAlgorithm"
]
