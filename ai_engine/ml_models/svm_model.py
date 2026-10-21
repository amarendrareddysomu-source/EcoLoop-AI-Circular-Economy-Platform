"""
ML Algorithm 2: Support Vector Machine (SVM) Algorithm with RBF Kernel
File: ai_engine/ml_models/svm_model.py

Implements Kernelized Support Vector Classifier (SVC) and Support Vector Regressor (SVR)
using Radial Basis Function (RBF) Kernel: K(x, x') = exp(-gamma * ||x - x'||^2).
Evaluates decision margins and support vector boundaries.
"""

import warnings
from typing import Dict, Any, List
import numpy as np
from sklearn.svm import SVC, SVR
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore", category=FutureWarning, message=".*probability parameter was deprecated.*")

class SupportVectorMachineAlgorithm:
    """
    Support Vector Machine (SVM) Algorithm wrapper for Margin-Based Classification and Regression.
    """

    def __init__(self):
        self.scaler = StandardScaler()
        self.svc = SVC(kernel="rbf", C=1.0, gamma="scale", probability=True, random_state=42)
        self.svr = SVR(kernel="rbf", C=10.0, epsilon=0.1)
        self.is_trained = False
        self._bootstrap_train()

    def _bootstrap_train(self):
        """
        Trains Support Vector Machine classifier and regressor models.
        """
        X, y_class, y_reg = [], [], []
        # Class labels: 0: Recyclable, 1: Reusable, 2: Repairable
        for age in np.linspace(0.1, 10.0, 35):
            for cond_score in np.linspace(10.0, 100.0, 35):
                for price in np.linspace(10.0, 1000.0, 15):
                    X.append([age, cond_score, price])
                    
                    if cond_score >= 70.0 and age <= 3.0:
                        c_label = 1  # Reusable / Sell
                    elif cond_score >= 40.0:
                        c_label = 2  # Repairable / Donate
                    else:
                        c_label = 0  # Recyclable

                    val = price * (cond_score / 100.0) / (1.0 + 0.15 * age)
                    y_class.append(c_label)
                    y_reg.append(val)

        X_arr = np.array(X)
        X_scaled = self.scaler.fit_transform(X_arr)
        
        self.svc.fit(X_scaled, y_class)
        self.svr.fit(X_scaled, y_reg)
        self.is_trained = True

    def predict(
        self,
        age_years: float,
        condition_score: float,
        original_price: float
    ) -> Dict[str, Any]:
        """
        Performs inference using RBF Kernel Support Vector Machine.
        """
        raw_features = np.array([[age_years, condition_score, original_price]])
        scaled_features = self.scaler.transform(raw_features)

        # 1. SVC Probability & Class Decision Boundary
        class_probs = self.svc.predict_proba(scaled_features)[0]
        predicted_class_idx = int(np.argmax(class_probs))
        class_names = ["Recycle", "Reuse / Sell", "Repair / Donate"]
        predicted_pathway = class_names[predicted_class_idx]

        # 2. SVR Non-Linear Value Estimation
        predicted_value = round(float(self.svr.predict(scaled_features)[0]), 2)

        # 3. Support Vector Metadata
        n_support_vectors = len(self.svc.support_)

        return {
            "algorithm_name": "Support Vector Machine (SVM) Algorithm",
            "kernel": "Radial Basis Function (RBF)",
            "hyperplane_regularization_C": 1.0,
            "gamma_parameter": "scale",
            "predicted_circular_pathway": predicted_pathway,
            "pathway_confidence": round(float(class_probs[predicted_class_idx]), 4),
            "predicted_asset_value": max(0.0, predicted_value),
            "support_vectors_count": n_support_vectors,
            "decision_function_margin": round(float(np.max(self.svc.decision_function(scaled_features))), 4)
        }

svm_algorithm = SupportVectorMachineAlgorithm()
