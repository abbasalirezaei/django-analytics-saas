import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "analytics_core.settings")

app = Celery("analytics_core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Periodic tasks
app.conf.beat_schedule = {
    "aggregate-daily-stats": {
        "task": "tracking.tasks.aggregate_daily_stats",
        "schedule": crontab(hour=1, minute=0),  # 1 AM daily
    },
    "cleanup-old-sessions": {
        "task": "tracking.tasks.cleanup_old_sessions",
        "schedule": crontab(hour=2, minute=0),  # 2 AM daily
    },
    "update-realtime-cache": {
        "task": "tracking.tasks.update_realtime_cache",
        "schedule": 60.0,  # Every 60 seconds
    },
}

app.conf.timezone = "UTC"
