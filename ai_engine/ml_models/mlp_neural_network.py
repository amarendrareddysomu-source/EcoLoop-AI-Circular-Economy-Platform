"""
ML Algorithm 5: Multi-Layer Perceptron (MLP) Artificial Neural Network Algorithm
File: ai_engine/ml_models/mlp_neural_network.py

Implements Feed-Forward Multi-Layer Perceptron (MLP) Artificial Neural Network Architecture.
Features:
- Input Layer: Normalized item metadata features
- Hidden Layers: (64, 32) Dense nodes with ReLU activation functions
- Optimization: Adam Optimizer with Backpropagation
- Loss Function: Cross-Entropy & Mean Squared Error
"""

import warnings
from typing import Dict, Any, List
import numpy as np
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.exceptions import ConvergenceWarning

warnings.filterwarnings("ignore", category=ConvergenceWarning)

class MultiLayerPerceptronAlgorithm:
    """
    Multi-Layer Perceptron (MLP) Artificial Neural Network Algorithm wrapper.
    """

    def __init__(self):
        self.scaler = StandardScaler()
        self.mlp_classifier = MLPClassifier(
            hidden_layer_sizes=(64, 32),
            activation="relu",
            solver="adam",
            max_iter=500,
            random_state=42
        )
        self.mlp_regressor = MLPRegressor(
            hidden_layer_sizes=(64, 32),
            activation="relu",
            solver="adam",
            max_iter=500,
            random_state=42
        )
        self.is_trained = False
        self._bootstrap_train()

    def _bootstrap_train(self):
        """
        Trains Multi-Layer Perceptron Neural Network models on circular economy feature dataset.
        Input features: [weight_kg, age_years, condition_score, original_price]
        """
        X, y_cls, y_reg = [], [], []
        cond_scores = {"Excellent": 95.0, "Good": 80.0, "Fair": 55.0, "Poor": 30.0}

        for w in [0.5, 2.0, 8.0, 20.0]:
            for age in [0.5, 1.5, 3.0, 6.0]:
                for cond_name, c_score in cond_scores.items():
                    for price in [100.0, 300.0, 800.0]:
                        X.append([w, age, c_score, price])
                        
                        # Category Class: 0: Light Recyclable, 1: Durable Consumer Good, 2: Heavy Industrial
                        if w < 3.0 and c_score > 70.0:
                            y_cls.append(0)
                        elif w < 15.0:
                            y_cls.append(1)
                        else:
                            y_cls.append(2)

                        # Sustainability Index Score (0-100)
                        s_score = min(100.0, (c_score * 0.5) + (100.0 / (1.0 + age * 0.2)) + (w * 0.5))
                        y_reg.append(s_score)

        X_arr = np.array(X)
        X_scaled = self.scaler.fit_transform(X_arr)
        
        self.mlp_classifier.fit(X_scaled, y_cls)
        self.mlp_regressor.fit(X_scaled, y_reg)
        self.is_trained = True

    def predict(
        self,
        weight_kg: float,
        age_years: float,
        condition_score: float = 80.0,
        original_price: float = 250.0
    ) -> Dict[str, Any]:
        """
        Performs neural network forward propagation inference.
        """
        raw_features = np.array([[weight_kg, age_years, condition_score, original_price]])
        scaled_features = self.scaler.transform(raw_features)

        # 1. MLP Neural Network Classification Forward Pass
        cls_probs = self.mlp_classifier.predict_proba(scaled_features)[0]
        top_cls_idx = int(np.argmax(cls_probs))
        class_labels = ["Light Consumer Recyclable", "Durable Household Item", "Heavy Commercial Waste"]
        predicted_item_archetype = class_labels[top_cls_idx]

        # 2. MLP Neural Network Regression Forward Pass
        predicted_sustainability_index = round(float(self.mlp_regressor.predict(scaled_features)[0]), 2)

        return {
            "algorithm_name": "Multi-Layer Perceptron (MLP) Artificial Neural Network Algorithm",
            "neural_network_architecture": {
                "input_layer_nodes": 4,
                "hidden_layer_1_nodes": 64,
                "hidden_layer_2_nodes": 32,
                "output_layer_nodes": 3,
                "activation_function": "ReLU (Rectified Linear Unit)",
                "optimizer": "Adam (Adaptive Moment Estimation)",
                "total_layers_count": 4
            },
            "predicted_item_archetype": predicted_item_archetype,
            "classification_probability": round(float(cls_probs[top_cls_idx]), 4),
            "predicted_sustainability_index": max(0.0, min(100.0, predicted_sustainability_index)),
            "neural_network_iterations_to_converge": self.mlp_classifier.n_iter_
        }

mlp_neural_network_algorithm = MultiLayerPerceptronAlgorithm()
