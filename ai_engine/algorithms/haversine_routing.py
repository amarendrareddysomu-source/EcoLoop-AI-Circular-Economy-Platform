"""
Algorithm 2: Haversine & Capacity Weighted Optimal Logistics Routing Algorithm
File: ai_engine/algorithms/haversine_routing.py

Computes Pareto-optimal routing for item collection/recycling/donation by calculating:
1. Haversine Great-Circle Distance (km) between user coordinates and candidate facilities
2. Capacity & operational load factor of recipient NGOs/Recycling Centers
3. Material compatibility matching score
4. Carbon emission estimation for transit
"""

import math
from typing import Dict, Any, List, Optional

class HaversineCapacityRoutingAlgorithm:
    """
    Haversine Distance and Operational Capacity Logistics Matcher.
    """
    EARTH_RADIUS_KM = 6371.0  # Mean radius of Earth in km

    def haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculates Haversine distance in kilometers between two GPS coordinate points.
        """
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        
        a = (
            math.sin(d_lat / 2.0) ** 2 +
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2.0) ** 2
        )
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        distance_km = self.EARTH_RADIUS_KM * c
        return round(distance_km, 3)

    def route_and_match(
        self,
        user_lat: float,
        user_lon: float,
        item_material: str,
        item_weight_kg: float,
        facilities: List[Dict[str, Any]],
        max_search_radius_km: float = 50.0,
        w_dist: float = 0.45,
        w_cap: float = 0.35,
        w_mat: float = 0.20
    ) -> Dict[str, Any]:
        """
        Matches user to optimal recycling center or NGO facility based on Haversine distance,
        available capacity, and material tag compatibility.
        """
        mat_target = (item_material or "general").lower().strip()
        matched_results = []

        for fac in facilities:
            f_lat = float(fac.get("latitude", user_lat + 0.05))
            f_lon = float(fac.get("longitude", user_lon + 0.05))
            f_name = fac.get("name", "Facility Center")
            f_type = fac.get("type", "Recycling Center")  # NGO or Recycling Center
            
            capacity_max = float(fac.get("capacity_max_kg", 1000.0))
            capacity_current = float(fac.get("capacity_current_kg", 200.0))
            accepted_materials = [m.lower() for m in fac.get("accepted_materials", ["electronics", "plastic", "metal", "clothes", "paper"])]

            # 1. Haversine Distance
            dist_km = self.haversine_distance(user_lat, user_lon, f_lat, f_lon)
            if dist_km > max_search_radius_km:
                continue

            # 2. Distance Score (1.0 for 0km, scaling linearly down to 0.0 at max radius)
            dist_score = max(0.0, 1.0 - (dist_km / max_search_radius_km))

            # 3. Available Capacity Score
            avail_capacity_kg = max(0.0, capacity_max - capacity_current)
            capacity_score = min(1.0, avail_capacity_kg / max(1.0, item_weight_kg * 5.0))

            # 4. Material Match Score
            if any(mat in m or m in mat for m in accepted_materials for mat in [mat_target]):
                mat_score = 1.0
            else:
                mat_score = 0.4  # Fallback general material processing capability

            # Total Pareto-Optimal Routing Score (0.0 to 100.0)
            overall_score = round((w_dist * dist_score + w_cap * capacity_score + w_mat * mat_score) * 100.0, 2)

            # Estimated transit carbon emissions (0.12 kg CO2 per km for light logistics vehicle)
            co2_emissions_kg = round(dist_km * 0.12, 3)

            # Estimated transport time in minutes (avg city speed 30 km/h)
            est_minutes = round((dist_km / 30.0) * 60.0 + 5.0, 1)

            matched_results.append({
                "facility_id": fac.get("id", f_name),
                "facility_name": f_name,
                "facility_type": f_type,
                "distance_km": dist_km,
                "travel_time_minutes": est_minutes,
                "capacity_available_kg": round(avail_capacity_kg, 1),
                "routing_score": overall_score,
                "co2_transit_footprint_kg": co2_emissions_kg,
                "material_compatible": mat_score == 1.0
            })

        # Sort facilities by highest routing score
        matched_results.sort(key=lambda x: x["routing_score"], reverse=True)

        best_match = matched_results[0] if matched_results else None

        return {
            "algorithm_name": "Haversine & Capacity Weighted Optimal Logistics Routing Algorithm",
            "user_coordinates": {"latitude": user_lat, "longitude": user_lon},
            "item_specs": {"material": mat_target, "weight_kg": item_weight_kg},
            "facilities_evaluated_count": len(facilities),
            "facilities_in_range_count": len(matched_results),
            "optimal_facility": best_match,
            "ranked_facilities": matched_results
        }

haversine_routing_algorithm = HaversineCapacityRoutingAlgorithm()
