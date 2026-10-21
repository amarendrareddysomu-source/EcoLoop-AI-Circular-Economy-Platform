"""
Sustainability Calculator Module
Calculates material-specific Life Cycle Assessment (LCA) environmental impact metrics:
- CO2 Carbon Offset Saved (kg)
- Landfill Waste Diverted (kg)
- Dynamic Sustainability Score (0-100)
"""

MATERIAL_RECYCLABILITY = {
    "Metal Can": 0.95,
    "Aluminum Can": 0.95,
    "Glass Bottle": 0.90,
    "Glass Jar": 0.90,
    "Paper": 0.85,
    "Cardboard": 0.85,
    "Plastic Bottle": 0.75,
    "Plastic Container": 0.70,
    "Plastic Cover": 0.30,
    "Plastic Bag": 0.25,
    "Laptop": 0.65,
    "Phone": 0.60,
    "Electronics": 0.65,
    "Furniture": 0.70,
    "Wood": 0.75,
    "Textile": 0.60,
    "Clothing": 0.60,
    "Organic Waste": 0.90
}

CO2_LCA_FACTOR_PER_KG = {
    "Electronics": 18.5,
    "Laptop": 18.5,
    "Phone": 18.5,
    "Keyboard": 12.0,
    "Monitor": 15.0,
    "Appliance": 10.2,
    "Microwave": 10.2,
    "Refrigerator": 12.5,
    "Washing Machine": 12.5,
    "Metal Can": 6.8,
    "Aluminum Can": 6.8,
    "Clothing": 12.0,
    "Textile": 12.0,
    "Furniture": 4.5,
    "Wood": 4.5,
    "Plastic Bottle": 3.2,
    "Plastic Container": 3.2,
    "Plastic Cover": 3.2,
    "Plastic Bag": 3.2,
    "Paper": 1.8,
    "Cardboard": 1.8,
    "Glass Bottle": 0.9,
    "Glass Jar": 0.9,
    "Organic Waste": 0.5
}

ESTIMATED_WEIGHT_KG = {
    "Laptop": 2.2,
    "Phone": 0.2,
    "Keyboard": 0.8,
    "Monitor": 4.5,
    "Electronics": 2.5,
    "Appliance": 15.0,
    "Furniture": 25.0,
    "Chair": 8.0,
    "Table": 18.0,
    "Desk": 20.0,
    "Sofa": 35.0,
    "Clothing": 0.6,
    "Plastic Cover": 0.05,
    "Plastic Bag": 0.03,
    "Plastic Bottle": 0.08,
    "Cardboard": 0.4,
    "Paper": 0.2,
    "Glass Bottle": 0.5,
    "Metal Can": 0.15
}

class SustainabilityCalculator:
    @staticmethod
    def calculate_impact(
        category: str, 
        condition: str, 
        action: str, 
        item_weight_kg: float = None,
        weight_kg: float = None,
        repairability_score: float = 70.0
    ) -> dict:
        cat = category.title() if category else "Electronics"
        if item_weight_kg is None and weight_kg is not None:
            item_weight_kg = weight_kg
        
        if not item_weight_kg or item_weight_kg <= 0:
            item_weight_kg = ESTIMATED_WEIGHT_KG.get(cat, 1.5)


        # Action multipliers based on circular loop displacement efficiency
        action_multipliers = {
            "Reuse": 1.0,
            "Donate": 1.0,
            "Sell": 1.0,
            "Repair": 0.85,
            "Recycle": 0.65,
            "Dispose Responsibly": 0.20
        }
        
        multiplier = action_multipliers.get(action.title(), 0.70)
        co2_factor = CO2_LCA_FACTOR_PER_KG.get(cat, 3.5)
        recyclability = MATERIAL_RECYCLABILITY.get(cat, 0.60)

        co2_saved = round(item_weight_kg * co2_factor * multiplier, 2)
        waste_diverted = round(item_weight_kg * multiplier, 2)
        
        # Dynamic sustainability score calculation (0 - 100)
        cond_factors = {"Excellent": 1.0, "Good": 0.88, "Fair": 0.70, "Poor": 0.45, "Damaged": 0.25}
        cond_mult = cond_factors.get(condition.title(), 0.70)

        raw_score = (recyclability * 35.0) + (repairability_score * 0.35) + (cond_mult * 30.0)
        sustainability_score = round(max(10.0, min(100.0, raw_score)), 1)

        impact_points = round((co2_saved * 10.0) + (waste_diverted * 5.0), 1)

        return {
            "sustainability_score": sustainability_score,
            "co2_saved_kg": co2_saved,
            "waste_diverted_kg": waste_diverted,
            "environmental_impact_points": impact_points,
            "item_weight_kg": item_weight_kg,
            "material_recyclability_percent": round(recyclability * 100.0, 1)
        }
