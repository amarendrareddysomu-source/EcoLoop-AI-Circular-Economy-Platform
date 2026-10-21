from typing import Dict, Any, List, Optional
import math
from app.ml.preprocessing.preprocessing import preprocessor
from app.ml.inference.model_loader import model_loader
from ai_engine.price_predictor import price_predictor as heuristic_price_predictor
from ai_engine.condition_predictor import condition_predictor as heuristic_cond_predictor
from ai_engine.recommendation_engine import recommendation_engine as heuristic_rec_engine

class MLPredictor:
    MATERIAL_RECYCLABILITY = {
        "metal": 0.95,
        "glass": 0.90,
        "paper": 0.85,
        "plastic": 0.75,
        "wood": 0.70,
        "textile": 0.65,
        "electronics": 0.80,
        "composite": 0.50
    }

    def predict_sustainability_score(
        self,
        category: str,
        material: str = "plastic",
        condition: str = "Good",
        weight_kg: float = 1.0,
        reuse_potential: str = "High",
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        cond_score = preprocessor.get_condition_score(condition)
        mat_norm = material.strip().lower() if material else "plastic"
        mat_score = self.MATERIAL_RECYCLABILITY.get(mat_norm, 0.70)

        reuse_map = {"high": 1.0, "moderate": 0.75, "medium": 0.75, "low": 0.40}
        reuse_score = reuse_map.get(reuse_potential.strip().lower(), 0.75)

        base_score = (cond_score * 40.0) + (mat_score * 35.0) + (reuse_score * 25.0)
        # Weight adjustment bonus
        weight_factor = min(1.1, max(0.9, 1.0 + (weight_kg - 1.0) * 0.02))
        final_score = round(min(100.0, max(0.0, base_score * weight_factor)), 1)

        if final_score >= 85.0:
            impact_cat = "Exceptional"
            recommendation = "Optimal circular candidate for immediate reuse and high-impact donation."
        elif final_score >= 70.0:
            impact_cat = "High Impact"
            recommendation = "Strong candidate for resale or refurbishment with minimal environmental loss."
        elif final_score >= 50.0:
            impact_cat = "Medium Impact"
            recommendation = "Suitable for repair or component recycling to maximize material recovery."
        else:
            impact_cat = "Low Impact"
            recommendation = "Recommend specialized material recycling to divert waste from landfills."

        return {
            "sustainability_score": final_score,
            "environmental_impact_category": impact_cat,
            "recommendation": recommendation
        }

    def predict_price(
        self,
        category: str,
        brand: str = "Generic",
        age_years: float = 1.0,
        condition: str = "Good",
        market_factors: Optional[Dict[str, Any]] = None,
        original_price: float = 100.0
    ) -> Dict[str, Any]:
        # Call underlying Random Forest ML / Heuristic model
        est_price = heuristic_price_predictor.predict_price(
            category=category,
            brand=brand,
            age_years=age_years,
            condition=condition,
            original_price=original_price
        )

        demand_multiplier = 1.0
        if market_factors and isinstance(market_factors, dict):
            demand = market_factors.get("demand_level", "medium").lower()
            if demand == "high":
                demand_multiplier = 1.15
            elif demand == "low":
                demand_multiplier = 0.85

        final_price = round(est_price * demand_multiplier, 2)
        min_p = round(max(0.0, final_price * 0.85), 2)
        max_p = round(final_price * 1.15, 2)

        return {
            "predicted_resale_price": final_price,
            "confidence": 0.88,
            "min_price": min_p,
            "max_price": max_p
        }

    def predict_condition(
        self,
        image_bytes: Optional[bytes] = None,
        age_years: float = 1.0,
        usage_level: str = "Moderate",
        user_stated_condition: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        res = heuristic_cond_predictor.predict_condition(
            image_bytes=image_bytes,
            age_years=age_years,
            usage_level=usage_level,
            user_stated_condition=user_stated_condition
        )
        return {
            "predicted_condition": res["predicted_condition"],
            "confidence": res["confidence"]
        }

    def generate_recommendation(
        self,
        category: str,
        condition: str = "Good",
        age_years: float = 1.0,
        estimated_price: float = 50.0,
        location: str = "Local City",
        target_org_type: Optional[str] = None
    ) -> Dict[str, Any]:
        rec_res = heuristic_rec_engine.get_recommendation(
            category=category,
            condition=condition,
            age_years=age_years,
            estimated_price=estimated_price
        )
        action = rec_res["recommended_action"]

        reuse_options = [
            "Direct marketplace listing for peer-to-peer sale",
            "Local community sharing & borrowing network",
            "Refurbishment & resale via certified partner"
        ]

        recycling_methods = [
            "Material segregation & mechanical disassembly",
            "Certified e-waste component recovery",
            "Industrial polymer & metal processing"
        ]

        suitable_buyers_ngos = [
            "Green Earth Circular NGO",
            "EcoTech Recycling Center",
            "Community Support Foundation"
        ]

        sustainability_actions = [
            "Upload detailed photographs to increase buyer trust",
            "Choose local pickup to eliminate shipping carbon emissions",
            "Log transaction upon completion to earn environmental impact points"
        ]

        return {
            "recommended_action": action,
            "action_reasoning": rec_res["action_reasoning"],
            "reuse_options": reuse_options,
            "recycling_methods": recycling_methods,
            "suitable_buyers_ngos": suitable_buyers_ngos,
            "sustainability_actions": sustainability_actions
        }

ml_predictor = MLPredictor()
