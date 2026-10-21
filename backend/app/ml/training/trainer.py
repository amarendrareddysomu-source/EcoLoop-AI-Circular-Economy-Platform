import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from app.ml.preprocessing.preprocessing import preprocessor
from app.core.logging import logger

class ModelTrainer:
    def train_price_model(self, output_path: str) -> bool:
        try:
            logger.info("Training ML Random Forest Resale Price Model...")
            # Generate synthetic training dataset
            np.random.seed(42)
            num_samples = 200

            X = []
            y = []

            categories = ["Electronics", "Furniture", "Clothing", "Plastic", "Paper", "Books"]
            conditions = ["Excellent", "Good", "Fair", "Poor"]

            for _ in range(num_samples):
                cat = np.random.choice(categories)
                cond = np.random.choice(conditions)
                age = np.random.uniform(0.1, 8.0)
                orig_price = np.random.uniform(20.0, 1500.0)

                feat = preprocessor.extract_features(
                    category=cat,
                    brand="Generic",
                    age_years=age,
                    condition=cond,
                    original_price=orig_price,
                    weight_kg=1.5
                )

                cond_mult = preprocessor.get_condition_score(cond)
                age_depr = max(0.1, 1.0 - (age * 0.12))
                target_price = orig_price * cond_mult * age_depr

                X.append(feat)
                y.append(target_price)

            rf = RandomForestRegressor(n_estimators=50, random_state=42)
            rf.fit(X, y)

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            joblib.dump(rf, output_path)
            logger.info(f"Model successfully saved to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error training model: {e}")
            return False

trainer = ModelTrainer()
