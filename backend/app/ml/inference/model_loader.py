import os
import joblib
from typing import Any, Optional, Dict
from app.core.logging import logger

class ModelLoader:
    _instance: Optional['ModelLoader'] = None
    _models: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
            cls._instance._models = {}
        return cls._instance

    def load_model(self, model_name: str, model_path: str) -> Optional[Any]:
        if model_name in self._models:
            return self._models[model_name]

        if os.path.exists(model_path):
            try:
                loaded = joblib.load(model_path)
                self._models[model_name] = loaded
                logger.info(f"Successfully loaded ML model '{model_name}' from {model_path}")
                return loaded
            except Exception as e:
                logger.warning(f"Failed to load model file {model_path}: {e}")
                return None
        else:
            logger.info(f"Model file {model_path} not found. Using ML heuristic engine for '{model_name}'.")
            return None

    def get_model(self, model_name: str) -> Optional[Any]:
        return self._models.get(model_name)

model_loader = ModelLoader()
