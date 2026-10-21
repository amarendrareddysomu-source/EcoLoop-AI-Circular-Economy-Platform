"""
Algorithm 3: Exponential Decay Asset Market Valuation & Depreciation Algorithm
File: ai_engine/algorithms/exponential_depreciation.py

Calculates post-consumer item market valuation using non-linear exponential decay:
  V(t) = V_original * exp(-lambda * t) * (Gamma_condition) * (1 - Delta_wear) * (1 + Mu_market)
Subject to category-specific raw material scrap valuation lower bound V_floor.
"""

import math
from typing import Dict, Any

class ExponentialDecayMarketValuationAlgorithm:
    """
    Non-linear asset depreciation model with continuous exponential decay and scrap floor enforcement.
    """

    # Category Annual Decay Constant (lambda) & Scrap Material Floor Rate (%)
    DECAY_PARAMETERS = {
        "Electronics": {"lambda": 0.35, "scrap_rate": 0.12},
        "Laptop": {"lambda": 0.32, "scrap_rate": 0.15},
        "Phone": {"lambda": 0.40, "scrap_rate": 0.10},
        "Clothing": {"lambda": 0.28, "scrap_rate": 0.05},
        "Furniture": {"lambda": 0.15, "scrap_rate": 0.18},
        "Books": {"lambda": 0.10, "scrap_rate": 0.08},
        "Plastic": {"lambda": 0.50, "scrap_rate": 0.03},
        "Glass": {"lambda": 0.05, "scrap_rate": 0.04},
        "Metal": {"lambda": 0.08, "scrap_rate": 0.25},
        "Cardboard": {"lambda": 0.60, "scrap_rate": 0.02},
        "General": {"lambda": 0.25, "scrap_rate": 0.10}
    }

    CONDITION_FACTORS = {
        "Excellent": 1.00,
        "Good": 0.85,
        "Fair": 0.65,
        "Poor": 0.40,
        "Damaged": 0.20
    }

    def calculate_valuation(
        self,
        category: str,
        original_price: float,
        age_years: float,
        condition: str = "Good",
        wear_index: float = 0.15,
        market_demand_index: float = 0.00
    ) -> Dict[str, Any]:
        """
        Calculates fair market resale price using continuous exponential decay formula:
        V(t) = V_0 * exp(-lambda * t) * Gamma_cond * (1 - Delta_wear) * (1 + Mu_market)
        """
        orig_p = max(1.0, float(original_price))
        t_years = max(0.0, float(age_years))
        w_index = max(0.0, min(0.90, float(wear_index)))
        m_index = max(-0.50, min(0.50, float(market_demand_index)))

        cat_title = (category or "General").title().strip()
        
        # Match category parameters
        params = self.DECAY_PARAMETERS.get("General")
        for k in self.DECAY_PARAMETERS:
            if k.lower() in cat_title.lower() or cat_title.lower() in k.lower():
                params = self.DECAY_PARAMETERS[k]
                break

        lam = params["lambda"]
        scrap_rate = params["scrap_rate"]

        cond_title = (condition or "Good").title().strip()
        gamma_cond = self.CONDITION_FACTORS.get(cond_title, 0.85)

        # 1. Exponential Decay Component
        exponential_decay_factor = math.exp(-lam * t_years)

        # 2. Raw Model Valuation
        raw_val = orig_p * exponential_decay_factor * gamma_cond * (1.0 - w_index) * (1.0 + m_index)

        # 3. Scrap Material Value Floor
        scrap_floor = orig_p * scrap_rate

        # 4. Final Enforced Valuation
        final_price = round(max(raw_val, scrap_floor), 2)
        total_depreciation_pct = round(((orig_p - final_price) / orig_p) * 100.0, 1)

        # Valuation Confidence Interval (+/- 12%)
        val_lower = round(final_price * 0.88, 2)
        val_upper = round(final_price * 1.12, 2)

        return {
            "algorithm_name": "Exponential Decay Asset Market Valuation & Depreciation Algorithm",
            "category": cat_title,
            "original_price": orig_p,
            "age_years": t_years,
            "condition": cond_title,
            "decay_constant_lambda": lam,
            "exponential_decay_factor": round(exponential_decay_factor, 4),
            "estimated_market_price": final_price,
            "scrap_material_floor": round(scrap_floor, 2),
            "depreciation_percentage": total_depreciation_pct,
            "valuation_confidence_range": {"lower_bound": val_lower, "upper_bound": val_upper},
            "formula_expression": f"V({t_years}y) = ${orig_p} * exp(-{lam} * {t_years}) * {gamma_cond} * (1 - {w_index:.2f})"
        }

exponential_depreciation_algorithm = ExponentialDecayMarketValuationAlgorithm()
