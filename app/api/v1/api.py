"""
API Router Configuration
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, models, predictions, users, health

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(models.router, prefix="/models", tags=["ML Models"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["Predictions"])
api_router.include_router(health.router, prefix="/health", tags=["Health"])
