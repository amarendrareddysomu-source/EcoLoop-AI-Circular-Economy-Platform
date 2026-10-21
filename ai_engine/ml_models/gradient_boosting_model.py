"""
ML Algorithm 3: Gradient Boosting Machine (GBM / XGBoost) Algorithm
File: ai_engine/ml_models/gradient_boosting_model.py

Implements Sequential Additive Boosting of Weak Decision Trees.
Minimizes residual loss function along negative gradient vectors to predict non-linear item depreciation.
"""

from typing import Dict, Any, List
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier

class GradientBoostingAlgorithm:
    """
    Gradient Boosting Machine (GBM) Machine Learning Algorithm wrapper.
    """

    def __init__(self):
        self.regressor = GradientBoostingRegressor(
            n_estimators=60,
            learning_rate=0.1,
            max_depth=4,
            random_state=42
        )
        self.classifier = GradientBoostingClassifier(
            n_estimators=40,
            learning_rate=0.1,
            max_depth=3,
            random_state=42
        )
        self.is_trained = False
        self._bootstrap_train()

    def _bootstrap_train(self):
        """
        Trains Gradient Boosting models on item degradation features.
        """
        X, y_reg, y_cls = [], [], []
        for age in np.linspace(0.1, 8.0, 30):
            for wear in np.linspace(0.0, 1.0, 20):
                for co2_base in [5.0, 15.0, 45.0, 100.0]:
                    X.append([age, wear, co2_base])
                    
                    # Target 1: CO2 reduction offset (kg)
                    co2_actual = co2_base * (1.0 - 0.5 * wear) * (1.0 + 0.05 * age)
                    y_reg.append(co2_actual)

                    # Target 2: High/Medium/Low Impact Class (0, 1, 2)
                    if co2_actual >= 30.0:
                        y_cls.append(0)  # High Impact
                    elif co2_actual >= 10.0:
                        y_cls.append(1)  # Medium Impact
                    else:
                        y_cls.append(2)  # Low Impact

        X_arr = np.array(X)
        self.regressor.fit(X_arr, y_reg)
        self.classifier.fit(X_arr, y_cls)
        self.is_trained = True

    def predict(
        self,
        age_years: float,
        wear_index: float,
        base_co2_factor: float = 25.0
    ) -> Dict[str, Any]:
        """
        Performs inference using Gradient Boosting Machine.
        """
        features = np.array([[age_years, wear_index, base_co2_factor]])

        # 1. Gradient Boosting Regression
        predicted_co2 = round(float(self.regressor.predict(features)[0]), 2)

        # 2. Gradient Boosting Classification
        cls_probs = self.classifier.predict_proba(features)[0]
        top_cls_idx = int(np.argmax(cls_probs))
        impact_labels = ["High Environmental Offset", "Medium Environmental Offset", "Low Environmental Offset"]
        predicted_impact_class = impact_labels[top_cls_idx]

        # 3. Feature Importance Metrics
        feat_names = ["age_years", "wear_index", "base_co2_factor"]
        importances = {
            name: round(float(imp), 4) for name, imp in zip(feat_names, self.regressor.feature_importances_)
        }

        # Loss stage train deviations
        train_score_last = round(float(self.regressor.train_score_[-1]), 4)

        return {
            "algorithm_name": "Gradient Boosting Machine (GBM / XGBoost) Algorithm",
            "boosting_stages_estimators": 60,
            "learning_rate_eta": 0.1,
            "tree_max_depth": 4,
            "predicted_co2_offset_kg": max(0.0, predicted_co2),
            "predicted_impact_category": predicted_impact_class,
            "classification_confidence": round(float(cls_probs[top_cls_idx]), 4),
            "feature_importances": importances,
            "final_stage_loss_deviance": train_score_last
        }

gradient_boosting_algorithm = GradientBoostingAlgorithm()
