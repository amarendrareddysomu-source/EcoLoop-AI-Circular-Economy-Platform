"""
ML Algorithm 1: Random Forest Classifier & Regressor Algorithm
File: ai_engine/ml_models/random_forest_model.py

Implements Ensemble Machine Learning using Bootstrap Aggregating (Bagging) of Decision Trees.
Extracts Gini Impurity reduction and feature importance metrics for item valuation and classification.
"""

from typing import Dict, Any, List, Optional
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

class RandomForestAlgorithm:
    """
    Random Forest Machine Learning Algorithm wrapper for Classification and Regression tasks.
    """

    def __init__(self):
        self.classifier = RandomForestClassifier(n_estimators=50, random_state=42)
        self.regressor = RandomForestRegressor(n_estimators=50, random_state=42)
        self.label_encoder = LabelEncoder()
        self.is_trained = False
        self._bootstrap_train()

    def _bootstrap_train(self):
        """
        Trains initial Random Forest models on circular economy feature dataset.
        Features: [age_years, original_price, weight_kg, condition_score, category_encoded]
        """
        categories = ["Electronics", "Clothes", "Furniture", "Books", "Plastic", "Metal", "Glass", "Paper", "Battery"]
        self.label_encoder.fit(categories)

        X, y_cat, y_price = [], [], []
        cond_map = {"Excellent": 90.0, "Good": 75.0, "Fair": 50.0, "Poor": 25.0}

        for cat_idx, cat in enumerate(categories):
            for age in [0.5, 1.0, 2.5, 5.0]:
                for price in [50.0, 150.0, 500.0, 1200.0]:
                    for cond_str, cond_score in cond_map.items():
                        weight = 1.0 + (cat_idx * 0.5)
                        X.append([age, price, weight, cond_score, cat_idx])
                        y_cat.append(cat_idx)
                        
                        # Resale price equation for synthetic training
                        resale = price * (0.85 ** age) * (cond_score / 100.0)
                        y_price.append(max(5.0, resale))

        X_arr = np.array(X)
        self.classifier.fit(X_arr, y_cat)
        self.regressor.fit(X_arr, y_price)
        self.is_trained = True

    def predict_item(
        self,
        category: str,
        original_price: float,
        age_years: float,
        condition: str = "Good",
        weight_kg: float = 2.0
    ) -> Dict[str, Any]:
        """
        Performs inference using trained Random Forest Classifier and Regressor.
        """
        cond_map = {"Excellent": 90.0, "Good": 75.0, "Fair": 50.0, "Poor": 25.0, "Damaged": 15.0}
        cond_score = cond_map.get((condition or "Good").title(), 75.0)

        try:
            cat_idx = self.label_encoder.transform([(category or "Electronics").title()])[0]
        except Exception:
            cat_idx = 0

        features = np.array([[age_years, original_price, weight_kg, cond_score, cat_idx]])

        # 1. Random Forest Classification Probabilities
        cat_probs = self.classifier.predict_proba(features)[0]
        top_cat_idx = int(np.argmax(cat_probs))
        predicted_category = str(self.label_encoder.inverse_transform([top_cat_idx])[0])
        classification_confidence = round(float(cat_probs[top_cat_idx]), 4)

        # 2. Random Forest Price Regression Prediction
        predicted_price = round(float(self.regressor.predict(features)[0]), 2)

        # 3. Feature Importance Extraction
        feature_names = ["age_years", "original_price", "weight_kg", "condition_score", "category_code"]
        importances = self.regressor.feature_importances_
        feature_importance_dict = {
            name: round(float(imp), 4) for name, imp in zip(feature_names, importances)
        }

        return {
            "algorithm_name": "Random Forest Machine Learning Algorithm",
            "model_type": "Ensemble Bagging (50 Decision Trees)",
            "predicted_category": predicted_category,
            "classification_confidence": classification_confidence,
            "predicted_resale_price": predicted_price,
            "feature_importances": feature_importance_dict,
            "trees_count": 50,
            "decision_node_split_criterion": "Gini Impurity (Classifier) / MSE (Regressor)"
        }

random_forest_algorithm = RandomForestAlgorithm()
