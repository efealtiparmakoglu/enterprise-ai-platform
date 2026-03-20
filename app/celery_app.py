"""
Celery Application Configuration
"""

from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "ai_platform",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.ml_tasks",
        "app.tasks.email_tasks",
        "app.tasks.cleanup_tasks",
    ]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Istanbul",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Beat schedule
celery_app.conf.beat_schedule = {
    "cleanup-old-predictions": {
        "task": "app.tasks.cleanup_tasks.cleanup_old_predictions",
        "schedule": 86400.0,  # Daily
    },
    "update-model-metrics": {
        "task": "app.tasks.ml_tasks.update_model_metrics",
        "schedule": 3600.0,  # Hourly
    },
}
