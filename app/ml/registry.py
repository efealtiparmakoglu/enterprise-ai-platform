"""
ML Model Registry
"""

import os
from typing import Any, Dict, Optional
import aiofiles
import joblib


class ModelRegistry:
    """Model registry for loading and caching ML models"""
    
    def __init__(self):
        self.models: Dict[str, Any] = {}
        self.model_path = os.getenv("MODEL_STORAGE_PATH", "./models")
    
    async def initialize(self):
        """Initialize registry"""
        os.makedirs(self.model_path, exist_ok=True)
        print(f"📦 Model registry initialized at {self.model_path}")
    
    async def load_model(self, model_id: str, framework: str = "sklearn") -> Any:
        """Load model from disk"""
        if model_id in self.models:
            return self.models[model_id]
        
        model_file = os.path.join(self.model_path, f"{model_id}.pkl")
        
        if not os.path.exists(model_file):
            raise FileNotFoundError(f"Model {model_id} not found")
        
        # Load based on framework
        if framework == "sklearn":
            model = joblib.load(model_file)
        elif framework == "tensorflow":
            import tensorflow as tf
            model = tf.keras.models.load_model(model_file)
        elif framework == "pytorch":
            import torch
            model = torch.load(model_file)
        else:
            model = joblib.load(model_file)
        
        # Cache model
        self.models[model_id] = model
        return model
    
    async def save_model(self, model_id: str, model: Any, framework: str = "sklearn"):
        """Save model to disk"""
        model_file = os.path.join(self.model_path, f"{model_id}.pkl")
        
        if framework == "sklearn":
            joblib.dump(model, model_file)
        elif framework == "tensorflow":
            model.save(model_file)
        elif framework == "pytorch":
            import torch
            torch.save(model, model_file)
        else:
            joblib.dump(model, model_file)
        
        # Update cache
        self.models[model_id] = model
    
    def unload_model(self, model_id: str):
        """Remove model from cache"""
        if model_id in self.models:
            del self.models[model_id]


class MLPredictor:
    """ML Predictor for making predictions"""
    
    def __init__(self):
        self.model = None
        self.model_id = None
    
    async def load_model(self, model_id: str):
        """Load model into predictor"""
        from app.main import app
        registry: ModelRegistry = app.state.model_registry
        self.model = await registry.load_model(model_id)
        self.model_id = model_id
    
    async def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make prediction"""
        if self.model is None:
            raise ValueError("Model not loaded")
        
        import numpy as np
        
        # Convert input to numpy array
        features = np.array(input_data.get("features", [])).reshape(1, -1)
        
        # Make prediction
        prediction = self.model.predict(features)
        
        # Get probability if available
        probability = None
        if hasattr(self.model, "predict_proba"):
            probability = self.model.predict_proba(features).tolist()
        
        return {
            "prediction": prediction.tolist(),
            "probability": probability,
            "model_id": self.model_id
        }
