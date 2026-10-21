from typing import Dict, Any, List, Optional
import re

class DataPreprocessor:
    CATEGORY_MAPPING = {
        "electronics": "Electronics",
        "furniture": "Furniture",
        "clothing": "Clothing",
        "plastic": "Plastic",
        "paper": "Paper",
        "books": "Books",
        "glass": "Glass",
        "metal": "Metal",
        "appliances": "Appliances"
    }

    CONDITION_SCORE_MAP = {
        "new": 1.0,
        "excellent": 0.95,
        "good": 0.80,
        "used": 0.70,
        "fair": 0.55,
        "recycled": 0.50,
        "poor": 0.30,
        "damaged": 0.20
    }

    @classmethod
    def normalize_category(cls, category: Optional[str]) -> str:
        if not category:
            return "Electronics"
        clean_cat = category.strip().lower()
        return cls.CATEGORY_MAPPING.get(clean_cat, category.title())

    @classmethod
    def get_condition_score(cls, condition: Optional[str]) -> float:
        if not condition:
            return 0.70
        clean_cond = condition.strip().lower()
        return cls.CONDITION_SCORE_MAP.get(clean_cond, 0.70)

    @classmethod
    def clean_text(cls, text: Optional[str]) -> str:
        if not text:
            return ""
        clean = re.sub(r"[^\w\s]", "", text.strip().lower())
        return clean

    @classmethod
    def extract_features(
        cls,
        category: str,
        brand: str = "Generic",
        age_years: float = 1.0,
        condition: str = "Good",
        original_price: float = 100.0,
        weight_kg: float = 1.0
    ) -> List[float]:
        cat_norm = cls.normalize_category(category)
        cond_score = cls.get_condition_score(condition)
        
        # Categorical index feature
        cat_index = float(hash(cat_norm) % 100) / 100.0
        brand_is_generic = 0.0 if brand and brand.lower() != "generic" else 1.0

        return [
            cat_index,
            brand_is_generic,
            max(0.0, float(age_years)),
            cond_score,
            max(0.0, float(original_price)),
            max(0.1, float(weight_kg))
        ]

preprocessor = DataPreprocessor()
