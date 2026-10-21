from ai_engine.sustainability_calculator import SustainabilityCalculator
from ai_engine.recommendation_engine import recommendation_engine
from ai_engine.price_predictor import price_predictor
from ai_engine.condition_predictor import condition_predictor

def test_sustainability_calculator():
    res = SustainabilityCalculator.calculate_impact("Electronics", "Good", "Reuse")
    assert res["co2_saved_kg"] > 0
    assert res["waste_diverted_kg"] > 0
    assert res["environmental_impact_points"] > 0

def test_recommendation_engine():
    # Selling high-value item
    rec = recommendation_engine.get_recommendation("Electronics", "Excellent", 1.0, 150.0)
    assert rec["recommended_action"] in ["Sell", "Donate", "Repair", "Recycle", "Reuse"]
    assert "recommended_action" in rec

def test_price_predictor():
    price = price_predictor.predict_price("Electronics", "Apple", 2.0, "Good", 500.0)
    assert isinstance(price, float)
    assert 0 < price <= 500.0

def test_condition_predictor():
    cond = condition_predictor.predict_condition(age_years=2.0, usage_level="Moderate")
    assert cond["predicted_condition"] in ["Excellent", "Good", "Fair", "Poor"]
