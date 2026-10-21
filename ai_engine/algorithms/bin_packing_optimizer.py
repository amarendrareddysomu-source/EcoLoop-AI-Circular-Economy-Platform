"""
Algorithm 4: Greedy Best-Fit Decreasing (BFD) Waste Bin-Packing Algorithm
File: ai_engine/algorithms/bin_packing_optimizer.py

Optimizes recycling collection bin allocations by solving multi-constraint (Mass in kg and Volume in m3)
container bin packing using Best-Fit Decreasing (BFD) heuristics.
"""

from typing import Dict, Any, List

class GreedyBestFitBinPackingAlgorithm:
    """
    Greedy Best-Fit Decreasing (BFD) Multi-Constraint Container Packing Optimizer.
    Packs recycling items into standard storage bins while respecting dual mass (kg) and volume (m³) constraints.
    """

    def pack_items(
        self,
        items: List[Dict[str, Any]],
        bin_capacity_kg: float = 100.0,
        bin_capacity_m3: float = 0.5,
        max_available_bins: int = 10
    ) -> Dict[str, Any]:
        """
        Packs a list of recycling items into bins using Best-Fit Decreasing (BFD) strategy.
        """
        if not items:
            return {
                "algorithm_name": "Greedy Best-Fit Decreasing (BFD) Waste Bin-Packing Algorithm",
                "bins_used_count": 0,
                "packed_bins": [],
                "unpacked_overflow_items": [],
                "space_utilization_efficiency_pct": 0.0
            }

        # 1. Sort items in decreasing order of weight density ratio (mass / volume)
        sorted_items = sorted(
            items,
            key=lambda x: (float(x.get("weight_kg", 1.0)) / max(0.001, float(x.get("volume_m3", 0.01)))),
            reverse=True
        )

        bins = []
        unpacked_items = []

        for item in sorted_items:
            item_id = item.get("id", item.get("name", "Item"))
            item_w = float(item.get("weight_kg", 1.0))
            item_v = float(item.get("volume_m3", 0.01))
            item_cat = item.get("category", "General")

            # Find Best-Fit bin (bin with smallest remaining capacity that can fit item)
            best_bin_idx = -1
            min_residual_capacity = float("inf")

            for idx, b in enumerate(bins):
                rem_w = bin_capacity_kg - b["current_weight_kg"]
                rem_v = bin_capacity_m3 - b["current_volume_m3"]

                if rem_w >= item_w and rem_v >= item_v:
                    # Residual capacity metric
                    residual = rem_w + rem_v * 100.0
                    if residual < min_residual_capacity:
                        min_residual_capacity = residual
                        best_bin_idx = idx

            # If suitable bin found, pack item into best_bin_idx
            if best_bin_idx != -1:
                target_bin = bins[best_bin_idx]
                target_bin["items"].append({
                    "id": item_id,
                    "category": item_cat,
                    "weight_kg": item_w,
                    "volume_m3": item_v
                })
                target_bin["current_weight_kg"] = round(target_bin["current_weight_kg"] + item_w, 2)
                target_bin["current_volume_m3"] = round(target_bin["current_volume_m3"] + item_v, 3)
            else:
                # Open a new bin if allowed
                if len(bins) < max_available_bins:
                    new_bin = {
                        "bin_index": len(bins) + 1,
                        "current_weight_kg": item_w,
                        "current_volume_m3": item_v,
                        "capacity_max_kg": bin_capacity_kg,
                        "capacity_max_m3": bin_capacity_m3,
                        "items": [{
                            "id": item_id,
                            "category": item_cat,
                            "weight_kg": item_w,
                            "volume_m3": item_v
                        }]
                    }
                    bins.append(new_bin)
                else:
                    # Container limit reached; item overflowed
                    unpacked_items.append(item)

        # Calculate space utilization metrics
        total_weight_packed = sum(b["current_weight_kg"] for b in bins)
        total_bin_capacity_kg = len(bins) * bin_capacity_kg if bins else 1.0
        utilization_pct = round((total_weight_packed / total_bin_capacity_kg) * 100.0, 2)

        return {
            "algorithm_name": "Greedy Best-Fit Decreasing (BFD) Waste Bin-Packing Algorithm",
            "items_processed_count": len(items),
            "bins_used_count": len(bins),
            "packed_bins": bins,
            "unpacked_overflow_items": unpacked_items,
            "total_packed_weight_kg": round(total_weight_packed, 2),
            "space_utilization_efficiency_pct": utilization_pct
        }

bin_packing_algorithm = GreedyBestFitBinPackingAlgorithm()
