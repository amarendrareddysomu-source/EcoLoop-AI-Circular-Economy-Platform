"""
Algorithm 1: Analytic Hierarchy Process (AHP) Circular Priority Matrix Algorithm
File: ai_engine/algorithms/ahp_circular_decision.py

Implements Multi-Criteria Decision Analysis (MCDM) via Saaty's Analytic Hierarchy Process (AHP).
Evaluates circular disposition pathways (Reuse, Repair, Donate, Sell, Recycle) across 5 weighted criteria:
1. CO2 Offset Potential (30%)
2. Financial Resale Return (25%)
3. Item Repairability Index (20%)
4. NGO/Community Need (15%)
5. Urgency / Degradation Risk (10%)
"""

import math
from typing import Dict, Any, List

class AHPCircularPriorityMatrixAlgorithm:
    """
    Analytic Hierarchy Process (AHP) Decision Matrix Algorithm for Circular Action Recommendation.
    Calculates principal eigenvector weights, matrix consistency index (CI), and consistency ratio (CR).
    """

    CRITERIA = ["co2_offset", "financial_return", "repairability", "ngo_demand", "urgency"]
    ACTIONS = ["Reuse", "Repair", "Donate", "Sell", "Recycle"]
    
    # Random Index (RI) lookup for Saaty AHP consistency check
    RANDOM_INDEX = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24}

    def __init__(self):
        # 5x5 Pairwise Comparison Matrix for Criteria
        # Comparing: [CO2 Offset, Financial Return, Repairability, NGO Demand, Urgency]
        self.criteria_pairwise_matrix = [
            [1.00, 1.33, 1.50, 2.00, 3.00],  # CO2 Offset vs others
            [0.75, 1.00, 1.25, 1.67, 2.50],  # Financial Return
            [0.67, 0.80, 1.00, 1.33, 2.00],  # Repairability
            [0.50, 0.60, 0.75, 1.00, 1.50],  # NGO Demand
            [0.33, 0.40, 0.50, 0.67, 1.00],  # Urgency
        ]

    def _normalize_and_eigenvector(self, matrix: List[List[float]]) -> Dict[str, Any]:
        """
        Normalizes columns and computes priority eigenvector W, Lambda_max, CI, and CR.
        """
        n = len(matrix)
        col_sums = [sum(matrix[r][c] for r in range(n)) for c in range(n)]
        
        # Normalize matrix
        norm_matrix = []
        for r in range(n):
            row_norm = [matrix[r][c] / col_sums[c] for c in range(n)]
            norm_matrix.append(row_norm)

        # Priority eigenvector (Row means)
        eigenvector = [sum(norm_matrix[r]) / n for r in range(n)]

        # Calculate Lambda_max: sum(col_sum[i] * eigenvector[i])
        lambda_max = sum(col_sums[i] * eigenvector[i] for i in range(n))

        # Consistency Index (CI) and Ratio (CR)
        ci = (lambda_max - n) / (n - 1) if n > 1 else 0.0
        ri = self.RANDOM_INDEX.get(n, 1.12)
        cr = ci / ri if ri > 0 else 0.0

        return {
            "eigenvector": eigenvector,
            "lambda_max": round(lambda_max, 4),
            "consistency_index": round(ci, 4),
            "consistency_ratio": round(cr, 4),
            "is_consistent": cr <= 0.10
        }

    def evaluate(
        self,
        category: str,
        condition: str,
        age_years: float = 1.0,
        estimated_price: float = 50.0,
        co2_saved_kg: float = 5.0,
        repairability_score: float = 65.0,
        ngo_demand_score: float = 70.0,
        urgency_score: float = 40.0
    ) -> Dict[str, Any]:
        """
        Executes the AHP Circular Decision Algorithm for an item.
        """
        # Step 1: Compute criteria priority weights
        ahp_crit = self._normalize_and_eigenvector(self.criteria_pairwise_matrix)
        w_co2, w_fin, w_rep, w_ngo, w_urg = ahp_crit["eigenvector"]

        cond_upper = (condition or "Good").title()
        cat_lower = (category or "Electronics").lower()

        # Step 2: Score candidate actions (0-100) across criteria based on domain rules
        # Actions: ["Reuse", "Repair", "Donate", "Sell", "Recycle"]
        
        # CO2 Offset scores
        co2_scores = {
            "Reuse": min(100.0, co2_saved_kg * 12.0 + 20.0),
            "Repair": min(100.0, co2_saved_kg * 10.0 + 25.0),
            "Donate": min(100.0, co2_saved_kg * 9.0 + 15.0),
            "Sell": min(100.0, co2_saved_kg * 8.0 + 10.0),
            "Recycle": min(100.0, co2_saved_kg * 5.0 + 5.0)
        }

        # Financial Return scores
        fin_scores = {
            "Sell": min(100.0, estimated_price * 1.2),
            "Reuse": min(100.0, estimated_price * 0.8),
            "Repair": min(100.0, estimated_price * 0.6),
            "Donate": 15.0,  # Tax writeoff value
            "Recycle": 10.0  # Scrap value
        }

        # Repairability scores
        rep_scores = {
            "Repair": repairability_score,
            "Reuse": repairability_score * 0.9 if cond_upper in ["Excellent", "Good"] else 30.0,
            "Sell": repairability_score * 0.8 if cond_upper in ["Excellent", "Good"] else 20.0,
            "Donate": repairability_score * 0.85,
            "Recycle": 100.0 if repairability_score < 30.0 else 20.0
        }

        # NGO Demand scores
        ngo_scores = {
            "Donate": ngo_demand_score,
            "Reuse": ngo_demand_score * 0.7,
            "Repair": ngo_demand_score * 0.6 if cond_upper in ["Fair", "Poor"] else 40.0,
            "Sell": 20.0,
            "Recycle": 30.0
        }

        # Urgency scores
        urg_scores = {
            "Recycle": urgency_score * 1.2,
            "Donate": urgency_score * 0.8,
            "Sell": urgency_score * 0.6,
            "Repair": urgency_score * 0.5,
            "Reuse": urgency_score * 0.4
        }

        # Step 3: Compute final synthesized MCDM score vector for each action
        action_scores = {}
        for act in self.ACTIONS:
            s_co2 = co2_scores[act]
            s_fin = fin_scores[act]
            s_rep = rep_scores[act]
            s_ngo = ngo_scores[act]
            s_urg = urg_scores[act]

            total_score = (
                w_co2 * s_co2 +
                w_fin * s_fin +
                w_rep * s_rep +
                w_ngo * s_ngo +
                w_urg * s_urg
            )
            action_scores[act] = round(total_score, 2)

        # Rank actions
        ranked_actions = sorted(action_scores.items(), key=lambda x: x[1], reverse=True)
        recommended_action, top_score = ranked_actions[0]

        return {
            "algorithm_name": "Analytic Hierarchy Process (AHP) Circular Priority Matrix Algorithm",
            "recommended_action": recommended_action,
            "ahp_score": top_score,
            "ranked_action_scores": dict(ranked_actions),
            "criteria_weights": {
                "co2_offset": round(w_co2, 4),
                "financial_return": round(w_fin, 4),
                "repairability": round(w_rep, 4),
                "ngo_demand": round(w_ngo, 4),
                "urgency": round(w_urg, 4)
            },
            "matrix_consistency": {
                "lambda_max": ahp_crit["lambda_max"],
                "consistency_index": ahp_crit["consistency_index"],
                "consistency_ratio": ahp_crit["consistency_ratio"],
                "is_valid": ahp_crit["is_consistent"]
            }
        }

ahp_algorithm = AHPCircularPriorityMatrixAlgorithm()
