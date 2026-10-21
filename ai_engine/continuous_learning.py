"""
Continuous Learning & Hard Negative Store
Records manual user corrections and misclassified validation samples for continuous model retraining.
"""

import os
import json
import time
import hashlib
from typing import Dict, Any, List, Optional

CORRECTIONS_FILE = os.path.join(os.path.dirname(__file__), "models_store", "continuous_learning_corrections.json")

class ContinuousLearningStore:
    def __init__(self):
        self.file_path = CORRECTIONS_FILE
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

    def record_correction(
        self, 
        image_bytes: Optional[bytes], 
        predicted_label: str, 
        user_correct_label: str, 
        confidence: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Records user manual correction for continuous model retraining.
        """
        img_hash = hashlib.sha256(image_bytes).hexdigest()[:16] if image_bytes else "no_image_hash"
        
        entry = {
            "id": int(time.time() * 1000),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "image_hash": img_hash,
            "predicted_label": predicted_label,
            "user_correct_label": user_correct_label,
            "confidence": round(float(confidence), 4),
            "metadata": metadata or {}
        }

        try:
            records = self.get_all_corrections()
            records.append(entry)
            with open(self.file_path, "w") as f:
                json.dump(records, f, indent=2)
        except Exception:
            pass

        return entry

    def get_all_corrections(self) -> List[Dict[str, Any]]:
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except Exception:
            return []

    def get_hard_negatives_summary(self) -> Dict[str, Any]:
        records = self.get_all_corrections()
        confused_pairs = {}
        for r in records:
            pair = f"{r['predicted_label']} -> {r['user_correct_label']}"
            confused_pairs[pair] = confused_pairs.get(pair, 0) + 1

        return {
            "total_corrections_recorded": len(records),
            "top_confused_pairs": sorted(confused_pairs.items(), key=lambda x: x[1], reverse=True)
        }

continuous_learning_store = ContinuousLearningStore()
