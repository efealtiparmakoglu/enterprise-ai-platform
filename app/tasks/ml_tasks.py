"""
ML Tasks - Celery Background Tasks
"""

import asyncio
from typing import Any, Dict

from app.celery_app import celery_app
from app.ml.registry import ModelRegistry
from app.ml.predictor import MLPredictor


@celery_app.task(bind=True, max_retries=3)
def predict_async(self, model_id: str, input_data: Dict[str, Any]):
    """
    Run ML prediction asynchronously
    """
    try:
        # Initialize predictor
        predictor = MLPredictor()
        
        # Load model
        asyncio.run(predictor.load_model(model_id))
        
        # Run prediction
        result = asyncio.run(predictor.predict(input_data))
        
        return {
            "status": "success",
            "model_id": model_id,
            "prediction": result
        }
        
    except Exception as exc:
        # Retry with exponential backoff
        self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@celery_app.task
def train_model(model_id: str, training_data: Dict[str, Any]):
    """
    Train ML model asynchronously
    """
    from app.db.session import SessionLocal
    from app.services.model_service import ModelService
    
    db = SessionLocal()
    try:
        model_service = ModelService(db)
        
        # Update status to training
        asyncio.run(model_service.update_status(model_id, "training"))
        
        # Training logic here...
        # This would be your actual training code
        
        # Update status to active
        asyncio.run(model_service.update_status(model_id, "active"))
        
        return {"status": "success", "model_id": model_id}
        
    finally:
        db.close()


@celery_app.task
def update_model_metrics():
    """
    Update model performance metrics periodically
    """
    from app.db.session import SessionLocal
    from app.services.model_service import ModelService
    
    db = SessionLocal()
    try:
        model_service = ModelService(db)
        
        # Get all active models
        models = asyncio.run(model_service.get_active_models())
        
        for model in models:
            # Calculate metrics
            metrics = asyncio.run(model_service.calculate_metrics(model.id))
            asyncio.run(model_service.update_metrics(model.id, metrics))
        
        return {"updated_models": len(models)}
        
    finally:
        db.close()
