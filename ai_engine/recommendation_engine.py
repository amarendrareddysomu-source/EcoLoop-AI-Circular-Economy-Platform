"""
Phase 5 Repairability Knowledge Base & Phase 8 Recommendation Engine
Deterministic Knowledge Base for repairability and e-waste safety rules.
"""

from typing import Dict, Any, List, Union, Optional

class RecommendationEngine:
    # Phase 5 Repairability Knowledge Base Matrix
    REPAIRABILITY_KNOWLEDGE_BASE = {
        # Primary 10 Categories
        "Battery": (0.0, "None", "Batteries contain sealed chemical cells and cannot be safely repaired."),
        "Biological": (0.0, "None", "Organic biological matter. Compost or dispose in organic waste bin."),
        "Cardboard": (15.0, "Very Low", "Fibreboard material. Taping possible for low load; recycle."),
        "Clothes": (65.0, "Medium", "Stitching, patching, button replacement, and zipper repair."),
        "Glass": (10.0, "Very Low", "Silica glass. Structural glue unsafe for liquid storage; recycle."),
        "Metal": (25.0, "Low", "Scrap metal or aluminum can. Metal welding or recycling recommended."),
        "Paper": (5.0, "Very Low", "Cellulose paper fiber. Non-repairable; recycle."),
        "Plastic": (15.0, "Very Low", "Molded thermoplastic. Patching possible for non-food use; recycle."),
        "Shoes": (55.0, "Medium", "Sole re-gluing, stitching, and lace replacement."),
        "Trash": (0.0, "None", "Non-recyclable residual waste. Dispose responsibly in trash."),

        # Batteries & Hazardous (None / Very Low)
        "Battery AA": (0.0, "None", "Batteries contain sealed chemical cells and cannot be safely repaired."),
        "Battery AAA": (0.0, "None", "Sealed electrochemical cell. Do not attempt disassembly."),
        "Lithium Battery": (5.0, "Very Low", "High fire risk. Component repair not supported."),
        "Car Battery": (10.0, "Very Low", "Sealed lead-acid electrolyte. Hazardous to repair."),
        "Aerosol Can": (0.0, "None", "Pressurized gas container. Disassembly prohibited."),
        
        # Packaging & Disposable Plastics (None / Very Low)
        "Plastic Cover": (0.0, "None", "Disposable thin-film polymer. Non-repairable."),
        "Plastic Bag": (0.0, "None", "Single-use polymer film. Non-repairable."),
        "Plastic Bottle": (5.0, "Very Low", "Single-use PET container. Non-repairable."),
        "Plastic Container": (20.0, "Low", "Molded thermoplastic. Patching possible for non-food use."),
        "Cardboard Box": (15.0, "Very Low", "Fibreboard material. Taping possible for low load."),
        "Paper Sheet": (5.0, "Very Low", "Cellulose paper fiber. Non-repairable."),
        "Envelope": (0.0, "None", "Single-use paper stationery. Non-repairable."),
        "Glass Bottle": (10.0, "Very Low", "Silica glass container. Structural glue unsafe for liquid storage."),
        "Aluminium Can": (0.0, "None", "Single-use aluminum beverage container. Non-repairable."),
        "Steel Can": (0.0, "None", "Single-use tinplate steel container. Non-repairable."),
        "Organic Waste": (0.0, "None", "Biodegradable organic matter. Non-repairable."),
        "Trash": (0.0, "None", "Non-recyclable residual waste. Non-repairable."),


        # High Repairability Items (High / 75-90)
        "Laptop": (85.0, "High", "Modular components: RAM, SSD, battery, keyboard, screen replaceable."),
        "Phone": (75.0, "High", "Replaceable display glass, battery, charging port module."),
        "Smartphone": (75.0, "High", "Replaceable screen, battery, camera module via repair center."),
        "Keyboard": (70.0, "High", "Replaceable keycaps, switches, and USB cable assembly."),
        "Monitor": (80.0, "High", "Replaceable power board, backlight LED strip, and capacitors."),
        "Printer": (72.0, "High", "Replaceable ink/toner cartridges, rollers, and paper tray."),
        "Desktop PC": (90.0, "High", "Fully modular ATX standard architecture."),

        # Medium Repairability Items (Medium / 50-65)
        "Wooden Chair": (60.0, "Medium", "Wood glue, dowel joints, screws, sanding, and refinishing."),
        "Chair": (60.0, "Medium", "Replaceable casters, gas lift cylinder, and bolt hardware."),
        "Wooden Table": (65.0, "Medium", "Wood filler, sanding, leg re-tightening, and varnish."),
        "Table": (65.0, "Medium", "Structural leg and bolt re-tightening."),
        "Desk": (65.0, "Medium", "Drawer slide and leg hardware replacement."),
        "Sofa": (55.0, "Medium", "Re-upholstery, spring tensioning, and cushion stuffing."),
        "Clothing": (65.0, "Medium", "Stitching, patching, button replacement, and zipper repair."),
        "Sneakers": (50.0, "Medium", "Sole re-gluing and lace replacement."),
        "T-Shirt": (60.0, "Medium", "Fabric patching and seam sewing.")
    }

    def compute_repairability(self, category: str, condition: str) -> Dict[str, Any]:
        cat_title = (category or "Electronics").title()
        
        # Match exact knowledge base entry
        kb_entry = None
        for key in self.REPAIRABILITY_KNOWLEDGE_BASE:
            if key.lower() in cat_title.lower() or cat_title.lower() in key.lower():
                kb_entry = self.REPAIRABILITY_KNOWLEDGE_BASE[key]
                break

        if not kb_entry:
            kb_entry = (65.0, "Medium", "General modular assembly.")

        base_score, base_rating, reasoning = kb_entry

        cond_factors = {"Excellent": 1.1, "Good": 1.0, "Fair": 0.8, "Poor": 0.5, "Damaged": 0.3, "Unknown": 0.7}
        factor = cond_factors.get((condition or "Good").title(), 0.8)

        final_score = round(max(5.0, min(100.0, base_score * factor)), 1)

        if final_score >= 75.0:
            rating = "High"
        elif final_score >= 45.0:
            rating = "Medium"
        elif final_score > 5.0:
            rating = "Low"
        else:
            rating = "None"

        return {
            "repairability_score": final_score,
            "repairability_rating": rating,
            "repairability_reasoning": reasoning
        }

    def get_recommendation(
        self, 
        category: str, 
        condition: str, 
        age_years: float = 1.0, 
        estimated_price: Union[float, dict] = 0.0,
        repairability_score: Optional[float] = None
    ) -> Dict[str, Any]:
        cat_title = (category or "Electronics").title().strip()
        cond_title = (condition or "Good").title().strip()

        # Compute actual repairability score if not explicitly passed
        if repairability_score is None or repairability_score == 70.0:
            rep_data = self.compute_repairability(cat_title, cond_title)
            repairability_score = rep_data["repairability_score"]

        if isinstance(estimated_price, dict):
            price_val = float(estimated_price.get("predicted_resale_price", 0.0))
        else:
            try:
                price_val = float(estimated_price or 0.0)
            except Exception:
                price_val = 0.0

        cat_lower = cat_title.lower()

        # 1. Batteries & E-Waste Hazardous Materials -> Recycle
        if any(b in cat_lower for b in ["battery", "cell", "lithium", "aerosol"]):
            action = "Recycle"
            reasoning = "Recycle at authorized e-waste collection center. Hazardous electrochemical components require specialized material recovery."
            reuse_options = ["Do not reuse spent electrochemical cells", "Deposit at certified e-waste bin"]
            recycling_methods = ["Authorized e-waste collection center", "Hydrometallurgical battery recycling facility"]

        # 2. Biological & Organic Waste -> Compost / Dispose Safely
        elif any(o in cat_lower for o in ["biological", "organic", "compost", "food"]):
            action = "Dispose Safely"
            reasoning = "Biological organic material. Recommended to route to municipal composting or organic waste bio-degradation facility."
            reuse_options = ["Home garden composting", "Anaerobic digestion bio-gas conversion"]
            recycling_methods = ["Municipal organic composting stream"]

        # 3. Packaging & Recyclable Materials (Cardboard, Paper, Glass, Metal, Plastic) -> Recycle
        elif any(p in cat_lower for p in ["cardboard", "paper", "glass", "metal", "plastic", "can", "bottle", "container", "box", "envelope", "film", "cover"]):
            action = "Recycle"
            reasoning = f"{cat_title} is a recyclable material. Recommended to route to a local material recovery center for industrial recycling."
            reuse_options = ["Upcycle into household containers", "Collect for material drop-off point"]
            recycling_methods = ["Single-stream curbside recycling", "Material recovery facility (MRF) sorting"]

        # 4. Residual Non-Recyclable Trash -> Dispose Safely
        elif "trash" in cat_lower or "residual" in cat_lower:
            action = "Dispose Safely"
            reasoning = "Residual trash waste. Recommended for safe municipal waste management or waste-to-energy recovery."
            reuse_options = ["Collect for municipal waste pickup", "Deposit at non-recyclable waste receptacle"]
            recycling_methods = ["Waste-to-energy recovery facility", "Sanitary municipal landfill management"]

        # 5. High-value resale items (Electronics, Furniture, Clothes, Shoes in Excellent/Good condition) -> Sell / Donate
        elif price_val >= 10.0 and cond_title in ["Excellent", "Good"]:
            action = "Sell"
            resale_inr = round(price_val * 83.0)
            reasoning = f"Item is in {cond_title} condition with estimated market resale value of ₹{resale_inr:,} (${price_val:.2f}). Listing for resale maximizes economic recovery."
            reuse_options = ["List on circular marketplace for resale", "Trade-in for refurbishment credit"]
            recycling_methods = ["Certified recycling if un-sold"]

        # 6. Reusable/Repairable items (Clothes, Shoes, Furniture, Electronics) in Fair/Poor condition with high repairability -> Repair
        elif cond_title in ["Fair", "Damaged", "Poor"] and repairability_score >= 45.0:
            action = "Repair"
            reasoning = f"Item has repair potential (Repairability: {repairability_score}/100). Refurbishment, stitching, or component replacement will restore utility."
            reuse_options = ["Local repair café or component replacement", "Refurbish for community center reuse"]
            recycling_methods = ["Depot component harvesting"]

        # 7. Functional items in Good/Fair condition -> Donate
        elif cond_title in ["Excellent", "Good", "Fair"]:
            action = "Donate"
            reasoning = "Item is functional. Donating to verified community NGOs provides social value and diverts waste from landfills."
            reuse_options = ["Donate to local community shelters or NGOs", "Free-cycle community distribution"]
            recycling_methods = ["Material recycling collection"]

        # 8. Severely damaged non-repairable -> Dispose Safely
        else:
            action = "Dispose Safely"
            reasoning = f"Item is in {cond_title} condition with low repair potential. Route to certified dismantling facility."
            reuse_options = ["Component harvesting for spare parts"]
            recycling_methods = ["Certified dismantling and material extraction"]

        return {
            "recommended_action": action,
            "action_reasoning": reasoning,
            "reuse_options": reuse_options,
            "recycling_methods": recycling_methods,
            "suitable_buyers_ngos": ["Local Certified Circular Recycling Centers", "Community Shelter NGOs"],
            "sustainability_actions": ["Keep out of municipal landfill streams", "Log impact on platform dashboard"]
        }

recommendation_engine = RecommendationEngine()
